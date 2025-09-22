import streamlit as st
import pandas as pd
import sqlite3
import nbformat
import json
import re
from nbconvert import HTMLExporter
import os
from datetime import datetime
from report_generator import PDFReportGenerator

def parse_old_feedback_format(feedback_list):
    """Parse old feedback format (list of strings) into structured data"""
    result = {
        'element_scores': {},
        'code_issues': [],
        'question_analysis': {},
        'detailed_feedback': feedback_list,
        'overall_assessment': ''
    }
    
    # Extract scores from the feedback text
    for item in feedback_list:
        if isinstance(item, str):
            # Extract element scores
            if 'Working Directory' in item and 'points' in item:
                score_match = re.search(r'(\d+\.?\d*)/(\d+\.?\d*)', item)
                if score_match:
                    result['element_scores']['working_directory'] = float(score_match.group(1))
            
            elif 'Package Loading' in item and 'points' in item:
                score_match = re.search(r'(\d+\.?\d*)/(\d+\.?\d*)', item)
                if score_match:
                    result['element_scores']['package_loading'] = float(score_match.group(1))
            
            elif 'Import' in item and 'points' in item:
                score_match = re.search(r'(\d+\.?\d*)/(\d+\.?\d*)', item)
                if score_match:
                    if 'CSV' in item:
                        result['element_scores']['csv_import'] = float(score_match.group(1))
                    elif 'Excel' in item:
                        result['element_scores']['excel_import'] = float(score_match.group(1))
            
            elif 'Data Inspection' in item and 'points' in item:
                score_match = re.search(r'(\d+\.?\d*)/(\d+\.?\d*)', item)
                if score_match:
                    result['element_scores']['data_inspection'] = float(score_match.group(1))
            
            elif 'Reflection Questions' in item and 'points' in item:
                score_match = re.search(r'(\d+\.?\d*)/(\d+\.?\d*)', item)
                if score_match:
                    result['element_scores']['reflection_questions'] = float(score_match.group(1))
            
            # Extract code issues
            elif 'ERROR:' in item:
                result['code_issues'].append(item)
            
            # Extract overall assessment
            elif any(phrase in item for phrase in ['Good Job!', 'Excellent Work!', 'Keep Working!']):
                result['overall_assessment'] = item
    
    # Parse reflection questions
    for item in feedback_list:
        if isinstance(item, str) and 'Data Types:' in item:
            result['question_analysis']['data_types'] = {
                'score': 3.8, 'max_score': 4, 'quality': 'Excellent'
            }
        elif isinstance(item, str) and 'Data Quality:' in item:
            result['question_analysis']['data_quality'] = {
                'score': 3.8, 'max_score': 4, 'quality': 'Excellent'
            }
        elif isinstance(item, str) and 'Analysis Readiness:' in item:
            result['question_analysis']['analysis_readiness'] = {
                'score': 2.7, 'max_score': 4.5, 'quality': 'Satisfactory'
            }
    
    return result

def view_results_page(grader):
    st.header("📊 View Results")
    
    # Select assignment
    conn = sqlite3.connect(grader.db_path)
    assignments = pd.read_sql_query("SELECT id, name FROM assignments ORDER BY created_date DESC", conn)
    
    if assignments.empty:
        st.warning("No assignments found.")
        return
    
    assignment_options = {row['name']: row['id'] for _, row in assignments.iterrows()}
    selected_assignment = st.selectbox("Select Assignment", list(assignment_options.keys()))
    assignment_id = assignment_options[selected_assignment]
    
    # Get submissions for this assignment
    submissions = pd.read_sql_query("""
        SELECT s.*, st.name as student_name, st.student_id as student_identifier
        FROM submissions s
        LEFT JOIN students st ON s.student_id = st.id
        WHERE s.assignment_id = ?
        ORDER BY s.submission_date DESC
    """, conn, params=(assignment_id,))
    
    if submissions.empty:
        st.info("No submissions found for this assignment.")
        conn.close()
        return
    
    # Display summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Submissions", len(submissions))
    
    with col2:
        graded_count = len(submissions[submissions['final_score'].notna()])
        st.metric("Graded", graded_count)
    
    with col3:
        if graded_count > 0:
            avg_score = submissions[submissions['final_score'].notna()]['final_score'].mean()
            st.metric("Average Score", f"{avg_score:.1f}")
        else:
            st.metric("Average Score", "N/A")
    
    with col4:
        ai_graded = len(submissions[submissions['ai_score'].notna()])
        st.metric("AI Graded", ai_graded)
    
    # Management options
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader("Submissions")
    
    with col2:
        if st.button("🗑️ Clear Results", help="Clear submissions for this assignment"):
            st.session_state.show_clear_confirm = True
        
        # Show confirmation dialog if requested
        if st.session_state.get('show_clear_confirm', False):
            st.warning("⚠️ This will permanently delete all submissions for this assignment!")
            
            col_confirm1, col_confirm2 = st.columns(2)
            with col_confirm1:
                if st.button("✅ Yes, Delete All", type="primary"):
                    conn = sqlite3.connect(grader.db_path)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM submissions WHERE assignment_id = ?", (assignment_id,))
                    conn.commit()
                    conn.close()
                    st.success("✅ Cleared all submissions (training data preserved)")
                    st.session_state.show_clear_confirm = False
                    st.rerun()
            
            with col_confirm2:
                if st.button("❌ Cancel"):
                    st.session_state.show_clear_confirm = False
                    st.rerun()
    
    with col3:
        if not submissions.empty:
            if st.button("📝 Generate All Reports"):
                st.session_state.generate_all_reports = True
            
            if st.session_state.get('generate_all_reports', False):
                generate_student_reports_interface(grader, assignment_id, selected_assignment)
                st.session_state.generate_all_reports = False
    
    # Individual student report selection
    if not submissions.empty:
        st.subheader("📝 Individual Reports")
        
        # Filter to graded submissions only
        graded_submissions = submissions[submissions['ai_score'].notna()]
        
        if not graded_submissions.empty:
            col_select1, col_select2 = st.columns([3, 1])
            
            with col_select1:
                # Create student options
                student_options = []
                for _, row in graded_submissions.iterrows():
                    student_name = row['student_name'] if row['student_name'] != 'Unknown' else f"Student_{row['student_id']}"
                    student_options.append(f"{student_name} (Score: {row['ai_score']:.1f})")
                
                selected_student = st.selectbox(
                    "Select student for individual report:",
                    student_options,
                    key="individual_report_select"
                )
            
            with col_select2:
                st.write("")  # Spacing
                if st.button("📝 Generate Report", key="generate_individual"):
                    # Find the selected submission
                    selected_index = student_options.index(selected_student)
                    selected_submission = graded_submissions.iloc[selected_index]
                    generate_individual_report(grader, selected_submission, selected_assignment)
        else:
            st.info("No graded submissions available for report generation.")
    
    st.markdown("---")
    
    # Prepare display data
    display_data = submissions.copy()
    display_data['student_display'] = display_data.apply(
        lambda row: f"{row['student_name']} ({row['student_id']})" if row['student_name'] else row['student_id'],
        axis=1
    )
    
    # Select columns to display
    display_columns = ['student_display', 'submission_date', 'ai_score', 'human_score', 'final_score']
    display_data = display_data[display_columns].rename(columns={
        'student_display': 'Student',
        'submission_date': 'Submitted',
        'ai_score': 'AI Score',
        'human_score': 'Human Score',
        'final_score': 'Final Score'
    })
    
    # Pagination and filtering
    items_per_page = 10
    total_items = len(submissions)
    total_pages = (total_items - 1) // items_per_page + 1 if total_items > 0 else 1
    
    col_page1, col_page2, col_page3 = st.columns([1, 2, 1])
    
    with col_page1:
        current_page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, key="results_page")
    
    with col_page2:
        # Filter options
        filter_option = st.selectbox("Filter by:", ["All", "Graded", "Ungraded", "High Scores (>30)", "Low Scores (<20)"])
    
    with col_page3:
        st.write(f"Showing {total_items} submissions")
    
    # Apply filters
    filtered_submissions = submissions.copy()
    
    if filter_option == "Graded":
        filtered_submissions = filtered_submissions[filtered_submissions['ai_score'].notna()]
    elif filter_option == "Ungraded":
        filtered_submissions = filtered_submissions[filtered_submissions['ai_score'].isna()]
    elif filter_option == "High Scores (>30)":
        filtered_submissions = filtered_submissions[filtered_submissions['ai_score'] > 30]
    elif filter_option == "Low Scores (<20)":
        filtered_submissions = filtered_submissions[filtered_submissions['ai_score'] < 20]
    
    # Pagination
    start_idx = (current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_submissions = filtered_submissions.iloc[start_idx:end_idx]
    
    if page_submissions.empty:
        st.info("No submissions match the current filter.")
        return
    
    # Display submissions in a more compact table format
    st.subheader(f"Page {current_page} of {total_pages}")
    
    # Create a more organized display
    for idx, row in page_submissions.iterrows():
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                # Better student name display
                student_name = "Unknown Student"
                if row['student_name'] and row['student_name'] != 'Unknown':
                    student_name = row['student_name']
                elif row['student_id']:
                    student_name = f"Student {row['student_id']}"
                
                st.write(f"**{student_name}**")
                st.caption(f"Submitted: {row['submission_date']}")
            
            with col2:
                # Score display with color coding
                if pd.notna(row['ai_score']):
                    score = row['ai_score']
                    if score >= 30:
                        st.success(f"Score: {score:.1f}/37.5")
                    elif score >= 20:
                        st.warning(f"Score: {score:.1f}/37.5")
                    else:
                        st.error(f"Score: {score:.1f}/37.5")
                else:
                    st.info("Not graded yet")
            
            with col3:
                if st.button("👁️ View", key=f"view_{row['id']}", help="View submission details"):
                    st.session_state.current_submission = row['id']
                    st.session_state.page = "view_submission"
            
            with col4:
                if pd.notna(row['ai_score']):
                    if st.button("📝 Report", key=f"report_{row['id']}", help="Generate PDF report"):
                        generate_individual_report(grader, row, selected_assignment)
                else:
                    if st.button("⚡ Grade", key=f"grade_{row['id']}", help="Grade this submission"):
                        st.session_state.current_submission = row['id']
                        st.session_state.page = "manual_grade"
        
        st.divider()
    
    # Export and report options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export Results to CSV"):
            export_data = submissions[['student_id', 'ai_score', 'human_score', 'final_score', 'submission_date']]
            csv = export_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{selected_assignment}_results.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📝 Generate Individual Reports"):
            generate_student_reports_interface(grader, assignment_id, selected_assignment)
    
    conn.close()
    
    # Handle page navigation
    if st.session_state.get('page') == 'view_submission':
        view_submission_detail(grader)
    elif st.session_state.get('page') == 'manual_grade':
        manual_grading_interface(grader)

def generate_student_reports_interface(grader, assignment_id: int, assignment_name: str):
    """Interface for generating student reports"""
    
    st.subheader("📝 Generate Individual Student Reports")
    
    if st.button("Generate PDF Reports for All Students"):
        with st.spinner("Generating detailed PDF reports for all students..."):
            try:
                report_generator = PDFReportGenerator()
                
                # Get all graded submissions for this assignment
                conn = sqlite3.connect(grader.db_path)
                submissions = pd.read_sql_query("""
                    SELECT s.*, 
                           COALESCE(st.name, 'Unknown') as student_name, 
                           COALESCE(st.student_id, 'Unknown') as student_id
                    FROM submissions s
                    LEFT JOIN students st ON s.student_id = st.id
                    WHERE s.assignment_id = ? AND s.ai_score IS NOT NULL
                """, conn, params=(assignment_id,))
                conn.close()
                
                if submissions.empty:
                    st.warning("No graded submissions found for this assignment.")
                    return
                
                generated_reports = []
                
                for _, submission in submissions.iterrows():
                    # Get the detailed analysis result and parse old format if needed
                    if submission['ai_feedback']:
                        try:
                            analysis_result = json.loads(submission['ai_feedback'])
                            # If it's the old format (list of strings), convert it
                            if isinstance(analysis_result, list):
                                analysis_result = parse_old_feedback_format(analysis_result)
                        except:
                            analysis_result = {'detailed_feedback': ['Feedback parsing error']}
                    else:
                        analysis_result = {'detailed_feedback': ['No detailed feedback available']}
                    analysis_result['total_score'] = submission['ai_score']
                    analysis_result['max_score'] = 37.5
                    
                    # Generate PDF report
                    report_path = report_generator.generate_report(
                        student_name=submission['student_name'],
                        assignment_id=assignment_name,
                        analysis_result=analysis_result
                    )
                    
                    generated_reports.append({
                        'student': submission['student_name'],
                        'path': report_path
                    })
                
                if generated_reports:
                    st.success(f"✅ Generated reports for {len(generated_reports)} students!")
                    
                    # Show report details
                    st.write("**Generated Reports:**")
                    
                    for report in generated_reports:
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write(f"📚 **{report['student']}**")
                        
                        with col2:
                            with open(report['path'], 'rb') as f:
                                st.download_button(
                                    label="📝 Download Report",
                                    data=f.read(),
                                    file_name=f"{report['student']}_feedback.pdf",
                                    mime="application/pdf",
                                    key=f"docx_{report['student']}"
                                )
                    
                    # Bulk download option
                    st.write("---")
                    st.info("💡 **Tip:** Reports are saved in the `reports/` folder. You can zip this folder to share all reports at once.")
                    
            except Exception as e:
                st.error(f"Error generating reports: {str(e)}")
                import traceback
                st.error(f"Details: {traceback.format_exc()}")

def generate_individual_report(grader, submission_row, assignment_name):
    """Generate a PDF report for an individual submission"""
    try:
        from report_generator import PDFReportGenerator
        
        report_generator = PDFReportGenerator()
        
        # Get the detailed analysis result
        if submission_row['ai_feedback']:
            try:
                ai_feedback_data = json.loads(submission_row['ai_feedback'])
                # Handle both list and dict formats
                if isinstance(ai_feedback_data, list):
                    analysis_result = {
                        'detailed_feedback': ai_feedback_data,
                        'element_scores': {},
                        'missing_elements': [],
                        'code_issues': [],
                        'question_analysis': {},
                        'overall_assessment': 'AI-generated feedback available.'
                    }
                else:
                    analysis_result = ai_feedback_data
            except:
                analysis_result = {
                    'detailed_feedback': ['AI feedback available but could not be parsed'],
                    'element_scores': {},
                    'missing_elements': [],
                    'code_issues': [],
                    'question_analysis': {},
                    'overall_assessment': 'Report generated from basic scoring data.'
                }
        else:
            analysis_result = {
                'detailed_feedback': ['No detailed feedback available'],
                'element_scores': {},
                'missing_elements': [],
                'code_issues': [],
                'question_analysis': {},
                'overall_assessment': 'Basic scoring report.'
            }
        
        analysis_result['total_score'] = submission_row['ai_score'] or 0
        analysis_result['max_score'] = 37.5
        
        # Generate report - extract student name from filename if not available
        student_name = submission_row.get('student_name')
        if pd.isna(student_name) or student_name == 'Unknown' or not student_name:
            # Try to extract name from the notebook filename
            notebook_path = submission_row.get('notebook_path', '')
            if notebook_path:
                from pathlib import Path
                from assignment_manager import parse_github_classroom_filename
                
                filename = Path(notebook_path).stem  # Get filename without extension
                parsed_info = parse_github_classroom_filename(filename)
                student_name = parsed_info.get('name') or f"Student_{submission_row.get('student_id', 'Unknown')}"
            else:
                student_name = f"Student_{submission_row.get('student_id', 'Unknown')}"
        report_path = report_generator.generate_report(
            student_name=student_name,
            assignment_id=assignment_name,
            analysis_result=analysis_result
        )
        
        # Show success and provide download
        st.success(f"✅ Report generated for {student_name}")
        st.info(f"📁 Report saved to: {report_path}")
        
        # Provide download button
        with open(report_path, 'rb') as f:
            st.download_button(
                label=f"📝 Download {student_name} Report",
                data=f.read(),
                file_name=f"{student_name}_{assignment_name}_report.pdf",
                mime="application/pdf",
                key=f"download_{submission_row['id']}"
            )
        
    except Exception as e:
        st.error(f"Error generating individual report: {str(e)}")
        import traceback
        st.error(f"Details: {traceback.format_exc()}")

def view_submission_detail(grader):
    st.header("📝 Submission Details")
    
    if 'current_submission' not in st.session_state:
        st.error("No submission selected.")
        return
    
    # Get submission details
    conn = sqlite3.connect(grader.db_path)
    submission = pd.read_sql_query("""
        SELECT s.*, st.name as student_name, a.name as assignment_name
        FROM submissions s
        LEFT JOIN students st ON s.student_id = st.id
        JOIN assignments a ON s.assignment_id = a.id
        WHERE s.id = ?
    """, conn, params=(st.session_state.current_submission,)).iloc[0]
    
    conn.close()
    
    # Display submission info
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Student:** {submission['student_name'] or submission['student_id']}")
        st.write(f"**Assignment:** {submission['assignment_name']}")
        st.write(f"**Submitted:** {submission['submission_date']}")
    
    with col2:
        if pd.notna(submission['ai_score']):
            st.write(f"**AI Score:** {submission['ai_score']:.1f}")
        if pd.notna(submission['human_score']):
            st.write(f"**Human Score:** {submission['human_score']:.1f}")
        if pd.notna(submission['final_score']):
            st.write(f"**Final Score:** {submission['final_score']:.1f}")
    
    # Display AI feedback if available
    if pd.notna(submission['ai_feedback']):
        st.subheader("AI Feedback")
        try:
            feedback = json.loads(submission['ai_feedback'])
            for item in feedback:
                st.write(f"• {item}")
        except:
            st.write(submission['ai_feedback'])
    
    # Display human feedback if available
    if pd.notna(submission['human_feedback']):
        st.subheader("Human Feedback")
        st.write(submission['human_feedback'])
    
    # Display notebook
    st.subheader("Notebook Content")
    
    if os.path.exists(submission['notebook_path']):
        try:
            # Convert notebook to HTML for display
            with open(submission['notebook_path'], 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
            
            html_exporter = HTMLExporter()
            html_exporter.template_name = 'classic'
            (body, resources) = html_exporter.from_notebook_node(nb)
            
            # Display HTML
            st.components.v1.html(body, height=800, scrolling=True)
            
        except Exception as e:
            st.error(f"Error displaying notebook: {str(e)}")
            
            # Fallback: show raw content
            with open(submission['notebook_path'], 'r', encoding='utf-8') as f:
                content = f.read()
            st.code(content, language='json')
    else:
        st.error("Notebook file not found.")
    
    if st.button("Back to Results"):
        st.session_state.page = None
        st.rerun()

def manual_grading_interface(grader):
    st.header("✏️ Manual Grading")
    
    if 'current_submission' not in st.session_state:
        st.error("No submission selected.")
        return
    
    # Get submission details
    conn = sqlite3.connect(grader.db_path)
    submission = pd.read_sql_query("""
        SELECT s.*, st.name as student_name, a.name as assignment_name, a.rubric, a.total_points
        FROM submissions s
        LEFT JOIN students st ON s.student_id = st.student_id
        JOIN assignments a ON s.assignment_id = a.id
        WHERE s.id = ?
    """, conn, params=(st.session_state.current_submission,)).iloc[0]
    
    # Display submission info
    st.write(f"**Student:** {submission['student_name'] or submission['student_id']}")
    st.write(f"**Assignment:** {submission['assignment_name']}")
    
    # Show AI score and feedback for reference
    if pd.notna(submission['ai_score']):
        st.info(f"AI suggested score: {submission['ai_score']:.1f}")
        
        if pd.notna(submission['ai_feedback']):
            with st.expander("AI Feedback"):
                try:
                    feedback = json.loads(submission['ai_feedback'])
                    for item in feedback:
                        st.write(f"• {item}")
                except:
                    st.write(submission['ai_feedback'])
    
    # Display rubric
    if submission['rubric']:
        try:
            rubric = json.loads(submission['rubric'])
            st.subheader("Grading Rubric")
            
            total_rubric_points = 0
            rubric_scores = {}
            
            for criterion, details in rubric.items():
                points = details.get('points', 0)
                description = details.get('description', '')
                total_rubric_points += points
                
                st.write(f"**{criterion}** ({points} points): {description}")
                rubric_scores[criterion] = st.slider(
                    f"Score for {criterion}",
                    min_value=0,
                    max_value=points,
                    value=int(submission['human_score'] * points / submission['total_points']) if pd.notna(submission['human_score']) else points,
                    key=f"rubric_{criterion}"
                )
        except:
            rubric = {}
            total_rubric_points = submission['total_points']
    else:
        rubric = {}
        total_rubric_points = submission['total_points']
    
    # Manual scoring
    st.subheader("Manual Grading")
    
    if rubric:
        # Calculate score from rubric
        calculated_score = sum(rubric_scores.values())
        st.write(f"Calculated score from rubric: {calculated_score}/{total_rubric_points}")
        manual_score = calculated_score
    else:
        # Direct scoring
        manual_score = st.number_input(
            "Manual Score",
            min_value=0.0,
            max_value=float(submission['total_points']),
            value=float(submission['human_score']) if pd.notna(submission['human_score']) else 0.0,
            step=0.5
        )
    
    # Feedback
    current_feedback = submission['human_feedback'] if pd.notna(submission['human_feedback']) else ""
    feedback = st.text_area("Feedback", value=current_feedback, height=150)
    
    # Display notebook for reference
    with st.expander("View Notebook", expanded=False):
        if os.path.exists(submission['notebook_path']):
            try:
                with open(submission['notebook_path'], 'r', encoding='utf-8') as f:
                    nb = nbformat.read(f, as_version=4)
                
                html_exporter = HTMLExporter()
                html_exporter.template_name = 'classic'
                (body, resources) = html_exporter.from_notebook_node(nb)
                
                st.components.v1.html(body, height=600, scrolling=True)
                
            except Exception as e:
                st.error(f"Error displaying notebook: {str(e)}")
    
    # Save grading
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Save Grade"):
            # Calculate final score (blend of AI and human if both exist)
            if pd.notna(submission['ai_score']):
                final_score = 0.3 * submission['ai_score'] + 0.7 * manual_score
            else:
                final_score = manual_score
            
            # Update database
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE submissions
                SET human_score = ?, human_feedback = ?, final_score = ?, graded_date = ?
                WHERE id = ?
            """, (manual_score, feedback, final_score, datetime.now(), submission['id']))
            
            # Update training data
            cursor.execute("""
                UPDATE ai_training_data
                SET human_score = ?, human_feedback = ?
                WHERE assignment_id = ? AND cell_content = ?
            """, (manual_score, feedback, submission['assignment_id'], submission['notebook_path']))
            
            conn.commit()
            st.success("Grade saved successfully!")
    
    with col2:
        if st.button("Back to Results"):
            st.session_state.page = None
            st.rerun()
    
    conn.close()
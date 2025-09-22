#!/usr/bin/env python3
"""
Generate PDF reports for graded homework submissions
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os
import re
from datetime import datetime
from typing import Dict, Any

class PDFReportGenerator:
    """Generate professional PDF reports for homework grading"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set up styles
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        ))
        self.styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=self.styles['Normal'],
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=6
        ))
    
    def _clean_text(self, text: str) -> str:
        """Clean text for PDF generation"""
        if not isinstance(text, str):
            text = str(text)
        
        # Remove emojis and special characters that might cause issues
        text = re.sub(r'[📋📈🗂️📦🔍📚✅❌]', '', text)
        text = text.replace('**', '')  # Remove markdown bold
        text = text.replace('*', '')   # Remove markdown italic
        
        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def generate_report(self, student_name: str, assignment_id: str, analysis_result: Dict[str, Any]) -> str:
        """Generate a PDF report for a graded submission"""
        
        # Create filename
        safe_student_name = student_name or "Unknown_Student"
        safe_name = re.sub(r'[^\w\s-]', '', safe_student_name).replace(' ', '_')
        filename = f"{safe_name}_{assignment_id}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter, topMargin=0.5*inch)
        story = []
        
        # Add content in clean, organized sections
        self._add_header(story, safe_student_name, assignment_id, analysis_result)
        self._add_score_summary(story, analysis_result)
        self._add_detailed_breakdown(story, analysis_result)
        
        # Add code fixes if there are issues
        if analysis_result.get('code_issues'):
            self._add_code_fixes(story, analysis_result)
        
        if 'question_analysis' in analysis_result:
            self._add_question_analysis(story, analysis_result['question_analysis'])
        
        self._add_recommendations(story, analysis_result)
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def _add_header(self, story, student_name: str, assignment_id: str, analysis_result: Dict[str, Any]):
        """Add report header"""
        # Title
        story.append(Paragraph("Homework Grading Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Student info table
        total_score = analysis_result.get('total_score', 0)
        max_score = analysis_result.get('max_score', 37.5)
        percentage = (total_score / max_score) * 100 if max_score > 0 else 0
        
        data = [
            ['Student Name:', self._clean_text(student_name)],
            ['Assignment:', self._clean_text(assignment_id)],
            ['Graded On:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
            ['Final Score:', f"{total_score:.1f} / {max_score} points ({percentage:.1f}%)"]
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
    
    def _add_score_summary(self, story, analysis_result: Dict[str, Any]):
        """Add score summary section"""
        story.append(Paragraph("Score Summary", self.styles['CustomHeading']))
        
        # Overall performance
        total_score = analysis_result.get('total_score', 0)
        max_score = analysis_result.get('max_score', 37.5)
        percentage = (total_score / max_score) * 100 if max_score > 0 else 0
        
        if percentage >= 90:
            performance = "Excellent"
        elif percentage >= 80:
            performance = "Good"
        elif percentage >= 70:
            performance = "Satisfactory"
        elif percentage >= 60:
            performance = "Needs Improvement"
        else:
            performance = "Unsatisfactory"
        
        story.append(Paragraph(f"<b>Overall Performance:</b> {performance} ({percentage:.1f}%)", self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Element scores breakdown
        if 'element_scores' in analysis_result:
            story.append(Paragraph("Component Scores:", self.styles['Heading2']))
            
            for element, score in analysis_result['element_scores'].items():
                element_name = element.replace('_', ' ').title()
                story.append(Paragraph(f"• {element_name}: {score:.1f} points", self.styles['CustomBullet']))
            
            story.append(Spacer(1, 12))
    
    def _add_detailed_breakdown(self, story, analysis_result: Dict[str, Any]):
        """Add clean, organized feedback breakdown"""
        
        # Performance by Category
        story.append(Paragraph("Performance by Category", self.styles['CustomHeading']))
        
        if 'element_scores' in analysis_result:
            for element, score in analysis_result['element_scores'].items():
                element_name = element.replace('_', ' ').title()
                # Create a clean score display
                if element == 'working_directory':
                    max_score = 2
                elif element == 'package_loading':
                    max_score = 4
                elif element == 'data_import':
                    max_score = 11
                elif element == 'data_inspection':
                    max_score = 8
                elif element == 'reflection_questions':
                    max_score = 12.5
                else:
                    max_score = 5
                
                percentage = (score / max_score) * 100 if max_score > 0 else 0
                
                if percentage >= 90:
                    status = "✅ Excellent"
                elif percentage >= 80:
                    status = "✅ Good"
                elif percentage >= 70:
                    status = "⚠️ Satisfactory"
                else:
                    status = "❌ Needs Work"
                
                story.append(Paragraph(f"{status} <b>{element_name}:</b> {score:.1f}/{max_score} points ({percentage:.0f}%)", self.styles['Normal']))
        
        story.append(Spacer(1, 20))
    
    def _add_code_fixes(self, story, analysis_result: Dict[str, Any]):
        """Add clean, actionable code fixes"""
        story.append(Paragraph("Code Issues & Fixes", self.styles['CustomHeading']))
        
        code_issues = analysis_result.get('code_issues', [])
        
        # Group similar issues
        file_issues = [issue for issue in code_issues if 'does not exist' in issue.lower()]
        variable_issues = [issue for issue in code_issues if 'not found' in issue.lower()]
        
        if file_issues:
            story.append(Paragraph("<b>📁 File Path Issues:</b>", self.styles['Heading2']))
            story.append(Paragraph("Your code is looking for data files in the wrong location. Here's how to fix it:", self.styles['Normal']))
            story.append(Spacer(1, 6))
            
            # Provide clean solution
            fix_text = """<b>Solution:</b><br/>
            1. Make sure your data files are in a 'data' folder<br/>
            2. Use these exact file paths:<br/>
            • sales_df &lt;- read_csv("data/sales_data.csv")<br/>
            • ratings_df &lt;- read_excel("data/ratings_data.xlsx", sheet = "ratings")<br/>
            • comments_df &lt;- read_excel("data/ratings_data.xlsx", sheet = "comments")"""
            
            story.append(Paragraph(fix_text, self.styles['Normal']))
            story.append(Spacer(1, 12))
        
        if variable_issues:
            story.append(Paragraph("<b>🔧 Variable Issues:</b>", self.styles['Heading2']))
            story.append(Paragraph("You're trying to use variables before creating them. Run your code cells in order from top to bottom.", self.styles['Normal']))
            story.append(Spacer(1, 12))
        
        story.append(Spacer(1, 12))
    
    def _add_question_analysis(self, story, question_analysis: Dict[str, Any]):
        """Add clean reflection questions analysis"""
        story.append(Paragraph("Reflection Questions Feedback", self.styles['CustomHeading']))
        
        for q_key, q_data in question_analysis.items():
            question_title = q_key.replace('_', ' ').title()
            
            # Question header with score
            score_text = f"<b>{question_title}:</b> {q_data['score']:.1f}/{q_data['max_score']} points ({q_data['quality']})"
            story.append(Paragraph(score_text, self.styles['Heading2']))
            
            # Clean feedback only (remove "What I'm looking for" sections)
            if q_data.get('detailed_feedback'):
                feedback = self._clean_text(q_data['detailed_feedback'])
                # Extract only the personalized feedback, not the template text
                feedback_lines = feedback.split('\n')
                clean_lines = []
                skip_template = False
                
                for line in feedback_lines:
                    if "What I'm looking for:" in line or "What to focus on:" in line:
                        skip_template = True
                        continue
                    if not skip_template and line.strip():
                        clean_lines.append(line.strip())
                
                if clean_lines:
                    story.append(Paragraph(' '.join(clean_lines), self.styles['Normal']))
            
            story.append(Spacer(1, 12))
    
    def _add_recommendations(self, story, analysis_result: Dict[str, Any]):
        """Add clean recommendations section"""
        story.append(Paragraph("Next Steps", self.styles['CustomHeading']))
        
        # Clean overall assessment (remove AI debugging text)
        if 'overall_assessment' in analysis_result:
            assessment = self._clean_text(analysis_result['overall_assessment'])
            # Remove AI debugging sections
            assessment_lines = assessment.split('\n')
            clean_lines = []
            skip_ai_section = False
            
            for line in assessment_lines:
                if any(ai_term in line.lower() for ai_term in ['ai enhancement', 'ai analysis', 'ai-generated', 'we need to']):
                    skip_ai_section = True
                    continue
                if not skip_ai_section and line.strip() and not line.startswith('■'):
                    clean_lines.append(line.strip())
            
            if clean_lines:
                clean_assessment = ' '.join(clean_lines)
                story.append(Paragraph(clean_assessment, self.styles['Normal']))
                story.append(Spacer(1, 12))
        
        # Study tips based on performance
        total_score = analysis_result.get('total_score', 0)
        max_score = analysis_result.get('max_score', 37.5)
        percentage = (total_score / max_score) * 100 if max_score > 0 else 0
        
        story.append(Paragraph("Study Tips:", self.styles['Heading2']))
        
        if percentage < 70:
            tips = [
                "Review the lecture notebook and practice running the examples yourself",
                "Make sure to execute all code cells and check for outputs",
                "Focus on understanding the fundamental concepts before moving to advanced topics"
            ]
        elif percentage < 85:
            tips = [
                "Good foundation! Focus on providing more detailed explanations in reflection questions",
                "Practice connecting technical concepts to business applications"
            ]
        else:
            tips = [
                "Excellent work! Consider exploring additional data analysis techniques",
                "Try applying these concepts to your own datasets"
            ]
        
        for tip in tips:
            story.append(Paragraph(f"• {tip}", self.styles['CustomBullet']))
        
        # Clean footer
        story.append(Spacer(1, 20))
        footer_style = ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        story.append(Paragraph("Generated by AI-Powered Homework Grader", footer_style))
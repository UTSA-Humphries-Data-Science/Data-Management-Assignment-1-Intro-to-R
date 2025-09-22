#!/usr/bin/env python3
"""
Detailed homework analyzer that provides specific feedback on what worked and what didn't
"""

import nbformat
import re
import json
from typing import Dict, List, Tuple, Any

class DetailedHomeworkAnalyzer:
    def __init__(self):
        self.required_elements = {
            'working_directory': {
                'function': 'getwd()',
                'description': 'Check current working directory',
                'points': 2
            },
            'package_loading': {
                'functions': ['library(tidyverse)', 'library(readxl)'],
                'description': 'Load required packages',
                'points': 4
            },
            'csv_import': {
                'variable': 'sales_df',
                'function': 'read_csv',
                'description': 'Import CSV data into sales_df',
                'points': 5
            },
            'excel_import': {
                'variables': ['ratings_df', 'comments_df'],
                'function': 'read_excel',
                'description': 'Import Excel data into ratings_df and comments_df',
                'points': 6
            },
            'data_inspection': {
                'functions': ['head()', 'str()', 'summary()'],
                'description': 'Perform data inspection on all datasets',
                'points': 8
            },
            'reflection_questions': {
                'questions': [
                    'Data Types Analysis',
                    'Data Quality Assessment', 
                    'Analysis Readiness'
                ],
                'description': 'Answer reflection questions with thoughtful responses',
                'points': 12.5
            }
        }
    
    def analyze_notebook(self, notebook_path: str) -> Dict[str, Any]:
        """Perform detailed analysis of student notebook"""
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
            
            # Execute notebook to capture real errors and outputs
            executed_nb = self._execute_notebook_safely(nb, notebook_path)
            
            analysis = {
                'total_score': 0,
                'max_score': 37.5,
                'detailed_feedback': [],
                'element_scores': {},
                'missing_elements': [],
                'code_issues': [],
                'question_analysis': {},
                'overall_assessment': '',
                'student_info': self._extract_student_info(nb),
                'execution_attempted': True
            }
            
            # Extract all code and markdown content from executed notebook
            code_cells = []
            markdown_cells = []
            
            for cell in executed_nb.cells:
                if cell.cell_type == 'code':
                    code_cells.append({
                        'source': cell.source,
                        'outputs': cell.get('outputs', [])
                    })
                elif cell.cell_type == 'markdown':
                    markdown_cells.append(cell.source)
            
            # Analyze each required element
            analysis = self._analyze_working_directory(code_cells, analysis)
            analysis = self._analyze_package_loading(code_cells, analysis)
            analysis = self._analyze_data_import(code_cells, analysis)
            analysis = self._analyze_data_inspection(code_cells, analysis)
            analysis = self._analyze_reflection_questions(markdown_cells, analysis)
            
            # Generate overall assessment
            analysis['overall_assessment'] = self._generate_overall_assessment(analysis)
            
            return analysis
            
        except Exception as e:
            return {
                'total_score': 0,
                'max_score': 37.5,
                'detailed_feedback': [f"❌ Error analyzing notebook: {str(e)}"],
                'element_scores': {},
                'missing_elements': ['All elements - notebook could not be analyzed'],
                'code_issues': [f"Notebook analysis failed: {str(e)}"],
                'question_analysis': {},
                'overall_assessment': 'Notebook could not be analyzed due to technical issues.'
            }
    
    def _analyze_working_directory(self, code_cells: List[Dict], analysis: Dict) -> Dict:
        """Check if student used getwd() to check working directory"""
        found_getwd = False
        has_output = False
        was_executed = False
        
        for cell in code_cells:
            if 'getwd()' in cell['source'] or 'getwd(' in cell['source']:
                found_getwd = True
                # More flexible execution detection
                if cell['outputs'] and len(cell['outputs']) > 0:
                    has_output = True
                    was_executed = True  # If there's output, it was executed
                # Also check execution_count as backup
                execution_count = cell.get('execution_count')
                if execution_count is not None and str(execution_count).isdigit():
                    was_executed = True
                break
        
        if found_getwd and has_output and was_executed:
            score = 2
            feedback = "✅ **Working Directory (2/2 points)**: Correctly used getwd() and showed output"
        elif found_getwd and was_executed:
            score = 1.5
            feedback = "👍 **Working Directory (1.5/2 points)**: Used getwd() and ran the cell - output may not be visible in this format"
        elif found_getwd:
            score = 0.5
            feedback = "⚠️ **Working Directory (0.5/2 points)**: Code is there but you need to RUN the cell to see the output"
        else:
            score = 0
            feedback = "❌ **Working Directory (0/2 points)**: Missing getwd() function call"
            analysis['missing_elements'].append("getwd() function call")
        
        analysis['total_score'] += score
        analysis['element_scores']['working_directory'] = score
        analysis['detailed_feedback'].append(feedback)
        
        return analysis
    
    def _analyze_package_loading(self, code_cells: List[Dict], analysis: Dict) -> Dict:
        """Check if required packages are loaded"""
        tidyverse_status = {'found': False, 'executed': False, 'error': False}
        readxl_status = {'found': False, 'executed': False, 'error': False}
        
        # Check each cell for package loading
        for cell in code_cells:
            cell_source = cell['source']
            # More flexible execution detection
            was_executed = False
            if cell['outputs'] and len(cell['outputs']) > 0:
                was_executed = True
            else:
                execution_count = cell.get('execution_count')
                if execution_count is not None and str(execution_count).isdigit():
                    was_executed = True
            
            # Check for tidyverse
            if re.search(r'library\s*\(\s*tidyverse\s*\)', cell_source):
                tidyverse_status['found'] = True
                if was_executed:
                    tidyverse_status['executed'] = True
                
                # Check for errors in outputs
                for output in cell.get('outputs', []):
                    if output.get('output_type') == 'error':
                        tidyverse_status['error'] = True
            
            # Check for readxl
            if re.search(r'library\s*\(\s*readxl\s*\)', cell_source):
                readxl_status['found'] = True
                if was_executed:
                    readxl_status['executed'] = True
                
                # Check for errors in outputs
                for output in cell.get('outputs', []):
                    if output.get('output_type') == 'error':
                        readxl_status['error'] = True
        
        score = 0
        feedback_parts = []
        
        # Score tidyverse
        if tidyverse_status['executed'] and not tidyverse_status['error']:
            score += 2
            feedback_parts.append("✅ tidyverse loaded and executed successfully")
        elif tidyverse_status['found'] and not tidyverse_status['executed']:
            score += 1
            feedback_parts.append("⚠️ tidyverse code written but not executed")
        elif tidyverse_status['executed'] and tidyverse_status['error']:
            score += 0.5
            feedback_parts.append("⚠️ tidyverse attempted but has errors")
            analysis['code_issues'].append("tidyverse loading error")
        elif tidyverse_status['found']:
            score += 0.5
            feedback_parts.append("⚠️ tidyverse code present but not run")
        else:
            feedback_parts.append("❌ tidyverse not loaded")
            analysis['missing_elements'].append("library(tidyverse)")
        
        # Score readxl
        if readxl_status['executed'] and not readxl_status['error']:
            score += 2
            feedback_parts.append("✅ readxl loaded and executed successfully")
        elif readxl_status['found'] and not readxl_status['executed']:
            score += 1
            feedback_parts.append("⚠️ readxl code written but not executed")
        elif readxl_status['executed'] and readxl_status['error']:
            score += 0.5
            feedback_parts.append("⚠️ readxl attempted but has errors")
            analysis['code_issues'].append("readxl loading error")
        elif readxl_status['found']:
            score += 0.5
            feedback_parts.append("⚠️ readxl code present but not run")
        else:
            feedback_parts.append("❌ readxl not loaded")
            analysis['missing_elements'].append("library(readxl)")
        
        feedback = f"📦 **Package Loading ({score}/4 points)**: " + " | ".join(feedback_parts)
        
        analysis['total_score'] += score
        analysis['element_scores']['package_loading'] = score
        analysis['detailed_feedback'].append(feedback)
        
        return analysis
    
    def _analyze_data_import(self, code_cells: List[Dict], analysis: Dict) -> Dict:
        """Check if data import was done correctly"""
        all_code = '\n'.join([cell['source'] for cell in code_cells])
        
        # Check CSV import
        csv_score = 0
        csv_feedback = []
        
        if 'sales_df' in all_code and 'read_csv' in all_code:
            csv_score += 3
            csv_feedback.append("✅ sales_df variable created with read_csv")
            
            # Check if correct file path is used
            if 'sales_data.csv' in all_code:
                csv_score += 2
                csv_feedback.append("✅ Correct filename (sales_data.csv)")
            else:
                csv_feedback.append("⚠️ Filename may be incorrect")
        else:
            csv_feedback.append("❌ Missing sales_df <- read_csv() assignment")
            analysis['missing_elements'].append("sales_df data import")
        
        # Check Excel import
        excel_score = 0
        excel_feedback = []
        
        ratings_found = 'ratings_df' in all_code and 'read_excel' in all_code
        comments_found = 'comments_df' in all_code and 'read_excel' in all_code
        
        if ratings_found:
            excel_score += 3
            excel_feedback.append("✅ ratings_df created with read_excel")
        else:
            excel_feedback.append("❌ Missing ratings_df import")
            analysis['missing_elements'].append("ratings_df data import")
        
        if comments_found:
            excel_score += 3
            excel_feedback.append("✅ comments_df created with read_excel")
        else:
            excel_feedback.append("❌ Missing comments_df import")
            analysis['missing_elements'].append("comments_df data import")
        
        total_import_score = csv_score + excel_score
        
        csv_feedback_str = f"📄 **CSV Import ({csv_score}/5 points)**: " + " | ".join(csv_feedback)
        excel_feedback_str = f"📊 **Excel Import ({excel_score}/6 points)**: " + " | ".join(excel_feedback)
        
        analysis['total_score'] += total_import_score
        analysis['element_scores']['data_import'] = total_import_score
        analysis['detailed_feedback'].extend([csv_feedback_str, excel_feedback_str])
        
        return analysis
    
    def _analyze_data_inspection(self, code_cells: List[Dict], analysis: Dict) -> Dict:
        """Check if proper data inspection was performed"""
        all_code = '\n'.join([cell['source'] for cell in code_cells])
        
        # Required functions
        functions_to_check = ['head(', 'str(', 'summary(']
        datasets_to_check = ['sales_df', 'ratings_df', 'comments_df']
        
        score = 0
        feedback_parts = []
        executed_functions = []
        
        # Check for errors in code execution
        self._detect_code_errors(code_cells, analysis)
        
        # Check each function usage and execution
        for func in functions_to_check:
            func_found = False
            func_executed = False
            
            for cell in code_cells:
                if func in cell['source']:
                    func_found = True
                    # More flexible execution detection
                    if cell['outputs'] and len(cell['outputs']) > 0:
                        func_executed = True
                        executed_functions.append(func[:-1])
                    else:
                        execution_count = cell.get('execution_count')
                        if execution_count is not None and str(execution_count).isdigit():
                            func_executed = True
                            executed_functions.append(func[:-1])
                    break
            
            if func_executed:
                score += 2
                feedback_parts.append(f"✅ {func[:-1]}() used and executed")
            elif func_found:
                score += 0.5
                feedback_parts.append(f"⚠️ {func[:-1]}() code written but not executed")
            else:
                feedback_parts.append(f"❌ {func[:-1]}() missing")
                analysis['missing_elements'].append(f"{func[:-1]}() function")
        
        # Check dataset coverage - be more specific about what was actually done
        datasets_analyzed = {
            'sales_df': {'found': False, 'executed': False},
            'ratings_df': {'found': False, 'executed': False}, 
            'comments_df': {'found': False, 'executed': False}
        }
        
        for cell in code_cells:
            cell_source = cell['source']
            # More flexible execution detection
            was_executed = False
            if cell['outputs'] and len(cell['outputs']) > 0:
                was_executed = True
            else:
                execution_count = cell.get('execution_count')
                if execution_count is not None and str(execution_count).isdigit():
                    was_executed = True
            
            for dataset in datasets_to_check:
                if dataset in cell_source and any(func in cell_source for func in functions_to_check):
                    datasets_analyzed[dataset]['found'] = True
                    if was_executed:
                        datasets_analyzed[dataset]['executed'] = True
        
        # Score based on actual execution
        for dataset, status in datasets_analyzed.items():
            if status['executed']:
                score += 1
                feedback_parts.append(f"✅ {dataset} properly analyzed")
            elif status['found']:
                score += 0.3
                feedback_parts.append(f"⚠️ {dataset} code written but not run")
            else:
                feedback_parts.append(f"❌ {dataset} not analyzed")
        
        score = min(8, score)  # Cap at 8 points
        
        # Add specific guidance based on what's missing
        if len(executed_functions) == 0:
            feedback_parts.append("💡 Remember to RUN your code cells to see the outputs!")
        elif len(executed_functions) < 3:
            feedback_parts.append("💡 Make sure to run ALL inspection functions (head, str, summary)")
        
        feedback = f"🔍 **Data Inspection ({score:.1f}/8 points)**: " + " | ".join(feedback_parts)
        
        analysis['total_score'] += score
        analysis['element_scores']['data_inspection'] = score
        analysis['detailed_feedback'].append(feedback)
        
        return analysis
    
    def _analyze_reflection_questions(self, markdown_cells: List[str], analysis: Dict) -> Dict:
        """Analyze answers to reflection questions with detailed professor feedback"""
        all_markdown = '\n'.join(markdown_cells)
        all_markdown_lower = all_markdown.lower()
        
        # Extract actual student responses for each question
        question_responses = self._extract_question_responses(all_markdown)
        
        questions = {
            'data_types': {
                'keywords': ['data type', 'date', 'amount', 'character', 'numeric', 'integer', 'appropriate', 'business', 'analytics'],
                'advanced_keywords': ['datetime', 'factor', 'categorical', 'continuous', 'discrete', 'format', 'conversion'],
                'title': 'Data Types Analysis',
                'points': 4,
                'question_text': 'data types analysis'
            },
            'data_quality': {
                'keywords': ['missing', 'quality', 'unusual', 'pattern', 'issue', 'problem', 'clean', 'null', 'na'],
                'advanced_keywords': ['outlier', 'inconsistent', 'duplicate', 'validation', 'integrity', 'standardization'],
                'title': 'Data Quality Assessment', 
                'points': 4,
                'question_text': 'data quality assessment'
            },
            'analysis_readiness': {
                'keywords': ['ready', 'analysis', 'preprocessing', 'prepare', 'clean', 'dataset', 'transform'],
                'advanced_keywords': ['normalization', 'aggregation', 'join', 'merge', 'pivot', 'reshape'],
                'title': 'Analysis Readiness',
                'points': 4.5,
                'question_text': 'analysis readiness'
            }
        }
        
        total_question_score = 0
        question_feedback = []
        
        for q_key, q_info in questions.items():
            # Find the specific response for this question
            response = question_responses.get(q_key, "")
            response_lower = response.lower()
            
            if response and len(response.strip()) > 15:  # Has some content
                response_lower = response.lower()
                
                # Analyze response quality
                score, quality, detailed_feedback = self._analyze_single_question(
                    q_key, response, response_lower, q_info
                )
                
                question_feedback.append(f"📝 **{q_info['title']}** ({score:.1f}/{q_info['points']} points)")
                question_feedback.append(detailed_feedback)
                
                analysis['question_analysis'][q_key] = {
                    'score': score,
                    'max_score': q_info['points'],
                    'quality': quality,
                    'response_text': response[:200] + "..." if len(response) > 200 else response,
                    'detailed_feedback': detailed_feedback
                }
                
            else:
                score = 0
                quality = 'Missing'
                
                # Provide specific guidance for missing responses
                missing_feedback = self._get_missing_question_guidance(q_key)
                question_feedback.append(f"❌ **{q_info['title']}** (0/{q_info['points']} points)")
                question_feedback.append(missing_feedback)
                
                analysis['missing_elements'].append(f"{q_info['title']} response")
                analysis['question_analysis'][q_key] = {
                    'score': 0,
                    'max_score': q_info['points'],
                    'quality': 'Missing',
                    'response_text': '',
                    'detailed_feedback': missing_feedback
                }
            
            total_question_score += score
        
        # Add overall reflection feedback
        overall_feedback = self._generate_reflection_overview(analysis['question_analysis'])
        question_feedback.append("")
        question_feedback.append(overall_feedback)
        
        feedback = f"💭 **Reflection Questions ({total_question_score:.1f}/12.5 points)**:\n" + "\n".join([f"   {fb}" for fb in question_feedback])
        
        analysis['total_score'] += total_question_score
        analysis['element_scores']['reflection_questions'] = total_question_score
        analysis['detailed_feedback'].append(feedback)
        
        return analysis
    
    def _extract_question_responses(self, markdown_text: str) -> Dict[str, str]:
        """Extract student responses to specific questions using flexible patterns"""
        responses = {}
        
        # Split markdown into sections and look for question-answer patterns
        sections = re.split(r'(?:^|\n)#{1,4}\s+', markdown_text, flags=re.MULTILINE)
        
        # More flexible patterns to find questions and answers
        question_indicators = {
            'data_types': [
                'data type', 'date', 'amount', 'column', 'appropriate', 'business analytics'
            ],
            'data_quality': [
                'data quality', 'quality', 'missing', 'issue', 'problem', 'unusual', 'pattern'
            ],
            'analysis_readiness': [
                'analysis readiness', 'ready', 'preprocessing', 'prepare', 'dataset', 'most ready'
            ]
        }
        
        # Look through all markdown content for responses
        for section in sections:
            section_lower = section.lower()
            
            # Check each question type
            for q_key, indicators in question_indicators.items():
                if q_key in responses:  # Already found this question
                    continue
                
                # Check if this section contains question indicators
                indicator_matches = sum(1 for indicator in indicators if indicator in section_lower)
                
                if indicator_matches >= 2:  # At least 2 indicators suggest this is the right question
                    # Look for answer patterns
                    answer_patterns = [
                        r'answer[:\s]+(.*?)(?=\n\n|\*\*|###|$)',
                        r'response[:\s]+(.*?)(?=\n\n|\*\*|###|$)',
                        r'your answer[:\s]+(.*?)(?=\n\n|\*\*|###|$)',
                        r'\[.*?\](.*?)(?=\n\n|\*\*|###|$)',  # Text after [placeholder]
                        r'(?:question \d+|analysis|assessment).*?\n\n(.*?)(?=\n\n|\*\*|###|$)'
                    ]
                    
                    for pattern in answer_patterns:
                        match = re.search(pattern, section, re.IGNORECASE | re.DOTALL)
                        if match:
                            response = match.group(1).strip()
                            # Clean up the response
                            response = re.sub(r'^\[.*?\]', '', response).strip()  # Remove placeholder brackets
                            response = re.sub(r'^[:\-\s]+', '', response).strip()  # Remove leading punctuation
                            
                            if len(response) > 15 and not self._is_placeholder_text(response):
                                responses[q_key] = response
                                break
        
        # Fallback: look for any substantial text after question keywords
        if len(responses) < 3:
            self._fallback_question_extraction(markdown_text, responses, question_indicators)
        
        return responses
    
    def _is_placeholder_text(self, text: str) -> bool:
        """Check if text is placeholder/template text"""
        text_lower = text.lower()
        placeholders = [
            'write your response here', 'your answer here', 'add your', 'todo',
            'write your', 'insert your', 'fill in', 'complete this',
            '[write', '[your', '[add', '[insert'
        ]
        return any(placeholder in text_lower for placeholder in placeholders)
    
    def _fallback_question_extraction(self, markdown_text: str, responses: Dict[str, str], question_indicators: Dict[str, List[str]]) -> None:
        """Fallback method to extract responses using broader patterns"""
        
        # Split by common separators and look for substantial text blocks
        text_blocks = re.split(r'\n\s*\n|\*\*.*?\*\*|#{1,4}', markdown_text)
        
        for block in text_blocks:
            block = block.strip()
            if len(block) < 20 or self._is_placeholder_text(block):
                continue
            
            block_lower = block.lower()
            
            # Try to match this block to a question type
            for q_key, indicators in question_indicators.items():
                if q_key in responses:  # Already found
                    continue
                
                # Count indicator matches
                matches = sum(1 for indicator in indicators if indicator in block_lower)
                
                # If we find relevant keywords and substantial content, consider it a response
                if matches >= 1 and len(block) > 30:
                    # Check if it looks like an answer (not just the question)
                    answer_indicators = ['because', 'since', 'the', 'this', 'these', 'i think', 'i believe', 'appears', 'seems']
                    if any(indicator in block_lower for indicator in answer_indicators):
                        responses[q_key] = block
    
    def _analyze_single_question(self, q_key: str, response: str, response_lower: str, q_info: Dict) -> Tuple[float, str, str]:
        """Analyze a single reflection question response"""
        
        # Count keywords
        basic_keywords = sum(1 for keyword in q_info['keywords'] if keyword in response_lower)
        advanced_keywords = sum(1 for keyword in q_info.get('advanced_keywords', []) if keyword in response_lower)
        
        # Check for placeholder text
        has_placeholder = any(placeholder in response_lower for placeholder in [
            '[write your response here]', '[your answer here]', 'todo', 'add your', 'write your response'
        ])
        
        # Analyze response length and depth
        word_count = len(response.split())
        sentence_count = len([s for s in response.split('.') if s.strip()])
        
        if has_placeholder:
            return 0.5, "Incomplete", "⚠️ Please replace the placeholder text with your own analysis."
        
        # Question-specific analysis
        if q_key == 'data_types':
            return self._analyze_data_types_response(response, response_lower, basic_keywords, advanced_keywords, word_count, q_info['points'])
        elif q_key == 'data_quality':
            return self._analyze_data_quality_response(response, response_lower, basic_keywords, advanced_keywords, word_count, q_info['points'])
        elif q_key == 'analysis_readiness':
            return self._analyze_analysis_readiness_response(response, response_lower, basic_keywords, advanced_keywords, word_count, q_info['points'])
        
        return 0, "Unknown", "Unable to analyze this response."
    
    def _analyze_data_types_response(self, response: str, response_lower: str, basic_keywords: int, advanced_keywords: int, word_count: int, max_points: float) -> Tuple[float, str, str]:
        """Analyze data types question response"""
        
        # Check for specific concepts
        mentions_date = any(term in response_lower for term in ['date', 'datetime', 'time'])
        mentions_amount = any(term in response_lower for term in ['amount', 'numeric', 'number', 'currency', 'dollar'])
        discusses_appropriateness = any(term in response_lower for term in ['appropriate', 'suitable', 'good', 'bad', 'better', 'should'])
        mentions_business_context = any(term in response_lower for term in ['business', 'analytics', 'analysis', 'calculation', 'report'])
        
        score = 0
        feedback_parts = []
        
        # Base scoring - more generous for basic responses
        if mentions_date and mentions_amount:
            score += max_points * 0.4
            feedback_parts.append("✅ Great - you identified both Date and Amount columns")
        elif mentions_date or mentions_amount:
            score += max_points * 0.25
            feedback_parts.append("👍 Good start - you mentioned data types, but try to discuss both Date and Amount columns")
        else:
            # Still give some credit if they show any understanding of data types
            if basic_keywords >= 1:
                score += max_points * 0.15
                feedback_parts.append("👍 You're thinking about data types - now focus on the specific Date and Amount columns")
            else:
                feedback_parts.append("💡 Focus on the Date and Amount columns from sales_df - what data types are they?")
        
        # Appropriateness discussion - more generous
        if discusses_appropriateness and mentions_business_context:
            score += max_points * 0.4
            feedback_parts.append("✅ Excellent - you connected data types to business analytics!")
        elif discusses_appropriateness:
            score += max_points * 0.3
            feedback_parts.append("✅ Good thinking about appropriateness - try connecting this to business needs")
        elif mentions_business_context:
            score += max_points * 0.2
            feedback_parts.append("👍 Nice business context - now discuss if the data types support your analysis goals")
        else:
            feedback_parts.append("💡 Think about this: can you do math with these data types? Can you sort dates chronologically?")
        
        # Effort and engagement - reward any substantial attempt
        if word_count >= 40:
            score += max_points * 0.2
            feedback_parts.append("✅ Good detail in your response")
        elif word_count >= 20:
            score += max_points * 0.15
            feedback_parts.append("👍 Nice effort - you could expand a bit more")
        elif word_count >= 10:
            score += max_points * 0.1
            feedback_parts.append("👍 You answered the question - try adding more detail next time")
        
        # Quality assessment
        if score >= max_points * 0.9:
            quality = "Excellent"
        elif score >= max_points * 0.7:
            quality = "Good"
        elif score >= max_points * 0.5:
            quality = "Satisfactory"
        else:
            quality = "Needs Improvement"
        
        # Detailed feedback without professor label
        professor_feedback = f"""
   {' | '.join(feedback_parts)}
   
   **What I'm looking for:** Data types matter more than you might think. If your dates are stored as text ("2023-01-15"), you can't calculate time differences or trends. If amounts have dollar signs ("$1,234.56"), you can't do math with them. 
   
   When I see dates stored properly as date objects, I know you can calculate things like "days between orders" or "monthly sales patterns." When amounts are numeric (1234.56), you can sum, average, and analyze them. 
   
   This isn't just technical nitpicking - it's about what analysis you can actually do with your data. Check this first, always. It'll save you headaches later."""
        
        return min(score, max_points), quality, professor_feedback.strip()
    
    def _analyze_data_quality_response(self, response: str, response_lower: str, basic_keywords: int, advanced_keywords: int, word_count: int, max_points: float) -> Tuple[float, str, str]:
        """Analyze data quality question response"""
        
        # Check for specific quality concepts
        mentions_missing = any(term in response_lower for term in ['missing', 'null', 'na', 'blank', 'empty'])
        mentions_patterns = any(term in response_lower for term in ['pattern', 'unusual', 'strange', 'consistent', 'inconsistent'])
        mentions_specific_issues = any(term in response_lower for term in ['duplicate', 'outlier', 'error', 'format', 'spelling'])
        discusses_impact = any(term in response_lower for term in ['impact', 'affect', 'problem', 'issue', 'concern'])
        
        score = 0
        feedback_parts = []
        
        # Issue identification - more generous scoring
        if mentions_missing and (mentions_patterns or mentions_specific_issues):
            score += max_points * 0.5
            feedback_parts.append("✅ Excellent - you identified multiple types of data quality issues")
        elif mentions_missing or mentions_patterns or mentions_specific_issues:
            score += max_points * 0.35
            feedback_parts.append("✅ Good job identifying quality issues")
        elif basic_keywords >= 1:
            score += max_points * 0.2
            feedback_parts.append("👍 You're thinking about data quality - try to be more specific about what issues you see")
        else:
            feedback_parts.append("💡 Look at your data outputs - do you see any missing values (NA's) or unusual patterns?")
        
        # Impact discussion - reward any analytical thinking
        if discusses_impact:
            score += max_points * 0.3
            feedback_parts.append("✅ Great analytical thinking about impact on analysis")
        elif any(word in response_lower for word in ['analysis', 'problem', 'issue', 'affect']):
            score += max_points * 0.2
            feedback_parts.append("👍 You're thinking analytically - expand on how these issues affect analysis")
        else:
            feedback_parts.append("💡 Think about this: how would missing data or errors affect your business conclusions?")
        
        # Effort and engagement
        if word_count >= 30:
            score += max_points * 0.2
            feedback_parts.append("✅ Good detail in your assessment")
        elif word_count >= 15:
            score += max_points * 0.15
            feedback_parts.append("👍 Nice response - you could add more specific examples")
        elif word_count >= 8:
            score += max_points * 0.1
            feedback_parts.append("👍 You addressed the question - try expanding your observations")
        
        # Quality assessment
        if score >= max_points * 0.9:
            quality = "Excellent"
        elif score >= max_points * 0.7:
            quality = "Good"
        elif score >= max_points * 0.5:
            quality = "Satisfactory"
        else:
            quality = "Needs Improvement"
        
        professor_feedback = f"""
   {' | '.join(feedback_parts)}
   
   **What I'm looking for:** Look for problems that will mess up your analysis. Missing values can throw off your totals. Inconsistent formatting (like "North" vs "NORTH" vs "north") will split your data when you try to group it. 
   
   Watch for things that don't make business sense - negative sales amounts, future dates, or someone buying 999,999 keyboards (probably a data entry error). 
   
   I also want to see you think about impact. If 5% of values are missing, that's different from 50% missing. If you have weird outliers, will they skew your averages? 
   
   This isn't busy work - bad data leads to bad decisions. Spend time here and your analysis will be much more reliable."""
        
        return min(score, max_points), quality, professor_feedback.strip()
    
    def _analyze_analysis_readiness_response(self, response: str, response_lower: str, basic_keywords: int, advanced_keywords: int, word_count: int, max_points: float) -> Tuple[float, str, str]:
        """Analyze analysis readiness question response"""
        
        # Check for readiness concepts
        compares_datasets = any(term in response_lower for term in ['compare', 'versus', 'vs', 'between', 'different'])
        mentions_preprocessing = any(term in response_lower for term in ['clean', 'prepare', 'process', 'transform', 'fix'])
        provides_reasoning = any(term in response_lower for term in ['because', 'since', 'due to', 'reason', 'therefore'])
        mentions_specific_steps = any(term in response_lower for term in ['first', 'next', 'then', 'step', 'need to'])
        
        score = 0
        feedback_parts = []
        
        # Dataset comparison - reward any comparison attempt
        if compares_datasets and provides_reasoning:
            score += max_points * 0.45
            feedback_parts.append("✅ Excellent - you compared datasets and explained your reasoning")
        elif compares_datasets:
            score += max_points * 0.3
            feedback_parts.append("✅ Good job comparing datasets - try explaining WHY one is more ready")
        elif any(dataset in response_lower for dataset in ['sales', 'rating', 'comment', 'dataset']):
            score += max_points * 0.2
            feedback_parts.append("👍 You mentioned the datasets - now compare which is most ready for analysis")
        else:
            feedback_parts.append("💡 Compare the three datasets (sales_df, ratings_df, comments_df) - which looks cleanest?")
        
        # Preprocessing awareness - reward analytical thinking
        if mentions_preprocessing and mentions_specific_steps:
            score += max_points * 0.35
            feedback_parts.append("✅ Excellent understanding of data preparation needs")
        elif mentions_preprocessing:
            score += max_points * 0.25
            feedback_parts.append("✅ Good - you understand data needs preparation")
        elif any(word in response_lower for word in ['clean', 'fix', 'prepare', 'ready']):
            score += max_points * 0.15
            feedback_parts.append("👍 You're thinking about data preparation - what specific steps are needed?")
        else:
            feedback_parts.append("💡 Think about what you'd need to do to make the messiest dataset analysis-ready")
        
        # Effort and reasoning
        if word_count >= 40:
            score += max_points * 0.2
            feedback_parts.append("✅ Thoughtful and detailed response")
        elif word_count >= 20:
            score += max_points * 0.15
            feedback_parts.append("✅ Good effort - nice reasoning")
        elif word_count >= 10:
            score += max_points * 0.1
            feedback_parts.append("👍 You answered thoughtfully - could expand a bit more")
        
        # Quality assessment
        if score >= max_points * 0.9:
            quality = "Excellent"
        elif score >= max_points * 0.7:
            quality = "Good"
        elif score >= max_points * 0.5:
            quality = "Satisfactory"
        else:
            quality = "Needs Improvement"
        
        professor_feedback = f"""
   {' | '.join(feedback_parts)}
   
   **What I'm looking for:** Compare the datasets and tell me which one you'd start analyzing first. Think practically - which has fewer missing values? Which has cleaner, more consistent formatting? Which one can answer your most important business questions?
   
   For example, if your sales data is mostly complete but your feedback data has lots of gaps and messy text, you'd probably start with sales data to get quick insights, then clean up the feedback data later.
   
   In real work, you rarely get perfect data. You have to prioritize where to spend your time. Show me you can think strategically about this - it's a key skill."""
        
        return min(score, max_points), quality, professor_feedback.strip()
    
    def _get_missing_question_guidance(self, q_key: str) -> str:
        """Provide specific guidance for missing question responses"""
        
        guidance = {
            'data_types': """
   **What you should address:** Look at your `str()` output for sales_df. What data type is the Date column? What about Amount? Are these appropriate for business calculations? For example, if dates are stored as text, you can't easily calculate "days between" or group by month. If amounts have dollar signs, you can't sum them up. Think about what analyses you'd want to do and whether the current data types support that.""",
            
            'data_quality': """
   **What you should address:** Look at your `summary()` and `head()` outputs. Do you see any missing values (NA's)? Any unusual patterns in the data? Are there inconsistencies in how things are formatted? For example, are company names spelled consistently? Do the numbers look reasonable? Think about what might cause problems if you tried to analyze this data.""",
            
            'analysis_readiness': """
   **What you should address:** Compare all three datasets (sales_df, ratings_df, comments_df). Which one looks cleanest and most ready to analyze right away? Which one would need the most work before you could use it? Consider factors like missing data, consistent formatting, appropriate data types, and overall organization. Explain your reasoning!"""
        }
        
        return guidance.get(q_key, "Please provide a thoughtful response to this question.")
    
    def _generate_reflection_overview(self, question_analysis: Dict) -> str:
        """Generate overall feedback on reflection questions"""
        
        total_score = sum(q['score'] for q in question_analysis.values())
        total_possible = sum(q['max_score'] for q in question_analysis.values())
        percentage = (total_score / total_possible) * 100 if total_possible > 0 else 0
        
        if percentage >= 85:
            return """
🌟 **Overall Reflection Quality: Excellent!** Your responses show strong analytical thinking and good understanding of data management concepts. You're thinking like a business analyst should - considering practical implications and being thorough in your observations. Keep up this level of critical thinking!"""
        
        elif percentage >= 70:
            return """
👍 **Overall Reflection Quality: Good!** You're on the right track with your analytical thinking. Your responses show you understand the key concepts, but there's room to go deeper. Try to connect your observations more explicitly to business implications and provide more specific examples from the data."""
        
        elif percentage >= 50:
            return """
📈 **Overall Reflection Quality: Developing** You're starting to think analytically about data, which is great! To improve, focus on being more specific in your observations and explaining the "why" behind your assessments. What would these data issues mean for a real business trying to make decisions?"""
        
        else:
            return """
💡 **Overall Reflection Quality: Needs Development** The reflection questions are where you really develop your analytical thinking skills. Take more time with these - they're not just busy work! Look carefully at your data outputs, think about what you observe, and explain your reasoning. This kind of thinking is what separates good analysts from great ones."""
    
    def _generate_overall_assessment(self, analysis: Dict) -> str:
        """Generate overall assessment and recommendations in professor voice"""
        score_percentage = (analysis['total_score'] / analysis['max_score']) * 100
        
        # Determine grade level and tone
        if score_percentage >= 90:
            grade_level = "Excellent Work!"
            emoji = "🌟"
            tone = "outstanding"
        elif score_percentage >= 80:
            grade_level = "Good Job!"
            emoji = "✅"
            tone = "solid"
        elif score_percentage >= 70:
            grade_level = "Nice Progress!"
            emoji = "👍"
            tone = "developing"
        elif score_percentage >= 60:
            grade_level = "Keep Working!"
            emoji = "📈"
            tone = "improving"
        else:
            grade_level = "Let's Regroup"
            emoji = "💪"
            tone = "building"
        
        # Create personalized assessment
        assessment = f"{emoji} **{grade_level}** ({analysis['total_score']:.1f}/{analysis['max_score']} points - {score_percentage:.1f}%)\n\n"
        
        # Add opening based on performance
        if score_percentage >= 85:
            assessment += "Strong work! You're getting comfortable with R and starting to think analytically about data. Your technical execution is solid. "
        elif score_percentage >= 70:
            assessment += "You're learning the fundamentals well. With some attention to the details below, you'll be ready for more advanced analysis. "
        elif score_percentage >= 50:
            assessment += "Good effort on this assignment. You're building the foundation skills you need. Don't get discouraged - this stuff takes practice. "
        else:
            assessment += "This is challenging material, so don't worry if it feels overwhelming. Focus on the basics and ask questions when you're stuck. "
        
        # Add specific, friendly recommendations
        recommendations = self._generate_friendly_recommendations(analysis)
        
        if recommendations:
            assessment += "Here's what to focus on for next time:\n\n" + "\n".join(recommendations)
        else:
            assessment += "You've mastered all the key concepts for this assignment. Keep up this excellent work!"
        
        # Add closing
        if score_percentage >= 80:
            assessment += "\n\nKeep this up. You're developing the analytical thinking that employers value."
        elif score_percentage >= 60:
            assessment += "\n\nYou're making progress. Each assignment builds on the previous one, so nail down these fundamentals."
        else:
            assessment += "\n\nCome to office hours if you need help. We can work through any concepts that aren't clicking."
        
        return assessment
    
    def _generate_friendly_recommendations(self, analysis: Dict) -> List[str]:
        """Generate friendly, specific recommendations"""
        recommendations = []
        
        # Technical recommendations 
        if analysis['element_scores'].get('working_directory', 0) < 2:
            recommendations.append("**Working Directory:** Run your `getwd()` command and make sure you can see the output. You need to know where R is looking for your files.")
        
        if analysis['element_scores'].get('package_loading', 0) < 4:
            recommendations.append("**Package Loading:** Check that both `tidyverse` and `readxl` load without errors. If you get error messages, you might need to install them first.")
        
        if analysis['element_scores'].get('data_import', 0) < 8:
            recommendations.append("**Data Import:** Make sure all three datasets (sales_df, ratings_df, comments_df) load successfully. Pay attention to file paths and sheet names for the Excel file.")
        
        if analysis['element_scores'].get('data_inspection', 0) < 6:
            recommendations.append("**Data Inspection:** Run `head()`, `str()`, and `summary()` on each dataset. Make sure you can see the outputs - this tells you what your data actually looks like.")
        
        reflection_score = analysis['element_scores'].get('reflection_questions', 0)
        if reflection_score < 10:
            if reflection_score < 5:
                recommendations.append("**Reflection Questions:** Take more time with these. Look at your data outputs and explain what you see. These aren't just busy work - they help you think analytically.")
            else:
                recommendations.append("**Reflection Questions:** Good start, but go deeper. Connect what you observe to business implications. What would these data patterns mean for real decision-making?")
        
        if analysis['code_issues']:
            recommendations.append("**Code Execution:** Fix any error messages before submitting. Red error text means something went wrong - don't ignore it.")
            
            # Add specific code corrections
            code_corrections = self._generate_code_corrections(analysis)
            if code_corrections:
                recommendations.extend(code_corrections)
        
        # Add study tips based on overall performance
        total_percentage = (analysis['total_score'] / analysis['max_score']) * 100
        if total_percentage < 70:
            recommendations.append("**Study Tip:** Go back through the lecture notebook and run the examples yourself. Practice is how you learn R.")
        
        return recommendations
    
    def _extract_student_info(self, nb):
        """Extract student information from notebook"""
        student_info = {
            'name': 'Unknown',
            'id': 'Unknown',
            'submission_date': 'Unknown'
        }
        
        # Look for student info in first few cells
        for i, cell in enumerate(nb.cells[:5]):
            if cell.cell_type == 'markdown':
                content = cell.source
                
                # Look for the specific format: **Student Name:** [NAME]
                name_patterns = [
                    r'\*\*Student Name:\*\*\s*\[?([^\]\n]+)\]?',  # **Student Name:** [NAME] or **Student Name:** NAME
                    r'Student Name:\s*\[?([^\]\n]+)\]?',          # Student Name: [NAME] or Student Name: NAME
                    r'\*\*Name:\*\*\s*\[?([^\]\n]+)\]?',         # **Name:** [NAME]
                    r'Name:\s*\[?([^\]\n]+)\]?',                 # Name: [NAME]
                    r'student[:\s]+([^\n\]]+)',                  # student: NAME (case insensitive)
                    r'name[:\s]+([^\n\]]+)'                      # name: NAME (case insensitive)
                ]
                
                for pattern in name_patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        name = match.group(1).strip()
                        # Clean up common placeholder text
                        if name.lower() not in ['your name here', 'name', 'student name', '[your name here]', 'unknown']:
                            student_info['name'] = name
                            break
                
                # Look for date patterns
                date_patterns = [
                    r'\*\*Date:\*\*\s*\[?([^\]\n]+)\]?',         # **Date:** [DATE]
                    r'Date:\s*\[?([^\]\n]+)\]?',                 # Date: [DATE]
                ]
                
                for pattern in date_patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        date = match.group(1).strip()
                        if date.lower() not in ['today\'s date', 'date', '[today\'s date]', 'unknown']:
                            student_info['submission_date'] = date
                            break
                
                # Look for student ID patterns (if present)
                id_patterns = [
                    r'\*\*Student ID:\*\*\s*\[?([^\]\n]+)\]?',   # **Student ID:** [ID]
                    r'Student ID:\s*\[?([^\]\n]+)\]?',           # Student ID: [ID]
                    r'ID:\s*\[?([^\]\n]+)\]?',                   # ID: [ID]
                ]
                
                for pattern in id_patterns:
                    match = re.search(pattern, content, re.IGNORECASE)
                    if match:
                        student_id = match.group(1).strip()
                        if student_id.lower() not in ['your id here', 'id', 'student id', '[your id here]', 'unknown']:
                            student_info['id'] = student_id
                            break
        
        return student_info
    
    def _generate_code_corrections(self, analysis: Dict) -> List[str]:
        """Generate specific code corrections based on detected issues"""
        corrections = []
        
        # Working directory corrections
        if analysis['element_scores'].get('working_directory', 0) < 2:
            corrections.append("""
**🔧 Working Directory Fix:**
```r
# Make sure to run this cell and see the output
getwd()
```
The output should show your current folder path. If you're not in the right folder, use:
```r
setwd("path/to/your/assignment/folder")
```""")
        
        # Package loading corrections
        pkg_score = analysis['element_scores'].get('package_loading', 0)
        if pkg_score < 4:
            if pkg_score < 2:  # Both packages missing
                corrections.append("""
**🔧 Package Loading Fix:**
```r
# Install packages first (only need to do this once)
install.packages("tidyverse")
install.packages("readxl")

# Then load them (do this every time you restart R)
library(tidyverse)
library(readxl)
```
If you get errors, try installing one at a time and restart R between installations.""")
            else:  # One package missing
                corrections.append("""
**🔧 Package Loading Fix:**
```r
# Make sure both packages are loaded
library(tidyverse)
library(readxl)
```
If you get "package not found" errors, install first:
```r
install.packages("package_name")
```""")
        
        # Data import corrections
        import_score = analysis['element_scores'].get('data_import', 0)
        if import_score < 8:
            corrections.append("""
**🔧 Data Import Fix:**
```r
# For CSV files
sales_df <- read_csv("data/sales_data.csv")

# For Excel files with multiple sheets
ratings_df <- read_excel("data/customer_feedback.xlsx", sheet = "ratings")
comments_df <- read_excel("data/customer_feedback.xlsx", sheet = "customer_feedback")
```
Common fixes:
- Check file paths: make sure "data/" folder exists
- Check sheet names: they're case-sensitive
- Use forward slashes (/) not backslashes (\\) in file paths""")
        
        # Data inspection corrections
        inspection_score = analysis['element_scores'].get('data_inspection', 0)
        if inspection_score < 6:
            corrections.append("""
**🔧 Data Inspection Fix:**
```r
# Run these for each dataset
head(sales_df)      # First 6 rows
str(sales_df)       # Structure and data types
summary(sales_df)   # Statistical summary

# Do the same for other datasets
head(ratings_df)
str(ratings_df)
summary(ratings_df)

head(comments_df)
str(comments_df)
summary(comments_df)
```
Make sure to RUN each cell - you should see output below each command.""")
        
        # Add language-specific corrections based on detected errors
        corrections.extend(self._generate_language_specific_corrections(analysis))
        
        return corrections
    
    def _detect_code_errors(self, code_cells: List[Dict], analysis: Dict):
        """Detect and catalog code execution errors with smart categorization"""
        for cell in code_cells:
            if 'outputs' in cell:
                for output in cell['outputs']:
                    if output.get('output_type') == 'error':
                        error_name = output.get('ename', 'Unknown Error')
                        error_value = output.get('evalue', 'No details')
                        
                        # Add to code issues with specific error info
                        error_msg = f"ERROR: {error_name}: {error_value}"
                        if error_msg not in analysis['code_issues']:
                            analysis['code_issues'].append(error_msg)
                    
                    elif output.get('output_type') == 'stream' and output.get('name') == 'stderr':
                        # Capture warning messages and errors in stderr
                        stderr_text = ''.join(output.get('text', []))
                        
                        # Handle tidyverse conflicts specially - these are informational, not errors
                        if 'tidyverse_conflicts()' in stderr_text and 'Conflicts' in stderr_text:
                            # This is the normal tidyverse conflicts message - treat as informational
                            if 'tidyverse_conflicts_info' not in analysis:
                                analysis['tidyverse_conflicts_info'] = stderr_text.strip()
                                analysis['detailed_feedback'].append("ℹ️ Tidyverse conflicts detected - this is normal and expected")
                        
                        # Handle actual errors that need fixing
                        elif any(error_term in stderr_text.lower() for error_term in [
                            'does not exist', 'path does not exist', 'object', 'not found', 
                            'could not find function', 'no such file'
                        ]):
                            if stderr_text not in analysis['code_issues']:
                                analysis['code_issues'].append(f"ERROR: {stderr_text.strip()}")
                        
                        # Skip minor warnings that aren't actionable
                        elif not any(skip_term in stderr_text.lower() for skip_term in [
                            'warning:', 'note:', 'info:', 'deprecated', 'package startup', 'conflicts'
                        ]):
                            if 'error' in stderr_text.lower() and stderr_text not in analysis['code_issues']:
                                analysis['code_issues'].append(f"ERROR: {stderr_text.strip()}")
    
    def _generate_language_specific_corrections(self, analysis: Dict) -> List[str]:
        """Generate corrections specific to R, SQL, or Python based on detected issues"""
        corrections = []
        
        # R-specific corrections
        r_corrections = self._generate_r_corrections(analysis)
        if r_corrections:
            corrections.extend(r_corrections)
        
        # TODO: Add SQL and Python corrections for future assignments
        # sql_corrections = self._generate_sql_corrections(analysis)
        # python_corrections = self._generate_python_corrections(analysis)
        
        return corrections
    
    def _generate_r_corrections(self, analysis: Dict) -> List[str]:
        """Generate R-specific code corrections with specific, actionable solutions"""
        corrections = []
        
        # Check for common R errors in code issues
        code_issues = analysis.get('code_issues', [])
        
        # Handle tidyverse conflicts explanation
        if 'tidyverse_conflicts_info' in analysis:
            corrections.append("""
**ℹ️ About Tidyverse Conflicts (This is Normal!):**
The message about `dplyr::filter()` masking `stats::filter()` is just R telling you that tidyverse functions will be used instead of base R functions with the same names. This is expected and not an error.

If you ever need the base R version, you can use `stats::filter()` explicitly, but for this class, the tidyverse versions are what we want.""")
        
        for issue in code_issues:
            issue_lower = issue.lower()
            
            # File path errors - most common student issue
            if 'does not exist' in issue_lower and '.csv' in issue_lower:
                corrections.append("""
**🔧 Data Import Fix - CSV File Not Found:**
```r
# Check your working directory and file location
getwd()  # See where R is currently looking
list.files()  # See what files are in current directory
list.files("data/")  # See what's in the data folder

# For CSV files, use:
sales_df <- read_csv("data/sales_data.csv")
# NOT: read_csv("../data/sales.csv") or read_csv("sales.csv")

# Make sure:
# 1. File is named exactly "sales_data.csv" (check spelling!)
# 2. File is in a "data" folder in your project
# 3. You're running from the correct working directory
```""")
            
            elif 'path does not exist' in issue_lower and '.xlsx' in issue_lower:
                corrections.append("""
**🔧 Data Import Fix - Excel File Not Found:**
```r
# For Excel files, use:
ratings_df <- read_excel("data/ratings_data.xlsx", sheet = "ratings")
comments_df <- read_excel("data/ratings_data.xlsx", sheet = "comments")

# Common fixes:
# 1. Check file name spelling: "ratings_data.xlsx" not "ratings.xlsx"
# 2. Make sure file is in "data" folder
# 3. Check sheet names are correct: "ratings" and "comments"

# To see sheet names in an Excel file:
excel_sheets("data/ratings_data.xlsx")
```""")
            
            elif 'object' in issue_lower and 'not found' in issue_lower:
                # Extract the object name if possible
                if 'sales_df' in issue_lower:
                    corrections.append("""
**🔧 Variable Fix - sales_df not found:**
```r
# You're trying to use sales_df before creating it
# Make sure you run this cell first:
sales_df <- read_csv("data/sales_data.csv")

# Then you can use it:
head(sales_df)
str(sales_df)
summary(sales_df)
```""")
                elif 'ratings_df' in issue_lower:
                    corrections.append("""
**🔧 Variable Fix - ratings_df not found:**
```r
# You're trying to use ratings_df before creating it
# Make sure you run this cell first:
ratings_df <- read_excel("data/ratings_data.xlsx", sheet = "ratings")

# Then you can use it:
head(ratings_df)
```""")
                elif 'comments_df' in issue_lower:
                    corrections.append("""
**🔧 Variable Fix - comments_df not found:**
```r
# You're trying to use comments_df before creating it
# Make sure you run this cell first:
comments_df <- read_excel("data/ratings_data.xlsx", sheet = "comments")

# Then you can use it:
head(comments_df)
```""")
                else:
                    corrections.append("""
**🔧 Variable Fix - Object Not Found:**
```r
# This error means you're using a variable before creating it
# Common causes:
# 1. Typo in variable name (check spelling!)
# 2. Didn't run the cell that creates the variable
# 3. Variables are case-sensitive: sales_df ≠ Sales_df

# Solution: Run cells in order from top to bottom
```""")
            
            elif 'could not find function' in issue_lower:
                if 'read_csv' in issue_lower:
                    corrections.append("""
**🔧 Function Fix - read_csv not found:**
```r
# read_csv comes from the tidyverse package
# Make sure you load it first:
library(tidyverse)

# Then you can use:
sales_df <- read_csv("data/sales_data.csv")
```""")
                elif 'read_excel' in issue_lower:
                    corrections.append("""
**🔧 Function Fix - read_excel not found:**
```r
# read_excel comes from the readxl package
# Make sure you load it first:
library(readxl)

# Then you can use:
ratings_df <- read_excel("data/ratings_data.xlsx", sheet = "ratings")
```""")
                else:
                    corrections.append("""
**🔧 Function Fix - Function Not Found:**
```r
# This function isn't available - you probably need to load a package
library(tidyverse)  # For data manipulation functions
library(readxl)     # For Excel import functions

# If you get "package not found", install first:
install.packages("tidyverse")
install.packages("readxl")
```""")
        
        return corrections
    
    def _generate_sql_corrections(self, analysis: Dict) -> List[str]:
        """Generate SQL-specific code corrections for future assignments"""
        corrections = []
        
        # TODO: Implement SQL error detection and corrections
        # Common SQL errors to handle:
        # - Syntax errors (missing semicolons, wrong keywords)
        # - Table/column not found
        # - JOIN syntax issues
        # - GROUP BY errors
        
        return corrections
    
    def _generate_python_corrections(self, analysis: Dict) -> List[str]:
        """Generate Python-specific code corrections for future assignments"""
        corrections = []
        
        # TODO: Implement Python error detection and corrections
        # Common Python errors to handle:
        # - IndentationError
        # - NameError (variable not defined)
        # - ImportError (module not found)
        # - KeyError (dictionary key not found)
        # - IndexError (list index out of range)
        
        return corrections
    
    def _execute_notebook_safely(self, nb, notebook_path: str):
        """Execute notebook cells safely to capture real errors and outputs"""
        try:
            import nbconvert
            from nbconvert.preprocessors import ExecutePreprocessor
            import tempfile
            import shutil
            import os
            
            # Create a temporary copy to execute (don't modify original)
            temp_dir = tempfile.mkdtemp()
            temp_notebook = os.path.join(temp_dir, 'temp_notebook.ipynb')
            
            # Copy the notebook to temp location
            with open(temp_notebook, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
            
            # Set up execution environment
            ep = ExecutePreprocessor(
                timeout=30,  # 30 seconds per cell max
                kernel_name='ir',  # R kernel
                allow_errors=True  # Don't stop on errors - we want to capture them
            )
            
            # Execute the notebook
            with open(temp_notebook, 'r', encoding='utf-8') as f:
                executed_nb = nbformat.read(f, as_version=4)
            
            # Set up execution environment with data files
            notebook_dir = os.path.dirname(os.path.abspath(notebook_path))
            
            # Create data directory and copy required files
            self._setup_data_files(notebook_dir)
            
            try:
                ep.preprocess(executed_nb, {'metadata': {'path': notebook_dir}})
                print(f"✅ Successfully executed notebook: {os.path.basename(notebook_path)}")
            except Exception as exec_error:
                print(f"⚠️ Execution completed with errors: {exec_error}")
            
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            return executed_nb
            
        except ImportError:
            print("⚠️ nbconvert not available - using original notebook without execution")
            return nb
        except Exception as e:
            print(f"⚠️ Notebook execution failed: {e} - using original notebook")
            return nb
    
    def _setup_data_files(self, notebook_dir: str):
        """Set up data files in the notebook execution directory"""
        try:
            import shutil
            
            # Find the main project data directory
            # Go up from homework_grader/submissions/X/ to find the main data/ folder
            current_dir = os.path.abspath(notebook_dir)
            project_root = None
            
            # Look for the main project root (where data/ folder exists)
            for _ in range(5):  # Try up to 5 levels up
                parent = os.path.dirname(current_dir)
                if os.path.exists(os.path.join(parent, 'data')):
                    project_root = parent
                    break
                current_dir = parent
            
            if not project_root:
                print("⚠️ Could not find main data directory")
                return
            
            source_data_dir = os.path.join(project_root, 'data')
            target_data_dir = os.path.join(notebook_dir, 'data')
            
            # Create data directory in notebook location
            os.makedirs(target_data_dir, exist_ok=True)
            
            # Copy required data files to support multiple working directory approaches
            required_files = [
                'sales_data.csv',
                'customer_feedback.xlsx',  # The actual file students use
                'ratings_data.xlsx',  # Alternative name
                'customer_ratings.csv',  # Alternative
                'customer_comments.csv'  # Alternative
            ]
            
            for filename in required_files:
                source_file = os.path.join(source_data_dir, filename)
                target_file = os.path.join(target_data_dir, filename)
                
                if os.path.exists(source_file):
                    shutil.copy2(source_file, target_file)
                    print(f"📁 Copied {filename} to execution directory")
                    
                    # Also copy to notebook directory root for students who set working directory to data
                    root_target = os.path.join(notebook_dir, filename)
                    if not os.path.exists(root_target):
                        shutil.copy2(source_file, root_target)
                        print(f"📁 Also copied {filename} to notebook root for direct access")
            
            # Create customer_feedback.xlsx if it doesn't exist (from separate CSV files)
            customer_feedback_path = os.path.join(target_data_dir, 'customer_feedback.xlsx')
            if not os.path.exists(customer_feedback_path):
                self._create_customer_feedback_excel(source_data_dir, customer_feedback_path)
                # Also copy to root
                root_feedback_path = os.path.join(notebook_dir, 'customer_feedback.xlsx')
                if not os.path.exists(root_feedback_path):
                    shutil.copy2(customer_feedback_path, root_feedback_path)
            
            # Create ratings_data.xlsx if it doesn't exist (combine CSV files into Excel)
            ratings_xlsx_path = os.path.join(target_data_dir, 'ratings_data.xlsx')
            if not os.path.exists(ratings_xlsx_path):
                self._create_ratings_excel(source_data_dir, ratings_xlsx_path)
            
        except Exception as e:
            print(f"⚠️ Error setting up data files: {e}")
    
    def _create_ratings_excel(self, source_data_dir: str, target_excel_path: str):
        """Create ratings_data.xlsx from CSV files"""
        try:
            import pandas as pd
            
            # Try to find ratings and comments CSV files
            ratings_csv = os.path.join(source_data_dir, 'customer_ratings.csv')
            comments_csv = os.path.join(source_data_dir, 'customer_comments.csv')
            
            if os.path.exists(ratings_csv) and os.path.exists(comments_csv):
                # Read CSV files
                ratings_df = pd.read_csv(ratings_csv)
                comments_df = pd.read_csv(comments_csv)
                
                # Create Excel file with multiple sheets
                with pd.ExcelWriter(target_excel_path, engine='openpyxl') as writer:
                    ratings_df.to_excel(writer, sheet_name='ratings', index=False)
                    comments_df.to_excel(writer, sheet_name='comments', index=False)
                
                print(f"📊 Created ratings_data.xlsx with ratings and comments sheets")
            
        except Exception as e:
            print(f"⚠️ Could not create ratings_data.xlsx: {e}")
    
    def _create_customer_feedback_excel(self, source_data_dir: str, target_excel_path: str):
        """Create customer_feedback.xlsx from CSV files"""
        try:
            import pandas as pd
            
            # Try to find ratings and comments CSV files
            ratings_csv = os.path.join(source_data_dir, 'customer_ratings.csv')
            comments_csv = os.path.join(source_data_dir, 'customer_comments.csv')
            
            if os.path.exists(ratings_csv) and os.path.exists(comments_csv):
                # Read CSV files
                ratings_df = pd.read_csv(ratings_csv)
                comments_df = pd.read_csv(comments_csv)
                
                # Create Excel file with multiple sheets
                with pd.ExcelWriter(target_excel_path, engine='openpyxl') as writer:
                    ratings_df.to_excel(writer, sheet_name='ratings', index=False)
                    comments_df.to_excel(writer, sheet_name='customer_feedback', index=False)
                
                print(f"📊 Created customer_feedback.xlsx with ratings and customer_feedback sheets")
            
        except Exception as e:
            print(f"⚠️ Could not create customer_feedback.xlsx: {e}")
    
    def _detect_execution_environment(self) -> str:
        """Detect what execution environment is available"""
        try:
            # Check for R kernel
            import subprocess
            result = subprocess.run(['R', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return 'R'
        except:
            pass
        
        try:
            # Check for Python
            import sys
            return 'Python'
        except:
            pass
        
        return 'None'
    
    def _setup_execution_environment(self, language: str):
        """Set up the execution environment for the detected language"""
        if language == 'R':
            # Ensure R packages are available
            r_packages = ['tidyverse', 'readxl', 'knitr']
            # Could add package installation logic here
            pass
        elif language == 'Python':
            # Ensure Python packages are available
            python_packages = ['pandas', 'numpy', 'matplotlib']
            # Could add package installation logic here
            pass

def format_detailed_feedback(analysis: Dict) -> List[str]:
    """Format the detailed analysis into readable feedback"""
    feedback = []
    
    # Header
    feedback.append("📋 **DETAILED HOMEWORK ANALYSIS**")
    feedback.append("=" * 50)
    feedback.append("")
    
    # Overall score
    feedback.append(f"**Final Score: {analysis['total_score']:.1f} / {analysis['max_score']} points**")
    feedback.append("")
    
    # Detailed breakdown
    feedback.append("**DETAILED BREAKDOWN:**")
    feedback.extend(analysis['detailed_feedback'])
    feedback.append("")
    
    # Missing elements
    if analysis['missing_elements']:
        feedback.append("**MISSING ELEMENTS:**")
        for element in analysis['missing_elements']:
            feedback.append(f"• {element}")
        feedback.append("")
    
    # Code issues
    if analysis['code_issues']:
        feedback.append("**CODE ISSUES TO FIX:**")
        for issue in analysis['code_issues']:
            feedback.append(f"• {issue}")
        feedback.append("")
    
    # Question analysis
    if analysis['question_analysis']:
        feedback.append("**REFLECTION QUESTIONS ANALYSIS:**")
        for q_key, q_data in analysis['question_analysis'].items():
            feedback.append(f"• {q_key.replace('_', ' ').title()}: {q_data['quality']} ({q_data['score']:.1f}/{q_data['max_score']} points)")
        feedback.append("")
    
    # Overall assessment
    feedback.append(analysis['overall_assessment'])
    
    return feedback
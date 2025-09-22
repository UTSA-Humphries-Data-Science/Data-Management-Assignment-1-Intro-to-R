# AI-Powered Homework Grader

A comprehensive Streamlit application for grading student homework notebooks with AI assistance and continuous learning capabilities.

## 📁 Project Structure

```
homework_grader/
├── 📱 Core Application
│   ├── app.py                    # Main Streamlit application
│   ├── ai_grader.py             # AI grading engine
│   ├── assignment_manager.py     # Assignment creation & management
│   ├── grading_interface.py     # Manual grading interface
│   ├── training_interface.py    # AI training dashboard
│   └── report_generator.py      # Report generation
│
├── 🔧 Utilities & Helpers
│   ├── alternative_approaches.py # Handle multiple valid solutions
│   ├── assignment_setup_helper.py # Assignment creation wizard
│   ├── correction_helpers.py    # Grading correction tools
│   ├── detailed_analyzer.py     # Comprehensive analysis
│   ├── excel_summary.py         # Excel report generation
│   ├── language_detector.py     # R/SQL/Python detection
│   └── model_status.py          # AI model status monitoring
│
├── 📚 Documentation
│   ├── docs/                    # Detailed guides and workflows
│   └── QUICKSTART.md           # Quick start guide
│
├── 🧪 Templates & Examples
│   └── templates/              # Assignment templates and rubrics
│
├── 🔬 Tests
│   └── tests/                  # Test files
│
├── 📜 Scripts
│   └── scripts/                # Setup and utility scripts
│
└── 📊 Data Directories
    ├── assignments/            # Assignment files
    ├── submissions/            # Student submissions
    ├── feedback_reports/       # Generated reports
    └── models/                # Trained AI models
```

## Features

### 🎯 Core Functionality
- **Assignment Management**: Create assignments with rubrics, templates, and solution notebooks
- **Batch Upload**: Upload multiple student submissions via ZIP files or individual uploads
- **AI Grading**: Automated grading using machine learning models
- **Manual Review**: Human grading interface with AI suggestions
- **Continuous Learning**: AI improves over time based on your grading patterns

### 🤖 AI Capabilities
- **Local AI Integration**: Uses OS120 or other local models for detailed grading
- **Code Execution**: Automatically runs student notebooks and checks for errors
- **Intelligent Analysis**: Provides contextual feedback on code quality and correctness
- **Solution Comparison**: Compares student work with reference solutions
- **Adaptive Learning**: Learns from your grading patterns to improve accuracy
- **Privacy-First**: All AI processing happens locally on your machine

### 📊 Analytics & Reporting
- **Grade Analytics**: View class performance and statistics
- **Export Results**: Download grades as CSV files
- **Progress Tracking**: Monitor AI training progress
- **Detailed Feedback**: Comprehensive feedback for students

## Installation

1. **Prerequisites**:
   ```bash
   # Ensure you have Python 3.8+ and Jupyter installed
   pip install jupyter
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Local AI (Optional but Recommended)**:
   ```bash
   # Follow the detailed guide in AI_SETUP.md
   # This enables advanced AI grading with OS120 model
   ```

4. **Run the Application**:
   ```bash
   python run_grader.py
   # or
   streamlit run app.py
   ```

## Quick Start Guide

### 1. Create Your First Assignment
1. Navigate to "Create Assignment" in the sidebar
2. Fill in assignment details and grading rubric
3. Upload template and solution notebooks
4. Click "Create Assignment"

### 2. Upload Student Submissions
1. Go to "Upload Submissions"
2. Select your assignment
3. Choose between single file or batch upload (ZIP)
4. Upload student notebooks

### 3. Grade with AI
1. Visit "Grade Submissions"
2. Select your assignment
3. Click "Grade All Submissions"
4. Review AI-generated scores and feedback

### 4. Manual Review & Training
1. Go to "View Results"
2. Click "Grade" next to any submission
3. Adjust scores and add feedback
4. Your corrections train the AI for future grading

### 5. Train the AI Model
1. Navigate to "AI Training"
2. Select assignment or "All Assignments"
3. Click "Train AI Model" (requires 10+ manual grades)

## File Structure

```
homework_grader/
├── app.py                 # Main Streamlit application
├── assignment_manager.py  # Assignment creation and upload handling
├── ai_grader.py          # AI grading engine and model training
├── grading_interface.py  # Manual grading and results viewing
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── assignments/         # Stored assignment templates and solutions
├── submissions/         # Student submission notebooks
├── models/             # Trained AI models
└── grading_database.db # SQLite database (created automatically)
```

## Database Schema

The application uses SQLite with the following tables:

- **assignments**: Assignment metadata, rubrics, and file paths
- **students**: Student information
- **submissions**: Individual submission records with scores
- **ai_training_data**: Training data for machine learning models

## Grading Rubric Format

Rubrics should be in JSON format:

```json
{
    "code_execution": {
        "points": 40,
        "description": "Code runs without errors"
    },
    "correct_output": {
        "points": 30,
        "description": "Produces expected results"
    },
    "code_quality": {
        "points": 20,
        "description": "Clean, readable code with comments"
    },
    "analysis": {
        "points": 10,
        "description": "Proper interpretation of results"
    }
}
```

## AI Grading Features

### Automatic Analysis
- **Code Execution**: Runs notebooks and detects errors
- **Code Quality**: Analyzes comments, structure, and style
- **Content Completeness**: Checks for required elements
- **Solution Similarity**: Compares with reference solutions

### Machine Learning
- **Feature Extraction**: Converts notebooks to numerical features
- **Random Forest Model**: Predicts scores based on historical data
- **Continuous Learning**: Improves with each manual grade
- **Personalized Models**: Adapts to your grading style

## Best Practices

### For Instructors
1. **Start Small**: Begin with a few manual grades to train the AI
2. **Review AI Suggestions**: Always review AI grades before finalizing
3. **Provide Detailed Feedback**: Rich feedback improves AI learning
4. **Regular Training**: Retrain models as you accumulate more data

### For Assignments
1. **Clear Rubrics**: Define specific, measurable criteria
2. **Solution Notebooks**: Provide complete reference solutions
3. **Consistent Structure**: Use similar notebook formats across assignments
4. **Test Cases**: Include expected outputs in solutions

## Troubleshooting

### Common Issues

**Notebook Execution Fails**:
- Ensure all required packages are installed
- Check for infinite loops or long-running code
- Verify file paths and data availability

**AI Scores Seem Inaccurate**:
- Need more training data (10+ manual grades minimum)
- Review and adjust manual grades for consistency
- Retrain the model with updated data

**Upload Issues**:
- Check file formats (.ipynb only)
- Ensure ZIP files contain notebooks in root directory
- Verify student ID naming conventions

### Performance Tips
- Use batch upload for large classes
- Train models regularly for better accuracy
- Export results frequently as backups
- Monitor disk space for large notebook collections

## Advanced Features

### Custom Scoring
- Modify `ai_grader.py` to implement custom scoring algorithms
- Add new feature extractors for specific assignment types
- Integrate with external grading tools or APIs

### Integration
- Export grades to LMS systems via CSV
- Connect to institutional databases
- Integrate with plagiarism detection tools

## Support

For issues or feature requests:
1. Check the troubleshooting section above
2. Review the code comments for implementation details
3. Modify the source code to fit your specific needs

## License

This project is designed for educational use. Modify and distribute as needed for your institution.
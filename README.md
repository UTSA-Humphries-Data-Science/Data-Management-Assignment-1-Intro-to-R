# Data Management Classroom

A **zero-touch Codespaces environment** for data science education using Python, R, Jupyter, and PostgreSQL.

## 🚀 Quick Start

1. **Open in Codespaces** - Click "Create codespace" 
2. **Wait for setup** - Takes 5-10 minutes for first-time setup
3. **Start coding** - Everything works immediately, no manual setup required

## 🎯 What You Get

### Instant Data Science Environment
- **Python 3.12** with pandas, numpy, matplotlib, seaborn, scikit-learn
- **R 4.3** with tidyverse, ggplot2, dplyr, data analysis packages  
- **Jupyter Lab** with Python and R kernels
- **PostgreSQL** database ready to use
- **VS Code** with all data science extensions

### Zero Manual Setup
- ✅ No password prompts
- ✅ No configuration needed
- ✅ Database works immediately
- ✅ All packages pre-installed
- ✅ Students can start coding right away

## 📁 Project Structure

```
├── assignments/     # Course assignments and exercises
├── notebooks/       # Jupyter notebooks and examples
├── data/           # Datasets and CSV files
├── databases/      # SQL scripts and database files
├── scripts/        # Environment testing and utility scripts
└── .devcontainer/  # Codespaces configuration (students don't need to touch)
```

## 🧪 Environment Details

### Python Environment
All packages installed via conda:
- Data: pandas, numpy, polars
- Visualization: matplotlib, seaborn, plotly
- Machine Learning: scikit-learn, scipy
- Database: sqlalchemy, psycopg2
- Jupyter: jupyter, ipython, kernels

### R Environment  
All packages via conda:
- Core: tidyverse, dplyr, ggplot2, tidyr, readr
- Database: DBI, RPostgreSQL
- Jupyter: IRkernel for R notebooks

### Database
- **PostgreSQL** server running locally
- **Database name:** `vscode`
- **Username:** `vscode` 
- **Connection:** Automatic via environment variables

## 📚 For Students

### Getting Started
1. Create a new Jupyter notebook in the `notebooks/` folder
2. Choose Python or R kernel
3. Start analyzing data immediately!

### Sample Data
- `data/WestRoxbury.csv` - Real estate data for analysis
- `data/sample.csv` - Basic sample dataset
- Additional datasets in `data/` folder

### Example Notebooks
- `notebooks/getting-started.ipynb` - Introduction examples
- `notebooks/westroxbury-analysis.ipynb` - Real data analysis
- `notebooks/r-kernel-diagnostic.ipynb` - R environment and database test

## 🛠️ For Instructors

### Adding Assignments
1. Create new folder in `assignments/`
2. Add Jupyter notebook with exercises
3. Include any needed data files
4. Students will have immediate access

### Database Setup
PostgreSQL is pre-configured and ready. To add sample data:
```sql
-- Connect to database (automatic in notebooks)
-- Add your tables and sample data
```

### Environment Verification
Run the test script to verify everything works:
```bash
python scripts/test_setup.py
```

## 🎓 Zero-Touch Philosophy

This environment follows a **zero-touch approach**:
- Students never see password prompts
- No manual installation or configuration
- All tools work immediately after Codespace creation
- Focus on learning, not setup

## 📋 Technical Notes

The devcontainer uses:
- **Base:** Jupyter datascience-notebook (official image)
- **User:** Transitions from `jovyan` to `vscode` during setup
- **Setup:** Automated user transition with passwordless sudo
- **Database:** PostgreSQL with pre-configured user and database
- **Extensions:** Complete VS Code data science extension pack

This provides a professional data science development environment that "just works" for education.

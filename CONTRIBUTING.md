# How to Submit Your Assignment

## Quick Submission Guide

1. **Complete your work** in `assignment/Homework/homework_lesson_1.R` (or `.Rmd`)

2. **Check your work** by running your code to make sure it works

3. **Commit your changes:**
   ```bash
   git add assignment/Homework/
   git commit -m "Complete homework lesson 1"
   ```

4. **Push to submit:**
   ```bash
   git push origin main
   ```

5. **Verify submission** by checking your GitHub repository online

## Troubleshooting

### "Permission denied" or authentication errors
- Make sure you're working in the GitHub Codespace
- Try: `git config --global credential.helper store`

### "Nothing to commit"
- Make sure your file is saved
- Check that you're in the right directory: `pwd`
- Your file should be in `assignment/Homework/`

### Code doesn't run
- Check for typos in variable names
- Make sure you loaded required packages: `library(tidyverse)`
- Verify data file paths are correct

### Still having issues?
Contact your instructor with:
- What you were trying to do
- The exact error message
- A screenshot if helpful

# How to Submit Your Assignment

## Quick Submission Guide

1. **Complete your work** in `assignment/Homework/homework_lesson_1.ipynb`

2. **Run all cells** to make sure your code works and shows output

3. **Save your notebook** (Ctrl+S or Cmd+S)

4. **Commit your changes:**
   ```bash
   git add assignment/Homework/
   git commit -m "Complete homework lesson 1"
   ```

5. **Push to submit:**
   ```bash
   git push origin main
   ```

6. **Verify submission** by checking your GitHub repository online

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
- Make sure you loaded required packages in the first cells
- Verify data file paths are correct
- Try restarting the R kernel: Kernel → Restart Kernel

### Notebook won't save
- Make sure you have write permissions
- Try Ctrl+S (or Cmd+S) to force save
- Check disk space isn't full

### Still having issues?
Contact your instructor with:
- What you were trying to do
- The exact error message
- A screenshot if helpful

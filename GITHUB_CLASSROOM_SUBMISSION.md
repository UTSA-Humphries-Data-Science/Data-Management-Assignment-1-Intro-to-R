# GitHub Classroom Submission Guide

## 🎯 For Students: How to Submit Your Assignment

### Before You Start
- Make sure you accepted the assignment through the GitHub Classroom link provided by your instructor
- You should be working in YOUR individual repository (the URL will include your GitHub username)
- Complete your work in the provided Jupyter notebook

### Submission Process

#### 1. Complete Your Assignment
- Open `assignment/Homework/homework_lesson_1.ipynb` in VS Code
- Complete all code cells and markdown responses
- Run all cells to show outputs (Cell → Run All)
- Save your notebook (Ctrl+S)

#### 2. Submit Through Git
```bash
# In the VS Code terminal, run these commands:

# Check your current status
git status

# Add your completed notebook
git add assignment/Homework/homework_lesson_1.ipynb

# Commit your work
git commit -m "Submit assignment 1"

# Push to GitHub Classroom (this is your submission!)
git push origin main
```

#### 3. Verify Your Submission
1. Go to your GitHub repository in a web browser
2. Navigate to `assignment/Homework/`
3. Click on your notebook file
4. Confirm you can see your completed work with outputs
5. Note the "Last commit" timestamp

### 🔍 How Grading Works

**Automatic Checks:**
- GitHub Classroom may run basic tests on your submission
- Check the "Actions" tab in your repository for test results
- Green checkmarks = tests passed, red X = issues found

**Manual Grading:**
- Your instructor will review your submitted notebook
- They can see all your code, outputs, and written responses
- Grades will be posted through your course management system

### ⚠️ Common Submission Issues

**"Nothing to commit" error:**
- Make sure you saved your notebook first (Ctrl+S)
- Check that you're in the right directory
- Verify your notebook actually has changes

**"Permission denied" error:**
- Make sure you're working in your own repository (not the template)
- You should be in GitHub Codespaces or have proper git credentials set up

**"Behind the remote" error:**
- Run `git pull origin main` first
- Then try your submission commands again

**Can't see outputs in GitHub:**
- Make sure you ran all cells before saving (Cell → Run All)
- Outputs should be visible when you view the notebook on GitHub

### 📅 Submission Timeline

- **Multiple submissions allowed**: You can push changes multiple times before the deadline
- **Latest submission counts**: Your most recent push before the deadline is what gets graded
- **Deadline enforcement**: GitHub Classroom tracks exact submission times
- **Late policy**: Check with your instructor about late submission policies

### 🆘 Getting Help

If you encounter issues:

1. **Check this guide first** - many common problems are covered above
2. **Ask a classmate** - they might have encountered the same issue
3. **Contact your instructor** - provide:
   - Screenshot of any error messages
   - Your repository URL
   - What you were trying to do when the error occurred
4. **Use office hours** - bring your laptop for hands-on help

### ✅ Submission Success Checklist

- [ ] Completed all sections of the notebook
- [ ] Ran all cells to show outputs
- [ ] Saved the notebook file
- [ ] Successfully pushed to GitHub (`git push origin main`)
- [ ] Verified submission appears on GitHub repository
- [ ] Checked timestamp is before deadline
- [ ] Reviewed any auto-grading results

**Remember: It's your responsibility to ensure your assignment is properly submitted before the deadline!**

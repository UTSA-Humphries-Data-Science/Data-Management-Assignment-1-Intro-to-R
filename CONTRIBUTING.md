# How to Submit Your Assignment to GitHub Classroom

## 📚 Complete Submission Guide

### Step 1: Complete Your Assignment
1. **Open your notebook**: `assignment/Homework/homework_lesson_1.ipynb`
2. **Fill in your information** at the top (name, date)
3. **Complete all sections** (Parts 1, 2, and 3)
4. **Run all cells** to show your outputs (Cell → Run All)
5. **Save your work** (Ctrl+S or Cmd+S)

### Step 2: Submit via Git Commands

**Option A: Using VS Code Terminal**
1. Open Terminal in VS Code (Terminal → New Terminal)
2. Run these commands one by one:

```bash
# Make sure you're in the right directory
cd /workspaces/Data-Management-Assignment-1-Intro-to-R

# Check what files you've changed
git status

# Add your completed notebook
git add assignment/Homework/homework_lesson_1.ipynb

# Commit with a message
git commit -m "Submit homework lesson 1 - [Your Name]"

# Push to GitHub Classroom
git push origin main
```

**Option B: Using VS Code Git Interface**
1. Click the Source Control icon in the left sidebar (looks like a branch)
2. You'll see your changed files listed
3. Click the "+" next to `homework_lesson_1.ipynb` to stage it
4. Type a commit message like "Submit homework lesson 1 - [Your Name]"
5. Click the "Commit" button
6. Click "Sync Changes" or "Push" to submit

### Step 3: Verify Your Submission

1. **Check the terminal output** - you should see something like:
   ```
   Enumerating objects: 5, done.
   Counting objects: 100% (5/5), done.
   Writing objects: 100% (3/3), 2.15 KiB | 2.15 MiB/s, done.
   Total 3 (delta 1), reused 0 (delta 0), pack-reused 0
   To https://github.com/[instructor]/[your-repo-name].git
      abc1234..def5678  main -> main
   ```

2. **Visit your GitHub repository**:
   - Go to your assignment repository in a web browser
   - Navigate to `assignment/Homework/`
   - Click on `homework_lesson_1.ipynb`
   - Verify you can see your completed work with outputs

3. **Check for auto-grading results** (if enabled):
   - Go to the "Actions" tab in your GitHub repository
   - Look for a green checkmark or red X next to your latest commit

## 🚨 Submission Deadline Reminders

- **Submit before the deadline** - GitHub Classroom tracks submission timestamps
- **You can submit multiple times** - your latest submission before the deadline counts
- **Don't wait until the last minute** - allow time for technical issues
- **Always verify your submission** - check that your work appears on GitHub

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

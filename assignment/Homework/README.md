# Homework Assignment - Lesson 1: Introduction to R



**Instructions:**

*   Complete the following tasks in an R script (`.R` file) or an R Markdown document (`.Rmd` file) in VS Code Codespaces.
*   Ensure your code is well-commented and easy to understand.
*   Submit your `.R` or `.Rmd` file, along with any generated output files (e.g., cleaned CSVs if applicable).

---

## Part 1: Setting Up Your Environment and Importing Data

1.  **Working Directory:**
    *   Open VS Code Codespaces and create a new folder for this homework assignment (e.g., `homework_lesson_1`).
    *   Verify your current working directory using `getwd()`.
    *   If necessary, set your working directory to the newly created folder using `setwd()`.

2.  **Package Installation & Loading:**
    *   Ensure the `tidyverse` and `readxl` packages are installed. If not, install them.
    *   Load both packages into your R session.

3.  **Data Import - CSV:**
    *   Download the `sales_data.csv` file from the course materials (or create one with similar structure if not available). This file contains dummy sales records.
    *   Import `sales_data.csv` into an R data frame named `sales_df` using `read_csv()`.

4.  **Data Import - Excel:**
    *   Download the `customer_feedback.xlsx` file from the course materials (or create one with similar structure if not available). This file contains customer feedback data, with different sheets for `Ratings` and `Comments`.
    *   Import the `Ratings` sheet from `customer_feedback.xlsx` into an R data frame named `ratings_df` using `read_excel()`.
    *   Import the `Comments` sheet from `customer_feedback.xlsx` into an R data frame named `comments_df` using `read_excel()`.

---

## Part 2: Basic Data Inspection

Perform the following inspection tasks for each of the three data frames you imported (`sales_df`, `ratings_df`, `comments_df`). For each data frame, provide the R code and the output, along with a brief interpretation of what you observe.

1.  **First Few Rows:** Display the first 10 rows of each data frame.
2.  **Structure:** Display the structure (data types, number of observations/variables) of each data frame.
3.  **Summary Statistics:** Display summary statistics for each data frame.
4.  **Visual Inspection (Optional, but Recommended):** If your VS Code setup allows, use `View()` to open each data frame in the data viewer and briefly describe any immediate observations (e.g., presence of missing values, unexpected values).

---

## Part 3: Reflection Questions

Answer the following questions in your submission document:

1.  Based on your inspection of `sales_df`, what are the data types of the `Date` and `Amount` columns? Are these data types appropriate for typical business analytics tasks involving sales data? Explain why or why not.
2.  Looking at `ratings_df` and `comments_df`, do you notice any potential issues (e.g., missing values, inconsistent data types) that might need to be addressed in future data wrangling steps? (No need to fix them, just identify them).
3.  Why is it important to perform initial data inspection immediately after importing data? What kind of problems can it help you identify early on?
4.  Briefly explain the difference between `install.packages()` and `library()` in R. When would you use each function?

---

**Submission Checklist:**

*   [ ] R script Notebook file with all code and outputs.
*   [ ] Answers to reflection questions included in the document or as a separate text file.
*   [ ] All necessary data files (`sales_data.csv`, `customer_feedback.xlsx`) are accessible (e.g., in the same directory or clearly referenced).

Good luck!



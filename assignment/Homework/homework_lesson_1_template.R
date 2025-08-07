# Homework Assignment - Lesson 1: Introduction to R
# Student Name: [YOUR NAME HERE]
# Date: [TODAY'S DATE]

# =============================================================================
# Part 1: Setting Up Your Environment and Importing Data
# =============================================================================

# 1. Working Directory
# Check current working directory
getwd()

# 2. Package Loading
# Load required packages
library(tidyverse)
library(readxl)

# 3. Data Import - CSV
# Import sales data
sales_df <- read_csv("data/sales_data.csv")

# 4. Data Import - Excel
# Import ratings data from Excel
ratings_df <- read_excel("data/customer_feedback.xlsx", sheet = "Ratings")

# Import comments data from Excel
comments_df <- read_excel("data/customer_feedback.xlsx", sheet = "Comments")

# =============================================================================
# Part 2: Basic Data Inspection
# =============================================================================

# Sales Data Inspection
print("=== SALES DATA INSPECTION ===")

# First 10 rows
print("First 10 rows of sales_df:")
head(sales_df, 10)

# Structure
print("Structure of sales_df:")
str(sales_df)

# Summary statistics
print("Summary statistics for sales_df:")
summary(sales_df)

# Visual inspection (optional)
# View(sales_df)  # Uncomment to open in data viewer

# Ratings Data Inspection
print("=== RATINGS DATA INSPECTION ===")

# TODO: Add your code here for ratings_df inspection
# - First 10 rows
# - Structure
# - Summary statistics

# Comments Data Inspection
print("=== COMMENTS DATA INSPECTION ===")

# TODO: Add your code here for comments_df inspection
# - First 10 rows
# - Structure  
# - Summary statistics

# =============================================================================
# Part 3: Reflection Questions
# =============================================================================

# Question 1: Data types of Date and Amount columns in sales_df
# TODO: Write your analysis here as comments

# Question 2: [Add other reflection questions from README]
# TODO: Write your responses here as comments

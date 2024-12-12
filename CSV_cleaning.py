from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower, lit, when, isnull
import pandas as pd

# Initialize Spark Session
spark = SparkSession.builder.appName('cleaning_cv_data').getOrCreate()

# Load CSV into a Spark DataFrame
cv_data = spark.read.csv("./cv_data.csv", header=True, inferSchema=True)

# Print schema to understand the data
cv_data.printSchema()

# Define a dictionary to map directories to sample content for missing columns
directory_to_content = {
    "ACCOUNTANT": {
        "Work Experience": "2+ years as an accountant in a corporate firm",
        "Education": "Bachelor's degree in Accounting",
        "Skills": "Excel, QuickBooks, Financial Analysis",
        "Languages": "English, French"
    },
    "ADVOCATE": {
        "Work Experience": "5+ years as a corporate advocate specializing in civil law",
        "Education": "Law Degree from XYZ University",
        "Skills": "Legal Research, Litigation, Negotiation",
        "Languages": "English, Arabic"
    },
    "AGRICULTURE": {
        "Work Experience": "3+ years in agricultural management and farming",
        "Education": "Bachelor's degree in Agriculture",
        "Skills": "Farm Management, Crop Rotation, Pest Control",
        "Languages": "English, French"
    },
    "APPAREL": {
        "Work Experience": "4+ years working in fashion design and apparel manufacturing",
        "Education": "Bachelor's degree in Fashion Design",
        "Skills": "Design, Pattern Making, Textile Knowledge",
        "Languages": "English, Italian"
    },
    "ARTS": {
        "Work Experience": "5+ years as a visual artist specializing in abstract art",
        "Education": "Master's in Fine Arts from ABC University",
        "Skills": "Painting, Sculpture, Digital Art",
        "Languages": "English, French"
    },
    "AUTOMOBILE": {
        "Work Experience": "3+ years in automobile sales and customer service",
        "Education": "Bachelor's degree in Automotive Engineering",
        "Skills": "Vehicle Diagnostics, Sales, Customer Relations",
        "Languages": "English, Spanish"
    },
    "AVIATION": {
        "Work Experience": "2+ years as a commercial pilot with XYZ Airlines",
        "Education": "Bachelor's in Aviation and Piloting from ABC Academy",
        "Skills": "Flight Operations, Safety Protocols, Aircraft Maintenance",
        "Languages": "English, Arabic"
    },
    "BANKING": {
        "Work Experience": "4+ years in retail banking and financial services",
        "Education": "Bachelor's degree in Finance",
        "Skills": "Customer Service, Loan Management, Risk Assessment",
        "Languages": "English, French"
    },
    "BPO": {
        "Work Experience": "3+ years in BPO operations as a customer support specialist",
        "Education": "Bachelor's degree in Business Administration",
        "Skills": "Customer Support, Telemarketing, Conflict Resolution",
        "Languages": "English, Hindi"
    },
    "BUSINESS-DEVELOPMENT": {
        "Work Experience": "5+ years as a Business Development Manager",
        "Education": "MBA in Business Development",
        "Skills": "Market Research, Sales Strategy, Partnership Management",
        "Languages": "English, Spanish"
    },
    "CHEF": {
        "Work Experience": "8+ years as an executive chef in a fine dining restaurant",
        "Education": "Culinary Arts Degree from ABC Culinary School",
        "Skills": "Menu Creation, Food Preparation, Staff Management",
        "Languages": "English, French"
    },
    "CONSTRUCTION": {
        "Work Experience": "10+ years as a project manager in the construction industry",
        "Education": "Bachelor's degree in Civil Engineering",
        "Skills": "Project Management, Site Supervision, Budgeting",
        "Languages": "English, Spanish"
    },
    "CONSULTANT": {
        "Work Experience": "5+ years as a business consultant specializing in strategy",
        "Education": "MBA in Business Strategy",
        "Skills": "Strategy Formulation, Market Analysis, Client Management",
        "Languages": "English, French"
    },
    "DESIGNER": {
        "Work Experience": "3+ years as a graphic designer for digital media",
        "Education": "Bachelor's degree in Graphic Design",
        "Skills": "Adobe Creative Suite, Typography, User Interface Design",
        "Languages": "English, German"
    },
    "DIGITAL-MEDIA": {
        "Work Experience": "4+ years as a social media manager and content strategist",
        "Education": "Bachelor's degree in Digital Marketing",
        "Skills": "Content Creation, Social Media Marketing, SEO",
        "Languages": "English, Spanish"
    },
    "ENGINEERING": {
        "Work Experience": "6+ years as a software engineer in a tech firm",
        "Education": "Bachelor's degree in Computer Science",
        "Skills": "Programming (Java, Python), Database Management, Agile",
        "Languages": "English, German"
    },
    "FINANCE": {
        "Work Experience": "4+ years as a financial analyst",
        "Education": "Bachelor's degree in Finance",
        "Skills": "Financial Reporting, Budgeting, Risk Management",
        "Languages": "English, French"
    },
    "FITNESS": {
        "Work Experience": "5+ years as a personal trainer and fitness coach",
        "Education": "Certified Personal Trainer",
        "Skills": "Strength Training, Weight Loss, Nutrition Planning",
        "Languages": "English, Spanish"
    },
    "HEALTHCARE": {
        "Work Experience": "6+ years as a nurse in a hospital setting",
        "Education": "Bachelor's in Nursing",
        "Skills": "Patient Care, Medical Documentation, Emergency Response",
        "Languages": "English, Arabic"
    },
    "HR": {
        "Work Experience": "3+ years in human resources management",
        "Education": "Bachelor's degree in Human Resource Management",
        "Skills": "Recruitment, Employee Relations, Payroll",
        "Languages": "English, Spanish"
    },
    "INFORMATION-TECHNOLOGY": {
        "Work Experience": "5+ years as an IT manager in a multinational company",
        "Education": "Bachelor's degree in Information Technology",
        "Skills": "Network Security, Cloud Computing, IT Support",
        "Languages": "English, German"
    },
    "PUBLIC-RELATIONS": {
        "Work Experience": "4+ years as a public relations manager for a major corporation",
        "Education": "Bachelor's in Public Relations",
        "Skills": "Media Relations, Crisis Communication, Brand Management",
        "Languages": "English, French"
    },
    "SALES": {
        "Work Experience": "3+ years in retail sales management",
        "Education": "Bachelor's degree in Marketing",
        "Skills": "Sales Strategy, Customer Service, Negotiation",
        "Languages": "English, Spanish"
    },
    "TEACHER": {
        "Work Experience": "5+ years as a high school mathematics teacher",
        "Education": "Bachelor's in Education",
        "Skills": "Lesson Planning, Classroom Management, Subject Knowledge",
        "Languages": "English, French"
    }
}

# Step 1: Handle Missing Values
# If critical columns have missing values, replace them with directory-specific data
critical_columns = ["Work Experience", "Education", "Skills", "Languages"]
for column in critical_columns:
    for directory, content in directory_to_content.items():
        cv_data = cv_data.withColumn(
            column,
            when((col("directory") == directory) & isnull(col(column)), lit(content[column])).otherwise(col(column))
        )

# Step 2: Remove Unwanted Columns (directory and filename may not be needed)
# cv_data = cv_data.drop("directory", "filename")

# Step 3: Remove Duplicates
cv_data = cv_data.dropDuplicates()

# Step 4: Trim whitespace and standardize text (lowercase) for string columns
string_columns = [field.name for field in cv_data.schema.fields if field.dataType.simpleString() == "string"]
for column in string_columns:
    cv_data = cv_data.withColumn(column, trim(col(column)))  # Trim whitespaces
    cv_data = cv_data.withColumn(column, lower(col(column)))  # Convert to lowercase


# Show the cleaned data
cv_data.show(truncate=False)

# Step 7: Convert Spark DataFrame to Pandas DataFrame for saving to CSV
pandas_df = cv_data.toPandas()

# Save the cleaned data to a CSV file using Pandas
pandas_df.to_csv("cleaned_cv_data.csv", index=False)

# Stop Spark Session
spark.stop()
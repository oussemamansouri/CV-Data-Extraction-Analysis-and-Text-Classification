from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower, lit
import pandas as pd

# Initialize Spark Session
spark = SparkSession.builder.appName('cleaning_cv_data').getOrCreate()

# Load CSV into a Spark DataFrame
cv_data = spark.read.csv("./cv_data.csv", header=True, inferSchema=True)

# Print schema to understand the data
cv_data.printSchema()

# Step 1: Handle Missing Values
# If critical columns have missing values, replace them with 'Not available'
critical_columns = ["Work Experience", "Education", "Skills", "Languages"]
for column in critical_columns:
    cv_data = cv_data.fillna({column: "Not available"})

# Step 2: Remove Unwanted Columns (directory and filename may not be needed)
cv_data = cv_data.drop("directory", "filename")

# Step 3: Remove Duplicates
cv_data = cv_data.dropDuplicates()

# Step 4: Trim whitespace and standardize text (lowercase) for string columns
string_columns = [field.name for field in cv_data.schema.fields if field.dataType.simpleString() == "string"]
for column in string_columns:
    cv_data = cv_data.withColumn(column, trim(col(column)))  # Trim whitespaces
    cv_data = cv_data.withColumn(column, lower(col(column)))  # Convert to lowercase

# Step 5: Anonymization (if needed, anonymize PII such as names or contact information)
# (Assuming names or other PII may exist in the dataset, though they aren't in the given columns)
# For example, anonymizing names (if they exist) can be done like this:
# cv_data = cv_data.withColumn("name", lit("Anonymized"))

# Step 6: Clean the data for each column more specifically if needed
# For example, if 'Work Experience' contains job titles or company names, ensure proper formatting.
# You might want to remove unnecessary characters, or clean up dates, etc.

# Show the cleaned data (optional for inspection)
cv_data.show(truncate=False)

# Step 7: Convert Spark DataFrame to Pandas DataFrame for saving to CSV
pandas_df = cv_data.toPandas()

# Save the cleaned data to a CSV file using Pandas
pandas_df.to_csv("cleaned_cv_data.csv", index=False)

# Stop Spark Session
spark.stop()

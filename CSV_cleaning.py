from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder.appName('cleaning_data').getOrCreate()

# Load CSV into a DataFrame
cv_data = spark.read.csv("./cv_data.csv", header=True, inferSchema=True)

# Clean the data using Spark SQL
cv_data.printSchema()
cleaned_cv_data = cv_data.na.drop()
from pyspark.sql.functions import col, sum

for column in cleaned_cv_data.columns:
    missing_count = cleaned_cv_data.filter(col(column).isNull()).count()
    print(f"Nombre de lignes manquantes dans la colonne {column}: {missing_count}")

# Show the cleaned data
cleaned_cv_data.show(truncate=False)

# Save the cleaned data to a new CSV file
output_path = "./cleaning_data"
cleaned_cv_data.write.csv(output_path, header=True, mode="overwrite")

# Stop Spark Session
# spark.stop()

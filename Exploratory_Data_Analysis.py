import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data Gathering
# Load the dataset from a CSV file into a pandas DataFrame
df = pd.read_csv('Updated_cv.csv')

# Exploratory Data Analysis
# Display the shape of the DataFrame (number of rows and columns)
print("Shape of the DataFrame (Rows, Columns):", df.shape)

# Display DataFrame information, including data types and non-null counts
print("\nDataframe Information:")
print(df.info())

# Show the distribution of values in the 'Category' column
print("\nCategory Value Counts:")
print(df['Category'].value_counts())

# Visualization - Countplot for Category
# Create a countplot to visualize the distribution of 'Category' values
plt.figure(figsize=(15, 5))
sns.countplot(x='Category', data=df)
plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility
plt.title('Category Distribution')  # Add title to the plot
plt.show()

# Print unique categories in the 'Category' column
print("\nUnique Categories in the 'Category' Column:")
print(df['Category'].unique())

# Prepare data for the pie chart
# Get the count of each category and the unique labels
counts = df['Category'].value_counts()
labels = df['Category'].unique()

# Visualization - Pie Chart for Category Distribution
# Create a pie chart to show the percentage distribution of categories
plt.figure(figsize=(15, 10))
plt.pie(counts, labels=labels, autopct='%1.1f%%', shadow=True, 
        colors=plt.cm.coolwarm(np.linspace(0, 1, len(labels))))
plt.title('Category Distribution (Pie Chart)') 
plt.show()

# Adding a New Analysis: Number of Skills in the Dataset (True/False)
# Example: List of skills that we want to check if they exist in the "Resume" column.
skills = ['Python', 'Java', 'SQL', 'JavaScript', 'Machine Learning', 'R', 'Tableau', 'TensorFlow', 'Keras', 'Scikit-learn']

# For each skill, we will create a new column showing True if the skill is present in the resume, False otherwise
for skill in skills:
    df[skill] = df['Resume'].str.contains(skill, case=False, na=False)

# Check the presence of skills in the dataset
print("\nPresence of Skills (True/False) in the Dataset:")
print(df[skills].sum())  # Summing the True/False values gives the count of occurrences of each skill

# Visualization - Count of True/False for each skill
# Plotting the number of occurrences for each skill (True/False)
plt.figure(figsize=(15, 8))
df[skills].sum().plot(kind='bar', color=['#86bf8c', '#ff7f50'], edgecolor='black')
plt.title('Number of Occurrences for Each Skill (True/False)', fontsize=16)
plt.ylabel('Number of Occurrences', fontsize=12)
plt.xlabel('Skills', fontsize=12)
plt.xticks(rotation=45)
plt.show()



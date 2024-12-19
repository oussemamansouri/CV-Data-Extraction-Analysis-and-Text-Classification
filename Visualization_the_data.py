import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import os

# Visualization function
def visualize_data(csv_filename, export_dir="visualizations"):
    # Load data
    df = pd.read_csv(csv_filename)

    # Ensure export directory exists
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    # Clean up column names by stripping spaces
    df.columns = df.columns.str.strip()

    # Filter out rows with empty or invalid 'directory' values
    df = df[df['directory'].notna() & (df['directory'] != '')]

    # Visualization 1: Count of CVs per directory
    plt.figure(figsize=(10, 6))  # Increase the size
    sns.countplot(data=df, x='directory', order=df['directory'].value_counts().index, hue='directory', palette='Set2', legend=False)
    plt.title('Count of CVs per Directory')
    plt.xlabel('Directory')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9)  # Adjust left and right padding
    plt.savefig(f'{export_dir}/cv_count_per_directory.png')
    plt.close()
    
    # Visualization 2: Length of "Work Experience" text
    df['Work Experience Length'] = df['Work Experience'].fillna('').apply(len)
    plt.figure(figsize=(10, 6))  # Increase the size
    sns.histplot(df['Work Experience Length'], bins=30, kde=True)
    plt.title('Distribution of Work Experience Text Lengths')
    plt.xlabel('Text Length')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9)  # Adjust left and right padding
    plt.savefig(f'{export_dir}/work_experience_length_distribution.png')
    plt.close()

    # Visualization 3: Presence of "Skills" in CVs
    df['Has Skills'] = df['Skills'].notna()
    plt.figure(figsize=(8, 5))  # Increase the size
    sns.countplot(data=df, x='Has Skills', hue='Has Skills', palette='pastel', legend=False)
    plt.title('Presence of Skills in CVs')
    plt.xlabel('Contains Skills')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9)  # Adjust left and right padding
    plt.savefig(f'{export_dir}/presence_of_skills.png')
    plt.close()

    # Visualization 4: Languages Mentioned - Modified to show language counts
    # Step 1: Extract and clean languages data from the 'Languages' column
    all_languages = []
    df['Languages'].dropna().apply(lambda x: all_languages.extend([lang.strip() for lang in x.split(',')]))

    # Step 2: Count the occurrences of each language
    language_counts = Counter(all_languages)

    # Step 3: Sort languages by frequency
    sorted_language_counts = dict(sorted(language_counts.items(), key=lambda item: item[1], reverse=True))

    # Step 4: Plot the languages and their appearance counts (Bar Chart)
    plt.figure(figsize=(12, 6))  # Increase the size for readability
    sns.barplot(x=list(sorted_language_counts.keys()), y=list(sorted_language_counts.values()), palette='Set3')
    plt.title('Language Occurrences in CVs')
    plt.xlabel('Languages')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9)  # Adjust padding for better visualization
    plt.savefig(f'{export_dir}/language_occurrences_bar_chart.png')
    plt.close()

    # Step 5: Pie Chart for language distribution
    plt.figure(figsize=(8, 6))  # Increase the size
    language_counts_series = pd.Series(language_counts)
    language_counts_series.plot.pie(autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set3', len(language_counts_series)))
    plt.title('Distribution of Languages in CVs')
    plt.ylabel('')  # Hide the y-axis label for pie chart
    plt.tight_layout()
    plt.savefig(f'{export_dir}/language_distribution_pie.png')
    plt.close()

    # Visualization 5: Pie chart of 'directory' distribution
    plt.figure(figsize=(8, 6))  # Increase the size
    directory_counts = df['directory'].value_counts()
    directory_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set3', len(directory_counts)))
    plt.title('Distribution of CVs per Directory')
    plt.ylabel('')  # Hide the y-axis label for pie chart
    plt.tight_layout()
    plt.savefig(f'{export_dir}/directory_distribution_pie.png')
    plt.close()

    # Visualization 6: Pie chart of 'Has Skills' distribution
    plt.figure(figsize=(8, 6))  # Increase the size
    skills_counts = df['Has Skills'].value_counts()
    skills_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Pastel1', len(skills_counts)))
    plt.title('Distribution of CVs with Skills')
    plt.ylabel('')  # Hide the y-axis label for pie chart
    plt.tight_layout()
    plt.savefig(f'{export_dir}/has_skills_distribution_pie.png')
    plt.close()

    # Extract all unique skills from the 'Skills' column
    skill_set = set()
    df['Skills'].dropna().apply(lambda x: skill_set.update(x.split(',')))

    # Remove leading/trailing whitespaces from each skill
    skill_set = {skill.strip() for skill in skill_set}

    # Visualization 8: Count of CVs with each skill (Bar chart)
    skill_counts = {skill: df['Skills'].str.contains(skill, case=False, na=False).sum() for skill in skill_set}
    skill_counts = dict(sorted(skill_counts.items(), key=lambda item: item[1], reverse=True))

    plt.figure(figsize=(12, 6))  # Increase the size
    plt.bar(skill_counts.keys(), skill_counts.values(), color=sns.color_palette('Blues', len(skill_counts)))
    plt.title('Skill Count Across CVs')
    plt.xlabel('Skills')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'{export_dir}/skill_count_bar_chart.png')
    plt.close()

# Main function to run the visualizations
def main():
    # Load the dataset
    df = pd.read_csv("updated_dataset.csv")

    # Visualize the data using different functions
    visualize_data("updated_dataset.csv", export_dir="visualizations")

# Run the main function
if __name__ == "__main__":
    main()

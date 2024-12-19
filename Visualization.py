import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import re

# Visualization function
def visualize_data(csv_filename, export_dir="visualizations"):
    # Load data
    df = pd.read_csv(csv_filename)
    
    # Ensure export directory exists
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # Filter out rows with empty or invalid 'directory' values
    df = df[df['directory'].notna() & (df['directory'] != '')]

    # Visualization 1: Count of CVs per directory
    plt.figure(figsize=(10, 6))  # Increase the size
    sns.countplot(data=df, x='directory', order=df['directory'].value_counts().index)
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
    sns.countplot(data=df, x='Has Skills')
    plt.title('Presence of Skills in CVs')
    plt.xlabel('Contains Skills')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9)  # Adjust left and right padding
    plt.savefig(f'{export_dir}/presence_of_skills.png')
    plt.close()
    
    # Visualization 4: Languages Mentioned
    df['Language Count'] = df['Languages'].fillna('').apply(lambda x: len(x.split(',')))
    plt.figure(figsize=(10, 6))  # Increase the size
    sns.histplot(df['Language Count'], bins=10, kde=False)
    plt.title('Number of Languages Mentioned')
    plt.xlabel('Number of Languages')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9)  # Adjust left and right padding
    plt.savefig(f'{export_dir}/number_of_languages_mentioned.png')
    plt.close()
    
    # Visualization 5: Top Words in "Education"
    education_text = ' '.join(df['Education'].dropna())
    word_counts = Counter(re.findall(r'\b\w+\b', education_text))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
    plt.figure(figsize=(12, 8))  # Increase the size
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Top Words in Education Section')
    plt.axis('off')
    plt.tight_layout()
    plt.subplots_adjust(left=0.1, right=0.9)  # Adjust left and right padding
    plt.savefig(f'{export_dir}/top_words_in_education.png')
    plt.close()

# Visualize the data
visualize_data("updated_dataset.csv", export_dir="visualizations")

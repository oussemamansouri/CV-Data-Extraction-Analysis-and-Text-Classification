import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Visualization function
def visualize_data(csv_filename):
    df = pd.read_csv(csv_filename)
    
    # Visualization 1: Count of CVs per directory
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='directory', order=df['directory'].value_counts().index)
    plt.title('Count of CVs per Directory')
    plt.xlabel('Directory')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # Visualization 2: Length of "Work Experience" text
    df['Work Experience Length'] = df['Work Experience'].fillna('').apply(len)
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Work Experience Length'], bins=30, kde=True)
    plt.title('Distribution of Work Experience Text Lengths')
    plt.xlabel('Text Length')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()
    
    # Visualization 3: Presence of "Skills" in CVs
    df['Has Skills'] = df['Skills'].notna()
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x='Has Skills')
    plt.title('Presence of Skills in CVs')
    plt.xlabel('Contains Skills')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()
    
    # Visualization 4: Languages Mentioned
    df['Language Count'] = df['Languages'].fillna('').apply(lambda x: len(x.split(',')))
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Language Count'], bins=10, kde=False)
    plt.title('Number of Languages Mentioned')
    plt.xlabel('Number of Languages')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()
    
    # Visualization 5: Top Words in "Education"
    from collections import Counter
    from wordcloud import WordCloud
    education_text = ' '.join(df['Education'].dropna())
    word_counts = Counter(re.findall(r'\b\w+\b', education_text))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Top Words in Education Section')
    plt.axis('off')
    plt.show()
    
    
    
# Visualize the data
visualize_data("cv_data.csv")    
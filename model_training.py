import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load your dataset
df = pd.read_csv('updated_dataset.csv')

# Check for missing values and handle them
df = df.dropna(subset=['Category', 'Work Experience', 'Education', 'Skills', 'Languages'])

# Concatenate the text columns (Work Experience, Education, Skills, Languages)
df['Text'] = df['Work Experience'] + ' ' + df['Education'] + ' ' + df['Skills'] + ' ' + df['Languages']

# Prepare the features and target variable
X = df['Text']
y = df['Category']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Use TF-IDF Vectorizer to convert text data into numerical format
vectorizer = TfidfVectorizer(stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Initialize and train a RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_tfidf, y_train)

# Predict on the test set
y_pred = model.predict(X_test_tfidf)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Print Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred, labels=model.classes_)

# Ensure all classes are present
if conf_matrix.shape[0] < len(model.classes_):
    # Add empty rows or columns if needed
    conf_matrix = np.pad(conf_matrix, ((0, len(model.classes_) - conf_matrix.shape[0]), 
                                        (0, len(model.classes_) - conf_matrix.shape[1])), 
                         mode='constant', constant_values=0)

# Plot Confusion Matrix
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=model.classes_, yticklabels=model.classes_)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

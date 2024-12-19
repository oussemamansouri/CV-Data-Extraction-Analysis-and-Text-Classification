import fitz  # PyMuPDF
import os
import pandas as pd
import re

def clean_text(text):
    """Clean extracted text by removing extra spaces, newlines, and unwanted characters."""
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespaces with a single space
    text = text.strip()  # Remove leading and trailing spaces
    # Remove unwanted characters (e.g., non-breaking spaces, special characters)
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    return text

def extract_text_from_pdf(pdf_path):
    """Extract text from a single PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    
    # Iterate through each page in the PDF and extract text
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    
    return clean_text(text)  # Clean the extracted text

def extract_information_from_text(text):
    """Extract key information from the text of a CV using regex."""
    data = {
        "Work Experience": None,
        "Education": None,
        "Skills": None,
        "Languages": None,
        "directory": None,
        "filename": None
    }
    
    # regex patterns for extracting information
    work_experience_pattern = re.compile(r"(Work\s+Experience|Professional\s+Experience)\s*[:\-]?\s*(.*?)(Education|Skills|Languages)", re.DOTALL)
    education_pattern = re.compile(r"(Education|Academic\s+Background)\s*[:\-]?\s*(.*?)(Skills|Languages)", re.DOTALL)
    skills_pattern = re.compile(r"(Skills|Key\s+Skills)\s*[:\-]?\s*(.*?)(Languages|End)", re.DOTALL)
    languages_pattern = re.compile(r"(Languages)\s*[:\-]?\s*(.*)", re.DOTALL)
    
    # Extract information using the regex patterns
    work_experience_match = work_experience_pattern.search(text)
    education_match = education_pattern.search(text)
    skills_match = skills_pattern.search(text)
    languages_match = languages_pattern.search(text)
    
    # Store matches if found
    if work_experience_match:
        data["Work Experience"] = clean_text(work_experience_match.group(2).strip())
    if education_match:
        data["Education"] = clean_text(education_match.group(2).strip())
    if skills_match:
        data["Skills"] = clean_text(skills_match.group(2).strip())
    if languages_match:
        data["Languages"] = clean_text(languages_match.group(2).strip())

    return data

def extract_information_from_pdfs_in_directory(directory_path):
    """Extract information from all PDF files in a directory and its subdirectories."""
    all_data = []
    
    # Traverse all directories and subdirectories
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(root, filename)
                extracted_text = extract_text_from_pdf(pdf_path)
                extracted_data = extract_information_from_text(extracted_text)
                
                # Add directory and filename for reference
                extracted_data["directory"] = os.path.basename(root)
                extracted_data["filename"] = filename
                
                # Append the extracted data
                all_data.append(extracted_data)
    
    return all_data

def save_to_csv(extracted_data, csv_filename="csv_data/cv_data.csv"):
    """Save the extracted data to a CSV file."""
    df = pd.DataFrame(extracted_data)
    df.to_csv(csv_filename, index=False)
    print(f"Data saved to {csv_filename}")


directory_path = "./cv_pdfs_collection"  # Path to the main 'data' directory
extracted_data = extract_information_from_pdfs_in_directory(directory_path)

# Save the extracted data to a CSV
save_to_csv(extracted_data)

# Print the extracted data
for data in extracted_data:
    print(f"Data from {data['directory']} - {data['filename']}:\n{data}\n")

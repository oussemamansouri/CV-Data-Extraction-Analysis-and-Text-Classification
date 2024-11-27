import fitz  # PyMuPDF
import os
import pandas as pd
import re

def extract_text_from_pdf(pdf_path):
    """Extract text from a single PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    
    # Iterate through each page in the PDF and extract text
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    
    return text

def extract_information_from_text(text):
    """Extract key information from the text of a CV using regex."""
    data = {
        "Full Name": None,
        "Contact Info": None,
        "Summary": None,
        "Work Experience": None,
        "Education": None,
        "Skills": None,
        "Languages": None
    }
    
    # Example regex patterns for extracting information
    name_pattern = re.compile(r"(?:Name|Full\s+Name)\s*[:\-]?\s*([A-Za-z\s]+)")
    contact_pattern = re.compile(r"(\+?[0-9]{1,3}[ -]?)?(\(?\d{3}\)?[ -]?\d{3}[ -]?\d{4})") 
    summary_pattern = re.compile(r"(Summary|Profile|Objective)\s*[:\-]?\s*(.*?)(Work Experience|Skills|Education)", re.DOTALL)
    work_experience_pattern = re.compile(r"(Work\s+Experience|Professional\s+Experience)\s*[:\-]?\s*(.*?)(Education|Skills|Languages)", re.DOTALL)
    education_pattern = re.compile(r"(Education|Academic\s+Background)\s*[:\-]?\s*(.*?)(Skills|Languages)", re.DOTALL)
    skills_pattern = re.compile(r"(Skills|Key\s+Skills)\s*[:\-]?\s*(.*?)(Languages|End)", re.DOTALL)
    languages_pattern = re.compile(r"(Languages)\s*[:\-]?\s*(.*)", re.DOTALL)
    
    # Extract information using the regex patterns
    name_match = name_pattern.search(text)
    contact_match = contact_pattern.search(text)
    summary_match = summary_pattern.search(text)
    work_experience_match = work_experience_pattern.search(text)
    education_match = education_pattern.search(text)
    skills_match = skills_pattern.search(text)
    languages_match = languages_pattern.search(text)
    
    # Store matches if found
    if name_match:
        data["Full Name"] = name_match.group(1).strip()
    if contact_match:
        data["Contact Info"] = contact_match.group(0).strip()
    if summary_match:
        data["Summary"] = summary_match.group(2).strip()
    if work_experience_match:
        data["Work Experience"] = work_experience_match.group(2).strip()
    if education_match:
        data["Education"] = education_match.group(2).strip()
    if skills_match:
        data["Skills"] = skills_match.group(2).strip()
    if languages_match:
        data["Languages"] = languages_match.group(2).strip()

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

def save_to_csv(extracted_data, csv_filename="cv_data.csv"):
    """Save the extracted data to a CSV file."""
    df = pd.DataFrame(extracted_data)
    df.to_csv(csv_filename, index=False)
    print(f"Data saved to {csv_filename}")

# Example usage
directory_path = "./data"  # Path to the main 'data' directory
extracted_data = extract_information_from_pdfs_in_directory(directory_path)

# Save the extracted data to a CSV
save_to_csv(extracted_data)

# Optionally, print the extracted data
for data in extracted_data:
    print(f"Data from {data['directory']} - {data['filename']}:\n{data}\n")

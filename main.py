import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Initialize a string to store the extracted text
    text = ""
    
    # Iterate through each page in the PDF
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")  # Extract text from the page
        
    return text


import os

def extract_text_from_pdfs_in_directory(directory_path):
    all_texts = {}
    
    # Loop through all PDF files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory_path, filename)
            extracted_text = extract_text_from_pdf(pdf_path)
            all_texts[filename] = extracted_text  # Store the extracted text with the filename as key
    
    return all_texts

# Example usage
directory_path = "./data/ACCOUNTANT"
pdf_texts = extract_text_from_pdfs_in_directory(directory_path)

# Print text of each PDF file
for filename, text in pdf_texts.items():
    print(f"Text from {filename}:\n{text}\n")





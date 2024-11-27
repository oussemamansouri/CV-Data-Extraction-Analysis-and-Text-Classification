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


pdf_path = "./data/TEACHER/10504237.pdf"
extracted_text = extract_text_from_pdf(pdf_path)
print(extracted_text)  # Print the extracted text to see it

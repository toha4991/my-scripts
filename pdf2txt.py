# this script reads a pdf file (or a page of it) and converts it into a txt format

import sys                           # a lib to open files
from PyPDF2 import PdfReader     # to read from PDF files

def pdf_to_text(pdf_path, start_page=None, end_page=None):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        
        # Determine the range of pages to convert
        if start_page is None:
            start_page = 0
        else:
            start_page = int(start_page) - 1
        
        if end_page is None:
            end_page = num_pages
        else:
            end_page = int(end_page)
        
        # Extract text from the specified pages
        text = ""
        for page_num in range(start_page, end_page):
            page = reader.pages[page_num]
            text += page.extract_text()
    
    return text

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <pdf_path> [start_page] [end_page]")
    else:
        pdf_path = sys.argv[1]
        start_page = sys.argv[2] if len(sys.argv) > 2 else None
        end_page = sys.argv[3] if len(sys.argv) > 3 else None
        
        text = pdf_to_text(pdf_path, start_page, end_page)

        print(text)
        
        # Save the extracted text to a .txt file
        with open("output.txt", "w") as output_file:
            output_file.write(text)
import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path, skip_pages=set()):
    """
    Extracts text from a PDF, skipping specified pages and removing a dynamically generated footer.

    :param pdf_path: Path to the PDF file.
    :param skip_pages: A set of page numbers to skip, starting from 1.
    :return: Extracted and cleaned text from the PDF.
    """
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            # Skip specified pages (adjusting for zero indexing)
            if page_num + 1 in skip_pages:
                continue
            
            page_text = doc.load_page(page_num).get_text()

            # Remove header using regex
            header_pattern = re.compile(r"Certified Tester\s+AI Testing \(CT-AI\)\s+Syllabus\s*", re.MULTILINE)
            page_text = re.sub(header_pattern, '', page_text)

            # Remove footer using regex
            footer_pattern = re.compile(r"v\d+\.\d+\s+Page \d+ of \d+\s+\d{4}-\d{2}-\d{2}\s+© International Software Testing Qualifications Board\s*", re.MULTILINE)
            page_text = re.sub(footer_pattern, '', page_text)

            # Remove dynamically generated footer text using regex
            footer_pattern = re.compile(r"v\d+\.\d+ Page \d+ of \d+ \d{4}-\d{2}-\d{2}\n© International Software Testing Qualifications Board")
            page_text = re.sub(footer_pattern, '', page_text)

            # Remove static header text
            #header_text = "Certified Tester\nAI Testing (CT-AI)\nSyllabus"
            #page_text = page_text.replace(header_text, '')
            
            text += page_text + "\n"  # Add a newline to separate pages
            
    return text

# Example usage
pdf_path = "C:\code\linkedInPost\ISTQB_CT-AI_Syllabus_v1.0_mghocmT.pdf"
# Assuming the first and second pages are title and TOC
extracted_text = extract_text_from_pdf(pdf_path, skip_pages={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99})
# Save the cleaned text to a new file
with open('cleaned_book.txt', 'w', encoding='utf-8') as file:
    file.write(extracted_text)


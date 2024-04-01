import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path, skip_pages=set()):
    """
    Extracts text from a PDF, skipping specified pages, and removing headers, footers,
    as well as various types of references including sections, chapters, and citation keys.

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

            # Remove headers, footers, and references using regex
            patterns_to_remove = [
                r"Certified Tester\s+AI Testing \(CT-AI\)\s+Syllabus\s*",
                r"v\d+\.\d+\s+Page \d+ of \d+\s+\d{4}-\d{2}-\d{2}\s+© International Software Testing Qualifications Board\s*",
                r"\(see Section \d+\.\d+\)",
                r"\(see \[\w+\] for more details\)",
                r"\(see\s+.*?\)",
                r"\[see\s+.*?\]",
                r"– see.*",
                r"as shown on.*",
                r"shown in.*",
                r"See.*",
                r"Figure\s+\d+:\s+.*?",
                r"\[\w+\d*\]",  # Matches references like [B05]
                r"\(see Chapter \d+\)"  # Matches phrases like "(see Chapter 5)"
            ]

            for pattern in patterns_to_remove:
                page_text = re.sub(pattern, '', page_text, flags=re.MULTILINE)
            
            text += page_text.strip() + "\n\n"  # Add stripped page text with two newlines as separator
            
    return text

# Example usage
pdf_path = "C:\code\linkedInPost\ISTQB_CT-AI_Syllabus_v1.0_mghocmT.pdf"
# Assuming the first and second pages are title and TOC
extracted_text = extract_text_from_pdf(pdf_path, skip_pages={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 20, 25, 32, 39, 44, 49, 57, 65, 73, 76, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99})
# Save the cleaned text to a new file
with open('cleaned_book.txt', 'w', encoding='utf-8') as file:
    file.write(extracted_text)


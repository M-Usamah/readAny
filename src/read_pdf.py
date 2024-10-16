from pypdf import PdfReader
import re
from num2words import num2words

def pdf_file(file):
    return PdfReader(file)

def total_pages(file) -> int:
    reader = pdf_file(file)
    return len(reader.pages)

def read_single_page_text(file, page_num) -> tuple[int, str]:
    reader = pdf_file(file)
    if 0 <= page_num < len(reader.pages):
        page = reader.pages[page_num]
        return page_num, page.extract_text()
    else:
        raise ValueError(f"Page number {page_num} is out of range")

def convert_numbers_to_words(text):
    def replace_number(match):
        number = match.group(0)
        try:
            return num2words(float(number))
        except ValueError:
            return number  # If conversion fails, return the original number

    # Regular expression to match numbers (including decimals)
    pattern = r'\b\d+(?:\.\d+)?\b'
    
    # Replace all numbers in the text
    return re.sub(pattern, replace_number, text)

def read_and_convert_page(file, page_num) -> tuple[int, str]:
    page_num, text = read_single_page_text(file, page_num)
    contant =  convert_numbers_to_words(text)
    return page_num, contant

if __name__ == "__main__":
    file_path = 'CHEATING AUTOMATIC LLM BENCHMARKS: NULL MODELS ACHIEVE HIGH WIN RATES.pdf'
    converted_text = read_and_convert_page(file_path, 0)
    print(converted_text[1])
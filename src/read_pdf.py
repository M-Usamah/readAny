from pypdf import PdfReader

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

if __name__ == "__main__":
    print(read_single_page_text('../Artificial Intelligence A Modern Approach.pdf', 22)[1])
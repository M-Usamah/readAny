from pypdf import PdfReader

def pdf_file(file):
    return PdfReader(file)

def total_pages(file) -> int:
    Pages = pdf_file(file)
    return len(Pages.pages)
    
def read_single_page_text(pages,page_num) -> str:
    file = pdf_file(pages)
    page = file.pages[page_num]
    return page.extract_text()
    
if __name__ == "__main__":
    print(read_single_page_text('../Artificial Intelligence A Modern Approach.pdf',20))
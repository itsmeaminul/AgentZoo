from PyPDF2 import PdfReader
from io import BytesIO

def process_pdf(file_content: bytes) -> str:
    pdf_file = BytesIO(file_content)
    reader = PdfReader(pdf_file)
    text = "\n".join([page.extract_text() for page in reader.pages])
    return text
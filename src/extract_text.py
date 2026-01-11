import pdfplumber

def extract_text_from_pdf(file_stream):
    """
    Extracts text from a PDF file stream (compatible with Streamlit).
    """
    text = ""
    try:
        with pdfplumber.open(file_stream) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""
    
    return text
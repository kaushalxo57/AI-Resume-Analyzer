import pypdf
import logging

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts plain text from an uploaded PDF file or file path.
    Supports multi-page documents and handles errors gracefully.
    """
    text = ""
    try:
        # pypdf can read from a file path or a file-like object (like Streamlit's UploadedFile)
        reader = pypdf.PdfReader(pdf_file)
        
        for page_idx, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        # Clean extra white spaces and duplicate newlines
        lines = [line.strip() for line in text.split('\n')]
        cleaned_text = "\n".join([line for line in lines if line])
        return cleaned_text
        
    except Exception as e:
        logger.error(f"Error parsing PDF: {e}")
        raise RuntimeError(f"Failed to parse PDF: {str(e)}")

import fitz


def extract_pdf_text(file_bytes):
    """
    Extract text from a PDF document.
    """

    text = ""

    try:
        document = fitz.open(stream=file_bytes, filetype="pdf")

        for page in document:
            text += page.get_text()

        document.close()

    except Exception:
        return ""

    return text


def get_pdf_page_count(file_bytes):
    """
    Return number of pages in a PDF.
    """

    try:
        document = fitz.open(stream=file_bytes, filetype="pdf")

        pages = len(document)

        document.close()

        return pages

    except Exception:
        return 0

import fitz 
import pytesseract
from PIL import Image
import io
import os
from dotenv import load_dotenv
from chunker import chunk_text

load_dotenv()

TESSERACT_PATH = os.getenv("TESSERACT_CMD")
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def load_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):

        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes("png")

        image = Image.open(io.BytesIO(img_bytes))

        text = pytesseract.image_to_string(image)
        full_text += text + "\n"

    return full_text


if __name__ == "__main__":
    content = load_pdf("economics.pdf")
    chunks = chunk_text(content)
    print(f"Total chunks created: {len(chunks)}")
    print("/n************************************************/n")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:\n{chunk}\n")
    print("/n************************************************/n")
    print("\nDone")

import os
import re
import json
import pytesseract
import pdfplumber
import spacy
import docx
import cv2
import fitz  # PyMuPDF for handling images in PDFs
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Function to check if a PDF contains selectable text
def is_text_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                return True
    return False

def extract_text_from_pdf(pdf_path):
    extracted_text = ""
    
    if is_text_pdf(pdf_path):
        # Extract text from text-based PDFs
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"
    else:
        # Extract text from scanned PDFs using OCR
        extracted_text = extract_text_from_scanned_pdf(pdf_path)
    
    return extracted_text.strip()

# Function to extract images from scanned PDFs and apply OCR
def extract_text_from_scanned_pdf(pdf_path):
    extracted_text = ""

    def noise_removal(image):
        kernel = np.ones((1, 1), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        image = cv2.medianBlur(image, 3)
        return image

    def thin_font(image):
        image = cv2.bitwise_not(image)
        kernel = np.ones((2,2), np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return image

    def thick_font(image):
        image = cv2.bitwise_not(image)
        kernel = np.ones((2,2), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return image

    def remove_borders(image):
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cntsSorted = sorted(contours, key=lambda x: cv2.contourArea(x))
            cnt = cntsSorted[-1]
            x, y, w, h = cv2.boundingRect(cnt)
            crop = image[y:y+h, x:x+w]
            return crop
        return image  # Return original image if no contours found

    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            for img_index, img in enumerate(doc[page_num].get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_np = np.frombuffer(image_bytes, dtype=np.uint8)
                image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

                # Preprocessing Steps
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                processed_image = cv2.adaptiveThreshold(
                    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY, 31, 2
                )

                processed_image = noise_removal(processed_image)
                processed_image = thin_font(processed_image)  # Try thin font first
                processed_image = thick_font(processed_image)  # Then thick font
                processed_image = remove_borders(processed_image)

                # OCR Extraction
                text = pytesseract.image_to_string(processed_image)
                extracted_text += text + "\n"

    return extracted_text.strip()


# Function to extract text from Word documents
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

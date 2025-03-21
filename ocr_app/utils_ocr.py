import pytesseract
import cv2
import numpy as np
from pdf2image import convert_from_path
from docx import Document as DocxDocument
from PIL import Image
def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)[1]
    text = pytesseract.image_to_string(img)
    return text

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(np.array(image))
    return text

def extract_text_from_word(word_path):
    doc = DocxDocument(word_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text
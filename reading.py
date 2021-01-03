# reading.py 读入各类数据
import pandas as pd
import docx
from pdfminer.high_level import extract_text

def readExcel(file_path, sheet_name):
    # xlsx documents
    # df = pd.read_excel(r'Minutes_Excel/Project_Data.xlsx', sheet_name='All')
    output = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
    return output

def readWord(file_path):
    # docx documents
    doc = docx.Document(file_path)
    output = ""
    for para in doc.paragraphs:
        output += para.text + "\n"
    return output

def readPDF(file_path):
    # PDF documents
    output = extract_text(file_path)
    return output

def readPDF_ocr(file_path):
    # scanned PDF documents
    out

if __name__ == "__main__":
    pass
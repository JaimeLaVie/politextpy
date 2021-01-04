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

def pdf2img(PDF_file, first_page=1, last_page=1, dpi=500):
    # Convert pdf to jpg files, this is for reading scanned PDF files whilch cannot be processed by readPDF(). Scanned PDF files should first 
    # be converted into jpg files, and then be processed by readJPG(). See sample codes below:
    """ 
    first_page = 6
    last_page = 10
    dpi = 500
    path = os.getcwd()
    PDF_file = "Execution Version PPA.pdf"
    target_folder = path + '\\' + PDF_file[:-4] + '_page_' + str(first_page) + '_' + str(last_page)
    if os.path.exists(target_folder):
        os.remove(target_folder)
    os.mkdir(target_folder)
    pdf2img(PDF_file, first_page, last_page, dpi)
    file_paths = []
    for i in range(first_page, last_page+1):
        file_paths.append(target_folder + '\\' + "page_" + str(i) + ".jpg")
    recognizer(file_paths, target_folder) 
    """

    print("Converting the PDF file to images (.jpg)...")
    pages = convert_from_path(PDF_file, dpi, first_page=first_page, last_page=last_page)

    # Counter to store images of each page of PDF to image 
    image_counter = 0

    # Iterate through all the pages stored above 
    for page in pages:
        print("Page " + str(first_page + image_counter))
        # Declaring filename for each page of PDF as JPG 
        # For each page, filename will be: 
        # PDF page 1 -> page_1.jpg 
        # PDF page 2 -> page_2.jpg 
        # PDF page 3 -> page_3.jpg 
        # .... 
        # PDF page n -> page_n.jpg 
        filename = "page_" + str(first_page + image_counter) + ".jpg"

        # Save the image of the page in system 
        page.save(target_folder + '\\' + filename, 'JPEG')

        # Increment the counter to update filename
        image_counter = image_counter + 1

    return image_counter  # Variable to get count of total number of pages

def readJPG(file_paths, target_folder):
    # file_paths should be a list of paths of the jpg images, and the order of the jpg files is the same as they appear in the output txt file.
    # This function can be used independently to extract texts in jpg files, or it can also work together with pdf2img() to recognize texts 
    # in scanned PDF files. See sample codes above (in pdf2img()).

    print("Recognizing texts in the images...")

    # Creating a text file to write the output
    outfile = "text.txt"

    f = open(target_folder + '\\' + outfile, "a")

    for filename in file_paths:
        # Set filename to recognize text from
        # filename = "page_" + str(i) + ".jpg"
        print("Picture name: " + filename)

        # Recognize the text as string in image using pytesserct
        text = str(((pytesseract.image_to_string(Image.open(filename)))))

        # The recognized text is stored in variable text
        # Any string processing may be applied on text
        # Here, basic formatting has been done:
        # In many PDFs, at line ending, if a word can't
        # be written fully, a 'hyphen' is added.
        # The rest of the word is written in the next line
        # Eg: This is a sample text this word here GeeksF-
        # orGeeks is half on first line, remaining on next.
        # To remove this, we replace every '-\n' to ''.
        text = text.replace('-\n', '')

        # Finally, write the processed text to the file.
        f.write('\n------------------------------------------------------------------\n')
        f.write('------------- ' + filename + ' -------------\n')
        f.write('------------------------------------------------------------------\n\n')
        f.write(text)

        # Close the file after writing all the text.
    f.close()

if __name__ == "__main__":
    pass
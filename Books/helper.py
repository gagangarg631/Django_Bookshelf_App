import os
from PyPDF2 import PdfFileReader, PdfFileWriter

from pdf2image import convert_from_path
from thumbnail import generate_thumbnail
import random
import string

def saveThumbnail(in_file, out_file, img_name):
    name,ext = os.path.splitext(in_file)
    out_file = os.path.join(out_file, img_name + ".jpg")
    if ext == ".mp4":
        options = {
            'trim': False,
            'height': 300,
            'width': 300,
            'quality': 85,
            'type': 'thumbnail'
        }
        
        generate_thumbnail(in_file, out_file, options)
    
    elif ext == ".pdf":
        pass


def toImage(path,outputDir,fileName):
    images = convert_from_path(path)
    images[0].save(os.path.join(outputDir, str(fileName) + ".jpg"))
    os.remove(path)

def getBookTitle(path):
    pdf = PdfFileReader(path)
    pdf_meta = pdf.getDocumentInfo()
    title = pdf_meta.title if pdf_meta.title else "Unknown"
    return title

def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]

    pdf = PdfFileReader(path)
    for page in range(1):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        # output_filename = '{}_page_{}.pdf'.format(
        #     fname, page+1)
        output_filename = 'firstPage.pdf'
 
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        return output_filename
        
def saveFirstPage(path,outputDir,fileName):
    pdf = pdf_splitter(path)
    img = toImage(pdf,outputDir,fileName)
    

if __name__ == '__main__':
    path = 'Regression Modeling Strategies_ With Applications to Linear Models, Logistic and Ordinal Regression, and Survival Analysis ( PDFDrive ).pdf'
    pdf_splitter(path)

import os
from PyPDF2 import PdfFileReader, PdfFileWriter

# define the page ranges to extract from the PDF
page_range1 = (0, 4)  # first 5 pages
page_range2 = (5, 9)  # next 5 pages

# define the root folder where PDF files are located
root_folder = 'path/to/root/folder'

# define the specific PDF file name to extract
pdf_file_name = 'example.pdf'

# loop through all subfolders and files in the root folder
for subdir, dirs, files in os.walk(root_folder):
    # get the last part of the subfolder path as the suffix to add to the PDF names
    suffix = os.path.basename(os.path.normpath(subdir))
    for file_name in files:
        # check if the file is a PDF file and has the specified name
        if file_name.endswith('.pdf') and file_name == pdf_file_name:
            # open the PDF file in read mode
            with open(os.path.join(subdir, file_name), 'rb') as file:
                # read the PDF file with PyPDF2
                pdf = PdfFileReader(file)
                # get the total number of pages in the PDF
                num_pages = pdf.getNumPages()
                # create a PdfFileWriter object to write the extracted PDFs
                writer = PdfFileWriter()
                # extract the first page range and add to the writer
                for page_num in range(*page_range1):
                    writer.addPage(pdf.getPage(page_num))
                # write the first extracted PDF to disk
                with open(os.path.join(subdir, f'{file_name.split(".")[0]}_{suffix}_part1.pdf'), 'wb') as output_file:
                    writer.write(output_file)
                # create a new PdfFileWriter object for the second extracted PDF
                writer = PdfFileWriter()
                # extract the second page range and add to the writer
                for page_num in range(*page_range2):
                    writer.addPage(pdf.getPage(page_num))
                # write the second extracted PDF to disk
                with open(os.path.join(subdir, f'{file_name.split(".")[0]}_{suffix}_part2.pdf'), 'wb') as output_file:
                    writer.write(output_file)

import os
from PyPDF2 import PdfReader, PdfWriter

# define the root folder where PDF files are located
root_folder = 'D:\pdf extract test'

# define the page ranges to extract from the PDF
page_range1 = (17, 20)  # pages 18-20
page_range2 = (20, 22)  # pages 21-22

# loop through all subfolders and files in the root folder
for subdir, dirs, files in os.walk(root_folder):
    for file_name in files:
        # check if the file is a PDF file named App.pdf
        if file_name == 'App.pdf':
            # open the PDF file in read mode
            with open(os.path.join(subdir, file_name), 'rb') as file:
                # read the PDF file with PyPDF2
                pdf = PdfReader(file)
                # create a PdfWriter object to write the extracted PDFs
                writer = PdfWriter()
                # extract the first page range and add to the writer
                for page_num in range(*page_range1):
                    writer.add_page(pdf.pages[page_num])
                # get the parent folder name to use in the output file name
                parent_folder = os.path.basename(os.path.normpath(subdir))
                # write the first extracted PDF to disk with the folder name as a prefix
                with open(os.path.join(subdir, f'{parent_folder}_part1.pdf'), 'wb') as output_file:
                    writer.write(output_file)
                # create a new PdfWriter object for the second extracted PDF
                writer = PdfWriter()
                # extract the second page range and add to the writer
                for page_num in range(*page_range2):
                    writer.add_page(pdf.pages[page_num])
                # write the second extracted PDF to disk with the folder name as a prefix
                with open(os.path.join(subdir, f'{parent_folder}_part2.pdf'), 'wb') as output_file:
                    writer.write(output_file)

import os
import getpass
import re
from PyPDF2 import PdfReader, PdfWriter

print('Enter correct username and password combo to continue')
count=0
while count < 3:
    username = input('Enter username: ')
    password = input('Enter password: ')
    if password=='8595' and username=='admin':
        print('Access granted')
        # define the root folder where PDF files are located
        root_folder = 'D:\pdf extract test'

        # define the page ranges to extract from the PDF
        page_range1 = (17, 20)  # pages 18-20
        page_range2 = (20, 22)  # pages 21-22

        # define the regex pattern to match against the file names
        file_pattern = re.compile(r'(?i)^App\w*\.pdf$')


        # loop through all subfolders and files in the root folder
        for subdir, dirs, files in os.walk(root_folder):
            for file_name in files:
                # check if the file is a PDF file named App.pdf
                if file_pattern.match(file_name):
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
                        split_at_comma = parent_folder.split(',')
                        last_names = split_at_comma[0]
                        first_name = (split_at_comma[1].strip(' ').split(' '))[0]
                        combined_name = last_names + ', ' + first_name
                        ##old method do not use first_two_words = ' '.join(parent_folder.split()[:2])
                        # write the first extracted PDF to disk with the folder name as a prefix
                        with open(os.path.join(subdir, f'DHS 11000 {combined_name}.pdf'), 'wb') as output_file:
                            writer.write(output_file)
                        # create a new PdfWriter object for the second extracted PDF
                        writer = PdfWriter()
                        # extract the second page range and add to the writer
                        for page_num in range(*page_range2):
                            writer.add_page(pdf.pages[page_num])
                        # write the second extracted PDF to disk with the folder name as a prefix
                        with open(os.path.join(subdir, f'BIRD {combined_name}.pdf'), 'wb') as output_file:
                            writer.write(output_file)
        break
    else:
        print('Access denied. Try again.')
        count += 1

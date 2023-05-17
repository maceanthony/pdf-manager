import os
from PyPDF2 import PdfReader, PdfWriter

# Define the file names
input_file_name = 'App.pdf'
output_file_name = 'App2.pdf'

# Get the current directory
current_directory = os.getcwd()

# Construct the input and output file paths
input_file_path = os.path.join(current_directory, input_file_name)
output_file_path = os.path.join(current_directory, output_file_name)

# Open the input PDF file
with open(input_file_path, 'rb') as input_file:
    # Create a PDF reader object
    reader = PdfReader(input_file)

    # Create a PDF writer object
    writer = PdfWriter()

    # Iterate over each page in the input file and add it to the writer
    for page in reader.pages:
        writer.add_page(page)

    # Write the output PDF file
    with open(output_file_path, 'wb') as output_file:
        writer.write(output_file)

print(f"Extracted all pages from '{input_file_name}' to '{output_file_name}'.")

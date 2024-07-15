import os
import sys
from PyPDF2 import PdfReader, PdfWriter

# Check if a file was provided via command line arguments
if len(sys.argv) < 2:
    print("No input file provided.")
    sys.exit(1)

# Get the input file name from the command line arguments
input_file_name = sys.argv[1]

# Split the input file name into name and extension
input_base_name, input_extension = os.path.splitext(input_file_name)

# Ensure the input file has a .pdf extension
if input_extension.lower() != '.pdf':
    print("Input file is not a PDF.")
    sys.exit(1)

# Define the output file name
output_file_name = f"{input_base_name}_ext.pdf"

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

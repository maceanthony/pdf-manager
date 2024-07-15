import os
import re
import shutil
from pypdf import PdfReader, PdfWriter, PdfMerger
from PIL import Image

# Version 1.1

# request password from user
print('Enter correct username and password combo to continue')
count = 0
# three tries
while count < 3:
    username = input('Enter username: ')
    password = input('Enter password: ')
    if password=='8595' and username=='admin':
        password_accepted = True
        print('Access granted')
        break
    else:
        # increase count on failed password
        print('Access denied. Try again.')
        password_accepted = False
        count += 1

if password_accepted == True:
    # define the root folder where PDF files are located
    root_folder = os.getcwd()
    os.chdir( root_folder )

    # define the page ranges to extract from the PDF
    page_range1 = (5, 8)  # pages 6-8
    page_range2 = (1, 3)  # pages 2-3
    page_range3 = (13, 14) # page 14

    # define the regex pattern to match against the file names
    file_pattern = re.compile(r'(?i)^Please Sign your LUKE Application forms\w*\.pdf$')
    merged_pattern = re.compile(r'(?i)^Merged App Dox -- .+\.pdf$')
    fcra_delete = re.compile(r'(?i)^FCRA\w*\.pdf$')
    fcra_certificate_pattern = re.compile(r'(?i)^Summary\w*\.pdf$')
    dhs_file_pattern = re.compile(r'(?i)^DHS 11000\w*\.pdf$')
    bird_file_pattern = re.compile(r'(?i)^BIRD\w*\.pdf$')

    # loop through all subfolders and files in the root folder
    for subdir, dirs, files in os.walk(root_folder):
        for file_name in files:
            # check if there is a pdf matching pattern
            if merged_pattern.match(file_name):
                with open(os.path.join(subdir, file_name), 'rb') as file:
                    parent_folder = os.path.basename(os.path.normpath(subdir))
                    # Generate name and SSN logic
                    split_at_comma = parent_folder.split(',')
                    last_names = split_at_comma[0]
                    first_middle_name = (split_at_comma[1].strip(' ').split(' -'))[0]
                    first_name_only, *middle_initials = map(str.strip, first_middle_name.split(" "))
                    middle_initial_name = f"{' '.join(m[0] for m in middle_initials)}"
                    last_four_num = parent_folder[-4:]
                    if last_four_num.isdigit():
                        last_four_num = last_four_num
                    else:
                        last_four_num = 'XXXX'
                    combined_name = f"{last_names}, {first_name_only} {middle_initial_name} {last_four_num}"
                    combined_name_no_four = f"{last_names}, {first_name_only} {middle_initial_name}"

                    pdf = PdfReader(file)
                    writer = PdfWriter()
                    # Extract the specified page range from the original PDF
                    for page_num in range(page_range2[0], page_range2[1]):
                        writer.add_page(pdf.pages[page_num])
                    
                    # Write the extracted pages to a new PDF named "BIRD {combined_name_no_four}.pdf"
                    output_file_path = os.path.join(subdir, f'BIRD {combined_name_no_four}.pdf')
                    with open(output_file_path, 'wb') as output_file:
                        writer.write(output_file)

                    print(f'Created new PDF: {output_file_path}')
            # check if the file is a PDF file
            if file_pattern.match(file_name):
                # open the PDF file in read mode
                with open(os.path.join(subdir, file_name), 'rb') as file:
                    # get the parent folder name to use in the output file name
                    parent_folder = os.path.basename(os.path.normpath(subdir))
                    # read the PDF file with PyPDF2
                    pdf = PdfReader(file)
                    # create a PdfWriter object to write the extracted PDFs
                    writer = PdfWriter()
                    
                    # Generate name and SSN logic
                    split_at_comma = parent_folder.split(',')
                    last_names = split_at_comma[0]
                    first_middle_name = (split_at_comma[1].strip(' ').split(' -'))[0]
                    first_name_only, *middle_initials = map(str.strip, first_middle_name.split(" "))
                    middle_initial_name = f"{' '.join(m[0] for m in middle_initials)}"
                    last_four_num = parent_folder[-4:]
                    if last_four_num.isdigit():
                        last_four_num = last_four_num
                    else:
                        last_four_num = 'XXXX'
                    combined_name = f"{last_names}, {first_name_only} {middle_initial_name} {last_four_num}"
                    combined_name_no_four = f"{last_names}, {first_name_only} {middle_initial_name}"

                    # Extract the specified page range from the original PDF
                    for page_num in range(page_range1[0], page_range1[1]):
                        writer.add_page(pdf.pages[page_num])
                    
                    # Write the extracted pages to a new PDF named "BIRD {combined_name_no_four}.pdf"
                    output_file_path = os.path.join(subdir, f'DHS 11000 {combined_name_no_four}.pdf')
                    with open(output_file_path, 'wb') as output_file:
                        writer.write(output_file)

                    print(f'Created new PDF: {output_file_path}')

                    for page_num in range(page_range3[0], page_range3[1]):
                        writer.add_page(pdf.pages[page_num])
                    
                    # Write the extracted pages to a new PDF named "BIRD {combined_name_no_four}.pdf"
                    output_file_path = os.path.join(subdir, f'FCRA.pdf')
                    with open(output_file_path, 'wb') as output_file:
                        writer.write(output_file)

                    print(f'Created new PDF: {output_file_path}')
#
                    # assign the DHS file path to a variable for use in shutil
                    file_path_DHS = os.path.join(subdir, f'DHS 11000 {combined_name_no_four}.pdf')
                    # assign the BIRD file path to a variable for use in shutil
                    file_path_BIRD = os.path.join(subdir, f'BIRD {combined_name_no_four}.pdf')
                    # assign FCRA to a file path variable for shutil
                    file_path_FCRA = os.path.join(subdir, f'FCRA.pdf')

                    # make new folder to put items
                    # in format "Sanchez, Mary R LRT COR"
                    # DRT = Del Rio, Eagle Pass, Uvalde. RGV = RGV. Laredo = LRT.
 
                    # LRT
                    if "Laredo" in parent_folder:
                        COR_folder_name = combined_name + " LRT COR"
                        new_folder_path = os.path.join(subdir, COR_folder_name)

                        try:
                            os.mkdir(new_folder_path)
                            print(f"New folder {COR_folder_name} created.")
                        except FileExistsError:
                            print(f"The folder {COR_folder_name} already exists.")

                    # RGV
                    if "RGV" in parent_folder:
                        COR_folder_name = combined_name + " RGV COR"
                        new_folder_path = os.path.join(subdir, COR_folder_name)

                        try:
                            os.mkdir(new_folder_path)
                            print(f"New folder {COR_folder_name} created.")
                        except FileExistsError:
                            print(f"The folder {COR_folder_name} already exists.")

                    # Eagle Pass
                    if "Eagle Pass" in parent_folder:
                        COR_folder_name = combined_name + " DRT-EGT COR"
                        new_folder_path = os.path.join(subdir, COR_folder_name)

                        try:
                            os.mkdir(new_folder_path)
                            print(f"New folder {COR_folder_name} created.")
                        except FileExistsError:
                            print(f"The folder {COR_folder_name} already exists.")
                    
                    # Uvalde
                    if "Uvalde" in parent_folder:
                        COR_folder_name = combined_name + " DRT-UVA COR"
                        new_folder_path = os.path.join(subdir, COR_folder_name)

                        try:
                            os.mkdir(new_folder_path)
                            print(f"New folder {COR_folder_name} created.")
                        except FileExistsError:
                            print(f"The folder {COR_folder_name} already exists.")

                    # Del Rio
                    if "Del Rio" in parent_folder:
                        COR_folder_name = combined_name + " DRT-DRS COR"
                        new_folder_path = os.path.join(subdir, COR_folder_name)

                        try:
                            os.mkdir(new_folder_path)
                            print(f"New folder {COR_folder_name} created.")
                        except FileExistsError:
                            print(f"The folder {COR_folder_name} already exists.")

                    # DRT - commented out, locations are separated above into 3 separate locations
                    """
                    DRT_locations = ["Del Rio", "Eagle Pass", "Uvalde"]

                    if any(location in parent_folder for location in DRT_locations):
                        COR_folder_name = middle_initial_name + " DRT COR"
                        new_folder_path = os.path.join(subdir, COR_folder_name)

                        try:
                            os.mkdir(new_folder_path)
                            print(f"New folder {COR_folder_name} created.")
                            print(new_folder_path)
                        except FileExistsError:
                            print(f"The folder {COR_folder_name} already exists.")
                    """

                    # copy the files to the newly created COR folder
                    #  - uses copy in case file already exists in the desination folder
                    try:
                        shutil.copy(file_path_DHS, new_folder_path)
                        os.remove(file_path_DHS)
                    except FileNotFoundError:
                        print(f"DHS not found {COR_folder_name}")

                    try:
                        shutil.copy(file_path_BIRD, new_folder_path)
                        os.remove(file_path_BIRD)
                    except FileNotFoundError:
                        print(f"BIRD not found {COR_folder_name}")

                    try:
                        shutil.copy(file_path_FCRA, new_folder_path)
                        os.remove(file_path_FCRA)
                    except FileNotFoundError:
                        print(f"FCRA not found {COR_folder_name}")

    # third loop to find all images and conver to pdf format
    for subdir, dirs, files in os.walk(root_folder):
        for file in files:
            
            # check extension of file to see if it is an image
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(subdir, file)
                pdf_path = os.path.join(subdir, f'{os.path.splitext(file)[0]}.pdf')

                # open the image and convert to PDF
                try:
                    image = Image.open(image_path)
                    image.save(pdf_path, 'PDF', resolution=300)
                    print(f"Image '{file}' converted to PDF.")
                except Exception as e:
                    print(f"Error converting image '{file}': {str(e)}")

    # fourth loop to check for citizenship type PDF's and combine them into one file
    target_names = ['pp', 'lpr', 'nat', 'eac', 'lapr', 'lp']

    for subdir, dirs, files in os.walk(root_folder):
        # check against target_names to find files in subdirs
        if any(file.lower().startswith(name) for name in target_names for file in files):
            merger = PdfMerger()

            for file in files:
                # check if file matches one of the target_names
                if any(file.lower().startswith(name) for name in target_names) and file.endswith(('.pdf')):
                    file_path = os.path.join(subdir, file)
                    # add file to merger
                    merger.append(file_path)
                    print(f"File '{file}' added to merger in folder '{subdir}'")

            # output file path for our new PDF within each folder
            output_path = os.path.join(subdir, 'Immigration_Docs.pdf')

            # writed merged PDF and close merger
            with open(output_path, 'wb') as output_file:
                merger.write(output_file)

            merger.close()

            print(f"Combined PDF created in folder '{subdir}': '{output_path}'")

            # finally move that combined file into COR folder
            cor_folder = next((d for d in dirs if d.endswith('COR')), None)
            if cor_folder:
                cor_folder_path = os.path.join(subdir, cor_folder)
                destination_path = os.path.join(cor_folder_path, 'Immigration_Docs.pdf')
                shutil.move(output_path, destination_path)
                print(f"Combined PDF moved to '{destination_path}'")
            else:
                print("No COR folder found, skipping the file movement.")

else: 
    print("Program not ran. Incorrect password")

input("Press enter to exit;")

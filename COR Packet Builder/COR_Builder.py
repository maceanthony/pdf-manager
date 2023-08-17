import os
import re
import shutil
from pypdf import PdfReader, PdfWriter, PdfMerger
from PIL import Image

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
    page_range1 = (17, 20)  # pages 18-20
    page_range2 = (20, 22)  # pages 21-22

    # define the regex pattern to match against the file names
    file_pattern = re.compile(r'(?i)^App\w*\.pdf$')
    fcra_delete = re.compile(r'(?i)^FCRA\w*\.pdf$')

    # loop over files to first see if there is an FCRA - the way this is written
    # there needs to be two loops or it will see the app first and move the FCRA
    # before it is edited
    for subdir, dirs, files in os.walk(root_folder):
        for file_name in files:
            # check if the file is named FCRA
            if fcra_delete.match(file_name):
                # open the PDF in read mode
                with open(os.path.join(subdir, file_name), 'rb') as file:
                    # read PDF with pydf2
                    pdf = PdfReader(file)
                    # create a PdfWriter object to write the extracted PDFs
                    writer = PdfWriter()
                    
                    # check to make sure doc is longer than 6 pages
                    if len(pdf.pages) > 6:
                        # skip first page and remaining pages to writer
                        for page_num in range(1, len(pdf.pages)):
                            writer.add_page(pdf.pages[page_num])
                        # write the page selection to disk
                        with open(os.path.join(subdir, f'FCRA.pdf'), 'wb') as output:
                            writer.write(output)
                        # print what we did
                        parent_folder = os.path.basename(os.path.normpath(subdir))
                        print(f"Removed page 1 from FCRA in {parent_folder}.")


    # loop through all subfolders and files in the root folder
    for subdir, dirs, files in os.walk(root_folder):
        for file_name in files:
            # check if the file is a PDF file named App.pdf
            if file_pattern.match(file_name):
                # open the PDF file in read mode
                with open(os.path.join(subdir, file_name), 'rb') as file:
                    # get the parent folder name to use in the output file name
                    parent_folder = os.path.basename(os.path.normpath(subdir))
                    # read the PDF file with PyPDF2
                    pdf = PdfReader(file)
                    # create a PdfWriter object to write the extracted PDFs
                    writer = PdfWriter()
                    # extract the first page range and add to the writer
                    for page_num in range(*page_range1):
                        writer.add_page(pdf.pages[page_num])
                    # split and make name of file based on parent folder name
                    split_at_comma = parent_folder.split(',')
                    last_names = split_at_comma[0]
                    first_name, *middle_name_parts = map(str.strip, split_at_comma[1].split(' -'))
                    middle_initial = middle_name_parts[0][0] if middle_name_parts else ''
                    combined_name = f"{last_names}, {first_name} {middle_initial}"

                    # old method do not use first_two_words = ' '.join(parent_folder.split()[:2])
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

                    # assign the DHS file path to a variable for use in shutil
                    file_path_DHS = os.path.join(subdir, f'DHS 11000 {combined_name}.pdf')
                    # assign the BIRD file path to a variable for use in shutil
                    file_path_BIRD = os.path.join(subdir, f'BIRD {combined_name}.pdf')
                    # assign FCRA to a file path variable for shutil
                    file_path_FCRA = os.path.join(subdir, f'FCRA.pdf')

                    # make new folder to put items
                    # in format "Sanchez, Mary R LRT COR"
                    # DRT = Del Rio, Eagle Pass, Uvalde. RGV = RGV. Laredo = LRT.

                    # build a new variable for name based on middle initial using combined_name above
                    # combined_name now uses middle name everywhere 08/16/2023
                    #first_name_only, *middle_initials = map(str.strip, first_middle_name.split(" "))
                    #middle_initial_name = f"{last_names}, {first_name_only} {' '.join(m[0] for m in middle_initials)}"
 
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
                        COR_folder_name = combined_name + " DRT-DRT COR"
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

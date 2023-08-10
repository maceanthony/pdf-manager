import os

# define a function to delete empty folders
def delete_empty_folders(directory):
    # topdown=False will delete subdirs first (empty folder within folder then now empty folder)
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)
                print("Deleted empty folder:", folder_path)

# call the function with the current directory as argument
delete_empty_folders(".")
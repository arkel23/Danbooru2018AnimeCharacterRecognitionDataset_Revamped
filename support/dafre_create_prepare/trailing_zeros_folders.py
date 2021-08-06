import os

def getFolders(dir_name):
    list_folders = os.listdir(dir_name)
    print(list_folders)
    print(len(list_folders))
    for folder in list_folders:
        original_folder_name = os.path.join(dir_name, folder)
        new_folder_name = os.path.join(dir_name, folder.zfill(4))
        print(new_folder_name)
        os.rename(original_folder_name, new_folder_name)

def main():
   getFolders('./data/')

main()

from zipfile import ZipFile
from utils.get_all_files import get_all_files

def zip_files(zip_name: str, paths: list):
    zipObj = ZipFile(zip_name, 'w')

    for path in paths:
        if is_folder(path):
            zip_all_folder_files(path, zipObj)
            
        zipObj.write(path)

    zipObj.close()

def is_folder(path):
    return '.' not in path[2:]

def zip_all_folder_files(folder_path: str, zip: ZipFile):
    files = get_all_files(folder_path, ['sql', 'java'])
    for file in files:
        print(f"{folder_path}/{file}")
        zip.write(f"./{file}")
        
    return

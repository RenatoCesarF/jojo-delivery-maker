from pathlib import Path

def get_all_files(directory: str, types: list) -> list:
    files = []
    for f_type in types:
        for file in Path(directory).glob(f"**/*.{f_type}"):
            files.append(file)
    
    return files

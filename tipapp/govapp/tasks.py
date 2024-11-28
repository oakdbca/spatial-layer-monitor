from datetime import datetime
import os



def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formatted_date = d.strftime('%d %b %Y %H:%M:%S')
    return formatted_date

def get_files_list(dir_path, extensions = []):
    files_list = []
    with os.scandir(dir_path) as dir_entries:
        for entry in dir_entries:
            if entry.is_file():
                info = entry.stat()
                files_list.append({"name": entry.name, "path" : entry.path , "last_modified": convert_date(info.st_mtime)})
    return files_list

def get_file_record(dir_path, file_name):
    file_path = os.path.join(dir_path, file_name)
    info = os.stat(file_path)
    return {"name": file_name, "path" : file_path , "last_modified": convert_date(info.st_mtime)}                
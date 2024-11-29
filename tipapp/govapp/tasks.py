import os
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


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
                file_name = entry.name
                if len(extensions) > 0:
                    _, file_extension = os.path.splitext(file_name)
                    if file_extension.lower() in extensions:
                        files_list.append({"name": file_name, "path" : entry.path , "created_at": convert_date(info.st_mtime)})
    return files_list

def get_dir_size(dir_path):
    try:
        root_directory = Path(dir_path)
        return sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
    except Exception as e:
        logger.error(f"Error getting size of directory: {dir_path}")
        logger.error(e)
        return 0

def get_thermal_files(dir_path, page,  offset):
    items = []
    index = 0

    with os.scandir(dir_path) as dir_entries:
        for entry in dir_entries:
            if index >=page * offset and index < (page + 1) * offset:
                info = entry.stat()
                is_dir = not entry.is_file()
                item = {"name": entry.name, "path" : entry.path , "created_at": convert_date(info.st_mtime), "is_dir": is_dir }
                if is_dir:
                    item['size'] = get_dir_size(entry.path+ entry.name)
                else:
                    item['size'] = info.st_size
                items.append(item)
            else:
                items.append({'name': entry.name})
            index += 1
            
    return items

def get_file_record(dir_path, file_name):
    file_path = os.path.join(dir_path, file_name)
    info = os.stat(file_path)
    return {"name": file_name, "path" : file_path , "created_at": convert_date(info.st_mtime)}                
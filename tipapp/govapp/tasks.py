import os
import re
import logging
from datetime import datetime, timezone
from pathlib import Path
import py7zr

from govapp import settings

logger = logging.getLogger(__name__)


def convert_date(timestamp):
    d = datetime.fromtimestamp(timestamp, timezone.utc)
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

def get_thermal_files(dir_path, page, offset, search = ""):
    items = []
    index = 0
    try:
        dir_entries = sorted(os.scandir(dir_path), key=lambda x: (x.is_file(), x.name))
        
        for entry in dir_entries:
            entry_name = entry.name
            if search != "" and not re.search(search, entry_name):
                continue
            if index >=page * offset and index < (page + 1) * offset:
                info = entry.stat()
                is_dir = not entry.is_file()
                item = {"name": entry_name, "path" : entry.path , "created_at": convert_date(info.st_mtime), "is_dir": is_dir }
                if is_dir:
                    item['size'] = get_dir_size(entry.path+ entry_name)
                else:
                    item['size'] = info.st_size
                items.append(item)
            else:
                items.append({'name': entry_name})
            index += 1
    except Exception as e:
        logger.error(f"Error getting thermal files from directory: {dir_path}")
            
    return items

def get_file_record(dir_path, file_name):
    file_path = os.path.join(dir_path, file_name)
    info = os.stat(file_path)
    return {"name": file_name, "path" : file_path , "created_at": convert_date(info.st_mtime)}

def zip_thermal_file_or_folder(dir_path):
    try:
        new_file_path = os.path.join(settings.DOWNLOADS_PATH,'download_'+str(datetime.now().timestamp()).split('.')[0]) 

        download_file_path = f'{new_file_path}.7z'
        if not os.path.exists(dir_path):
            return None           
        
        if os.path.isfile(dir_path):
            with py7zr.SevenZipFile(download_file_path, 'w') as archive:
                archive.write(dir_path)
        else:
            with py7zr.SevenZipFile(download_file_path, 'w') as archive:
                archive.writeall(dir_path)
            
        return download_file_path
    except Exception as e:
        logger.error(f"Error zipping thermal file or folder: {dir_path}")
        return None
    

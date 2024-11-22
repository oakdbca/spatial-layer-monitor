import os
root = "/data/data/projects/thermal-image-processing/thermalimageprocessing/thermal_data"
for path, subdirs, files in os.walk(root):
    for name in files:
        file_plus_path = os.path.join(path, name)
        print (file_plus_path)
        print (os.path.getctime(file_plus_path))
        print (os.stat(file_plus_path).st_size)
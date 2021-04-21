#! /bin/bash
filename=$1
dirname="${filename%.*}"
#mkdir /home/f2quser/Processed_Thermal_Imagery/$dirname
cp /mnt/data/dmp/$filename /home/f2quser/Processed_Thermal_Imagery/$filename
cd /home/f2quser/Processed_Thermal_Imagery
7z x $filename
rm $filename
cd /home/f2quser/

source /home/f2quser/miniconda3/bin/activate
conda activate TI_venv
python miniconda3/envs/TI_venv/Scripts/Thermal_Image_Processing/thermal_image_processing.py  $dirname

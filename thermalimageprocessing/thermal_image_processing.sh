#! /bin/bash
folder_path=`pwd`
echo $folder_path
full_filename=$1
filename="${full_filename%.7z*}.7z"
basename_filename=`basename $filename`
timestamp=$(date +"%Y-%m-%d_%H:%M:%S")
printf "\n%s filename: %s" "$timestamp" "$filename" >> ./logs/log.txt
#if [[ $filename == *.7z ]]; then

dirname="${basename_filename%.*}"
printf "\ndirname: $dirname" >> ./logs/log.txt
sleep 10
echo "STARTING"
echo $filename
cp $filename   $folder_path/thermal_data_processing/$basename_filename
cd $folder_path/thermal_data_processing/
echo "Uncompressing file $filename"

7z x $basename_filename -aoa
rm $basename_filename

echo $dirname
echo "Run pythonscript"
python $folder_path/thermal_image_processing.py  $folder_path/thermal_data_processing/$dirname
end_timestamp=$(date +"%Y-%m-%d_%H:%M:%S")
printf "\n%s %s done" $end_timestamp $dirname  >> ./logs/log.txt

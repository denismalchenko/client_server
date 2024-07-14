#!/bin/bash

files_list=(
  "duet.mp3"
  "matroskin.mp3"
  "picture.jpg"
  "singer.mov"
  "Winnie_the_Pooh.MP3"
)

echo "start list:"
python3 screwdriver.py list
for file in "${files_list[@]}"; do
  echo ""
  echo "upload: $file"
  python3 screwdriver.py upload examples_files/"$file"
  echo "----list:----"
  python3 screwdriver.py list
done
echo ""
echo "upload: duet.mp3"
python3 screwdriver.py upload examples_files/duet.mp3
echo "----list:----"
python3 screwdriver.py list
#!/bin/bash

python delete_unnecessary_data.py before

python prepare_for_gpt.py

while IFS= read -r line; do
$line
done < lines_for_gpt.txt

rm lines_for_gpt.txt

python delete_unnecessary_data.py after

python create_images.py



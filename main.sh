#!/bin/bash

python delete_unnecessary_data.py before

python lines.py S2
while IFS= read -r line; do
$line
done < lines_for_gpt.txt

rm lines_for_gpt.txt

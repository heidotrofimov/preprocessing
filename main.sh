#!/bin/bash

python lines.py S2
while IFS= read -r line; do
echo $line
$line
done < lines_for_gpt.txt

rm lines_for_gpt.txt

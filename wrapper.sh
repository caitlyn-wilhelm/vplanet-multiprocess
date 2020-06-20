#!/usr/bin/env bash

while IFS= read -r line
do
    python multi_process.py $line
done < multi_list.txt

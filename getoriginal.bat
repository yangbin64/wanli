rem head -n 401 ..\10_data\input_data.csv | tail -n 300 | cut -f3- -d, > original2.csv

python randomselect.py input2.csv original2.csv 600

pause

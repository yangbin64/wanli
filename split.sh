#!/bin/sh

head -n 133657 data_2.csv | cut -f2- -d, > data_training_X.csv
head -n 133657 data_2.csv | cut -f1 -d, > data_training_y.csv
tail -n 33414 data_2.csv | cut -f2- -d, > data_testing_X.csv
tail -n 33414 data_2.csv | cut -f1 -d, > data_testing_y.csv


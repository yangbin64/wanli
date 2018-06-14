#!/bin/sh

python predict.py data_training_X.csv data_training_y.csv logistic.pkl data_training_y_predict.csv data_training_y_predict_proba.csv

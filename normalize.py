import numpy as np
import pandas as pd
import sys

def normalize(filename_input, filename_output):
    df = pd.read_csv(filename_input, header=None)
    print(df)

    for i in np.arange(1,24):
        mean = df[i].mean()
        std = df[i].std()
        df[i] = (df[i]-mean)/std
        print(df[i].std())

    print(df)

    df.to_csv(filename_output, header=False, index=False)

def main():
    filename_input = sys.argv[1]
    filename_output = sys.argv[2]
    normalize(filename_input, filename_output)

main()


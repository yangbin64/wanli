
"""
Demonstrates similarities between pcolor, pcolormesh, imshow and pcolorfast
for drawing quadrilateral grids.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import math

def show_result(sn):
    aa = (np.arange(10)+0.5-5.0)/2.0
    bb = (np.arange(10)+0.5-5.0)/2.0
    xx, yy = np.meshgrid(aa, bb)
    zz = (xx+yy)/2

    df = pd.read_csv("input2.csv", sep=',', header=None, names=['x', 'y', 'value'])
    for key, row in df.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        v = float(row['value'])
        if x!=0 and x!=10 and y!=0 and y!=10:
            zz[y-1,x-1] = v

    df_bandit = pd.read_csv("log2_ts.csv", sep=',', header=None, names=['l', 'x', 'y', 'value', 'value1'])
    df_bandit_sn = df_bandit[['x', 'y', 'value']][:sn]
    #print(df_bandit_sn)
    #print(np.average(df_bandit['value'][:sn]))

    df_original = pd.read_csv("original2.csv", sep=',', header=None, names=['x', 'y', 'value'])
    df_original_sn = df_original[['x', 'y', 'value']][:sn]

    x_org = np.arange(0, sn, 1)

    y_original = np.cos(x_org/10)
    y_original = np.array(df_original_sn['value'])
    y_original_mean = np.zeros(sn)

    y_bandit = np.sin(x_org/10)
    y_bandit = np.array(df_bandit_sn['value'])
    y_bandit_mean = np.zeros(sn)

    for s in np.arange(sn):
        b = 0
        if s>100:
            b = s - 100
        bandit_ave = np.mean(df_bandit['value'][b:s])
        y_bandit_mean[s] = bandit_ave
        original_ave = np.mean(df_original['value'][b:s])
        y_original_mean[s] = original_ave

    fig = plt.figure(figsize=(8,5))

    plt.axes([0.05, 0.05, 0.3, 0.4])
    plt.pcolor(xx, yy, zz, cmap='RdBu', vmin=0, vmax=0.12)
    plt.title('bandit(' + str(sn) + ')')
    # set the limits of the plot to the limits of the data
    plt.axis([xx.min(), xx.max(), yy.min(), yy.max()])
    plt.colorbar()
    for key, row in df_bandit_sn.iterrows():
        x = (row['x']-5.0)/2.0
        y = (row['y']-5.0)/2.0
        a = math.pow(0.8,sn-key)
        if a<0.1:
            a = 0.1
        plt.scatter(np.array([x]), np.array([y]), s=300, c="green", alpha=a)

    plt.axes([0.45, 0.05, 0.5, 0.4])
    plt.title('bandit(' + str(sn) + ')')
    plt.plot(x_org, y_bandit, color='green')
    plt.plot(x_org, y_bandit_mean, color='red', linewidth = 3.0)
    plt.hlines([0.04, 0.08, 0.12, 0.16], 0, 600, linestyles=":")
    #plt.hlines([0], 0, 300, linestyles="-")

    plt.axes([0.05, 0.55, 0.3, 0.4])
    plt.pcolor(xx, yy, zz, cmap='RdBu', vmin=0, vmax=0.12)
    plt.title('original(' + str(sn) + ')')
    # set the limits of the plot to the limits of the data
    plt.axis([xx.min(), xx.max(), yy.min(), yy.max()])
    plt.colorbar()
    for key, row in df_original_sn.iterrows():
        x = (row['x']-5.0)/2.0
        y = (row['y']-5.0)/2.0
        a = math.pow(0.8,sn-key)
        if a<0.1:
            a = 0.1
        plt.scatter(np.array([x]), np.array([y]), s=300, c="green", alpha=a)

    plt.axes([0.45, 0.55, 0.5, 0.4])
    plt.title('original(' + str(sn) + ')')
    plt.plot(x_org, y_original, color='green')
    plt.plot(x_org, y_original_mean, color='red', linewidth = 3.0)
    plt.hlines([0.04, 0.08, 0.12, 0.16], 0, 600, linestyles=":")
    #plt.hlines([0], 0, 300, linestyles="-")

    plt.subplots_adjust(wspace=0.5, hspace=0.5)

    #plt.show()
    strsn = '{0:07d}'.format(sn)
    fn = 'resu_frames\\frame' + strsn + '.png'
    plt.savefig(fn)

show_result(600)
for sn in np.arange(600):
    show_result(sn)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import math

fig = plt.figure(figsize=(6.4,4.8))
b_colorbar1 = True
b_colorbar2 = True

def show_result(sn):
    print('sn=' + str(sn))
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
    #print(zz)

    df_bandit = pd.read_csv("log2_ts.csv", sep=',', header=None, names=['l', 'x', 'y', 'exp', 'value'])
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
        bandit_ave = np.mean(df_bandit['value'][:s])
        y_bandit_mean[s] = bandit_ave
        original_ave = np.mean(df_original['value'][:s])
        y_original_mean[s] = original_ave

    #fig = plt.figure(figsize=(6.4,4.8))

    plt.axes([0.05, 0.1, 0.3, 0.3])
    plt.cla()
    plt.pcolor(xx, yy, zz, cmap='RdBu', vmin=-2, vmax=2)
    plt.title('bandit(' + str(sn) + ')')
    # set the limits of the plot to the limits of the data
    plt.axis([xx.min(), xx.max(), yy.min(), yy.max()])
    global b_colorbar1
    if b_colorbar1:
        plt.colorbar()
        b_colorbar1 = False
    for key, row in df_bandit_sn.iterrows():
        x = (row['x']-5.0)/2.0
        y = (row['y']-5.0)/2.0
        a = math.pow(0.8,sn-key)
        if a<0.1:
            a = 0.1
        plt.scatter(np.array([x]), np.array([y]), s=100, c="green", alpha=a)

    plt.axes([0.45, 0.1, 0.5, 0.3])
    plt.cla()
    plt.title('bandit(' + str(sn) + ')')
    plt.plot(x_org, y_bandit, color='green')
    plt.plot(x_org, y_bandit_mean, color='red', linewidth = 3.0)
    plt.hlines([-3, -2, -1, 1, 2, 3], 0, 300, linestyles=":")
    plt.hlines([0], 0, 300, linestyles="-")

    plt.axes([0.05, 0.6, 0.3, 0.3])
    plt.cla()
    plt.pcolor(xx, yy, zz, cmap='RdBu', vmin=-2, vmax=2)
    plt.title('original(' + str(sn) + ')')
    # set the limits of the plot to the limits of the data
    plt.axis([xx.min(), xx.max(), yy.min(), yy.max()])
    global b_colorbar2
    if b_colorbar2:
        plt.colorbar()
        b_colorbar2 = False
    for key, row in df_original_sn.iterrows():
        x = (row['x']-5.0)/2.0
        y = (row['y']-5.0)/2.0
        a = math.pow(0.8,sn-key)
        if a<0.1:
            a = 0.1
        plt.scatter(np.array([x]), np.array([y]), s=100, c="green", alpha=a)

    plt.axes([0.45, 0.6, 0.5, 0.3])
    plt.cla()
    plt.title('original(' + str(sn) + ')')
    plt.plot(x_org, y_original, color='green')
    plt.plot(x_org, y_original_mean, color='red', linewidth = 3.0)
    plt.hlines([-3, -2, -1, 1, 2, 3], 0, 300, linestyles=":")
    plt.hlines([0], 0, 300, linestyles="-")

    plt.subplots_adjust(wspace=0.5, hspace=0.5)

def plot(data):
    print(data)
    plt.cla()
    rand = np.random.randn(100)
    #im = plt.plot(rand)
    plt.plot(rand)

def show_animation():
    ani = animation.FuncAnimation(fig, show_result, interval=100, frames=300)
    #plt.show()
    #ani.save("result.gif", writer="imagemagick")
    ani.save("result.htm")

show_animation()
#show_plot()

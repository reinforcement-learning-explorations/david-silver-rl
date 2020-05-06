import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def value_fn_plotter(V, title='V*', file_path="./plots/plot", show=False):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    x = []
    y = []
    z = []
    for i in range(1, 10+1):
        for j in range(1, 21+1):
            x.append(i)
            y.append(j)
            z.append(V[i-1, j-1])

    surf = ax.plot_trisurf(x, y, z, cmap=cm.coolwarm)

    ax.set_xlabel('dealer')
    ax.set_ylabel('player')
    ax.set_zlabel('V')
    plt.title(title)
    plt.xticks(np.arange(1, 11))
    plt.yticks(np.arange(1, 22, 4))

    if file_path != None:
        plt.savefig(file_path)
    if show:
        plt.show()

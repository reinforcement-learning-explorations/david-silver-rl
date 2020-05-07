import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def value_fn_plotter(V, axis_range_step, title='V*', axis_labels=("X", "Y", "Z"), file_path="./plots/plot", show=False):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    x = []
    y = []
    z = []
    a, b, c = axis_range_step[0]
    d, e, f = axis_range_step[1]
    for i in range(a, b+1):
        for j in range(d, e+1):
            x.append(i)
            y.append(j)
            # this could cause generalization problems where states start at 0,0 instead of 1,1 in future environments
            z.append(V[i-1, j-1])

    surf = ax.plot_trisurf(x, y, z, cmap=cm.coolwarm)

    ax.set_xlabel(axis_labels[0])
    ax.set_ylabel(axis_labels[1])
    ax.set_zlabel(axis_labels[2])
    plt.title(title)

    plt.xticks(np.arange(a, b, c))
    plt.yticks(np.arange(d, e, f))
    if len(axis_range_step) == 3:
        a,b,c = axis_range_step[2]
        plt.zticks(np.arange(a,b+1,c))

    if file_path != None:
        plt.savefig(file_path)
        plt.clf()
    if show:
        plt.show()

def mean_sq_error_plotter(mse, X, title='MEAN SQUARED ERROR', axis_label="X", file_path="./plots/plot", show=False, legend=False):
    if legend:
        # if we need a legend, there must be many sets of data on the same plot ->
        legend_items = []
        for l in X:
            legend_items.append('λ={:0.1f}'.format(l))
            plt.plot(list(range(len(mse[l]))), mse[l])
        plt.legend(legend_items, ncol=4)
    else:
        plt.plot(X, mse)

    plt.xlabel(axis_label)
    plt.ylabel("MEAN SQ ERROR")
    plt.title(title)
    plt.grid(True)

    if file_path != None:
        plt.savefig(file_path)
        plt.clf()
    if show:
        plt.show()

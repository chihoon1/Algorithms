'''
plotting functions that visualize data points for clusterings and etc.
'''
#import os, sys
#sys.path.insert(0, os.getcwd())
import seaborn as sns
import matplotlib.pyplot as plt

def plot2D_clustering(D, cluster_labels, **kwargs):
    '''
    Plot clustering of the dataset D. i-th index of cluster_labels is the clust label of i-th row(data) in D
    :param D: numpy 2d array dataset (expect 2-dimensional data)
    :param cluster_labels: numpy 1d array represent cluster label of data point in D
    :return: None
    '''
    sns.scatterplot(x=D[:, 0], y=D[:, 1], hue=cluster_labels)
    plt.show()




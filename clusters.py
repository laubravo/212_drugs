import seaborn as sns
import umap
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from scipy.spatial import distance_matrix
import statistics
import random
from sklearn.manifold import TSNE


def calc_distance_matrix(node_vectors):
    matrix = distance_matrix(node_vectors, node_vectors)
    print ('done distance matrix')
    return matrix

def silhoutte_score(embed_vectors, embed_ids, pathInd_name_dict, path_list):
    dist_matrix = calc_distance_matrix(embed_vectors)
    silScore_pathId_list = []
    print (len(path_list))
    for pathInd in range(0, len(path_list)):
        if (pathInd % 100 ==0):
            print (pathInd)
        labels = [len(path_list)] * len(embed_ids)
        indexNode_inPath = []
        if (pathInd in pathInd_name_dict):
            names_inPath = pathInd_name_dict[pathInd]
            indexNode_inPath = [embed_ids.index(name) for name in names_inPath]
            for index in indexNode_inPath:
                labels[index] = pathInd
            
        
        if (len(set(labels)) > 1):
            sil_score_list = metrics.silhouette_samples(dist_matrix, labels, metric='precomputed')
            sil_score = statistics.mean([sil_score_list[k] for k in indexNode_inPath])
        else:
            sil_score = -1
        silScore_pathId_list.append(sil_score)
    print ('Average silhouette score: ' + str(statistics.mean(silScore_pathId_list)))
    return dist_matrix, silScore_pathId_list
def get_colors(embed_ids, pathInd_name_dict, path_list, pathInd):
    colors = ['grey'] * len(embed_ids)
    marker_size = [5] * len(embed_ids)
    names_inPath = pathInd_name_dict[pathInd]
    embed_id_set = set(embed_ids)
    indexNode_inPath = []
    for name in names_inPath:
        if (name in embed_id_set):
            indexNode_inPath.append(embed_ids.index(name))
    
    for index in indexNode_inPath:
        colors[index] = 'red'
        marker_size[index] = 30
    return colors, marker_size

def plot(embed_vectors, embed_ids, pathInd_name_dict, path_list, run):
    print ('goes into plotting')
    tsne = TSNE(n_components=2)
    node_embeddings_2d = tsne.fit_transform(embed_vectors)
    pathInd_list = random.sample(range(0, len(path_list)), 100)
    for i in pathInd_list:
        if (i in pathInd_name_dict):
            colors, marker_size = get_colors(embed_ids, pathInd_name_dict, path_list, i)
            plt.figure()
            plt.scatter(
                node_embeddings_2d[:, 0],
                node_embeddings_2d[:, 1],
                s=marker_size,
                alpha=0.4,
                c=colors)#[sns.color_palette(n_colors=2)[x] for x in colors])
            #plt.gca().set_aspect('equal', 'datalim')
            plt.title('Pathway {}'.format(path_list[i]), fontsize=24)
            plt.savefig('../figs/umap_node/{}_tsne/nodes_{}.png'.format(run, i))
            plt.close()

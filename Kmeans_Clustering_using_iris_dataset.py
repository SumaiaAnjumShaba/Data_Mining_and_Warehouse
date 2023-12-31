# -*- coding: utf-8 -*-
"""1920932_Assignmnet2_ KMeans_CSC417_Su22.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QeKVMmF8mGm8jusZrBfusBClJIsa6Fxm

#Sumaia Anjum Shaba
#1920932

#**Mounting**
"""

import os
import google.colab
import time
import sys
if not os.path.isdir('/content/drive'):
  google.colab.drive.mount('/content/drive')

"""#**Import Libary**"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import figure
from scipy.stats import multivariate_normal
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
from numpy import random
from numpy import sqrt
from scipy.spatial import distance

"""#**Hierarchical clustering**

#**Dataset connection**
"""

df = pd.read_csv("/content/drive/MyDrive/Data Mining/hierarchicalClusterData.csv")
print(df)
print(df.shape)

data=df.iloc[:].values # it will remove the index number and coloum header for all row
print(data)

hierarchy_linkage=shc.linkage(data,'single')
plt.figure(figsize=(10, 7))
plt.title("Dendrograms")
dendrogram= shc.dendrogram(hierarchy_linkage)

cluster = AgglomerativeClustering(n_clusters=3, affinity='euclidean', linkage='ward')
cluster.fit_predict(data)

plt.figure(figsize=(10, 7))
plt.scatter(data[:,0], data[:,1], c=cluster.labels_)

"""#**KMeans Clustering**

"""

import random
import math
import json
import sys
import time

"""Load data from file and save in the numpy matrix"""

def load(file_name):
    # data(list of list): [[index, dimensions], [.., ..], ...]
    data = []
    fh = open(file_name)
    for line in fh:
        line = line.strip().split(',')
        temp = [int(line[0])]
        for feature in line[1:]:
            temp.append(float(feature))
        data.append(temp)
    return data

"""simple centroid initialization function"""

def initialize_centroids_simple(data, dimension, k):

    #centroids: [(centroid0 fearures); (centroid0 features); ... ..]
    centroids = [[0 for _ in range(dimension)] for _ in range(k)]
    centroids=np.array(centroids)

    #TO DO
    print(data.shape)
    length = len(data)
    for i in range(k):
      random_index=random.randint(0,length-1)
      centroids[i]=(data[random_index,1:])




    #Write your code to return initialized centroids by randomly assiging them to K points
    return centroids

"""Centroid initilization using min max"""

# def initialize_centroids(data, dimension, k):
#     centroids = [[0 for _ in range(dimension)] for _ in range(k)]
#     centroids=np.array(centroids)
#     max_feature_vals = [0 for _ in range(dimension)]
#     min_feature_vals = [float('inf') for _ in range(dimension)]
#     # TO DO
#     # Calculate max feature and min feture value for each dimension
#     for i in data:
#       for j in range(dimension):
#         if i[j+1]>max_feature_vals[j]:
#           max_feature_vals[j]=i[j+1]
#         elif i[j+1]<min_feature_vals[j]:
#           min_feature_vals[j]=i[j+1]

#     #diff: max - min for each dimension
#     diff=[max_feature_vals[j]-min_feature_vals[j] for j in range(dimension)]
#     # for each centroid, in each dimension assign centroids[j][i] = min_feature_val + diff * random.uniform(1e-5, 1)
#     for i in range(k):
#       for j in range(dimension):
#         centroids[i][j] = min_feature_vals[j]+diff[j]*random.uniform(1e-5,1)
#     centroids=np.array(centroids)
#     return centroids

def initialize_centroids(data, dimension, k):
    centroids = np.zeros((k,dimension))
    max_feature_vals = np.max(data[:,1:],axis=0)
    min_feature_vals = np.min(data[:,1:],axis=0)

    diff = max_feature_vals-min_feature_vals
    for i in range(k):
        centroids[i] = min_feature_vals+diff*random.uniform(1e-5, 1)
    return centroids

"""Calculate eucledian distance"""

def get_euclidean_distance(p1, p2): #centroid=p1,poin=p2
    distance = 0
    #Write your code
    #distance=distance.euclidean(p1,p2)

    distance=np.linalg.norm(p1-p2[1:])



    return distance

"""Sampling data from whole dataset"""

def get_sample(data):
    length = len(data)

    sample_size = int(length * 0.01)
    random_nums = set()
    sample_data = []

    for i in range(sample_size):
        random_index = random.randint(0, length - 1)
        while random_index in random_nums:
            random_index = random.randint(0, length - 1)
        random_nums.add(random_index)
        sample_data.append(data[random_index])
    return sample_data

"""KMeans Function

"""

def kmeans(data, dimension, k):
    #centroids: [(centroid0 fearures); (centroid1 features); ... ..]

    centroids = initialize_centroids_simple(data, dimension, k)



    #cluster_affiliation: [((point1index  features),clusterindex); ((point2index features), clusterindex)... ]
    cluster_affiliation = np.array([[tuple(features), None] for features in data])
    flag = True
    Jprev=0

    while flag:
      J=0

      for i, point in enumerate(data):
          min_distance = float('inf')
          min_distance_index = None
          #find closest centroids for each data points
          for cluster_index, centroid in enumerate(centroids):
            if centroid[0] == None:
              continue
            distance = get_euclidean_distance(centroid, point)
            if distance < min_distance:
              min_distance = distance
              min_distance_index = cluster_index
            #record or update cluster for each data points
          if cluster_affiliation[i][1] != min_distance_index:
            cluster_affiliation[i][1] = min_distance_index
            J+=min_distance*min_distance

        #recompute centroids
      centroids = np.array([[0 for _ in range(dimension)] for _ in range(k)])
      clutser_point_count = np.array([0 for _ in range(k)])

      #TO DO
      #write your code to count each cluster pointcount and store them in clutser_point_count structure
      #recompute centroids using the count
      for i in range(k):
        clutser_point_count[i] =cluster_affiliation[:,1].tolist().count(i)
        for x,j in enumerate(cluster_affiliation[:,1]):
          if j==i:
            centroids[j]=[sum(xx) for xx in zip(centroids[j],cluster_affiliation[x,0][1:])]
      # print(clutser_point_count)
      for i in range(k):
        if clutser_point_count[i]!=0:
          centroids[i]=centroids[i]/clutser_point_count[i]
      # centroids=(centroids.T/clutser_point_count).T
      J=J/dimension
      if abs(J-Jprev)<=10**-5:
        flag=False
      Jprev=J
      # print(J)
      # print(clutser_point_count)

        #TO DO
        #Terminate the while loop based on termination criteria. Write your code to turn flag = false



    return (centroids,cluster_affiliation)

"""#**Kmeans_Max_Min**"""

def kmeans2(data, dimension, k):
    #centroids: [(centroid0 fearures); (centroid1 features); ... ..]

    centroids = initialize_centroids(data, dimension, k)



    #cluster_affiliation: [((point1index  features),clusterindex); ((point2index features), clusterindex)... ]
    cluster_affiliation = np.array([[tuple(features), None] for features in data])
    flag = True
    Jprev=0

    while flag:
      J=0

      for i, point in enumerate(data):
          min_distance = float('inf')
          min_distance_index = None
          #find closest centroids for each data points
          for cluster_index, centroid in enumerate(centroids):
            if centroid[0] == None:
              continue
            distance = get_euclidean_distance(centroid, point)
            if distance < min_distance:
              min_distance = distance
              min_distance_index = cluster_index
            #record or update cluster for each data points
          if cluster_affiliation[i][1] != min_distance_index:
            cluster_affiliation[i][1] = min_distance_index
            J+=min_distance*min_distance

        #recompute centroids
      centroids = np.array([[0 for _ in range(dimension)] for _ in range(k)])
      clutser_point_count = np.array([0 for _ in range(k)])

      #TO DO
      #write your code to count each cluster pointcount and store them in clutser_point_count structure
      #recompute centroids using the count
      for i in range(k):
        clutser_point_count[i] =cluster_affiliation[:,1].tolist().count(i)
        for x,j in enumerate(cluster_affiliation[:,1]):
          if j==i:
            centroids[j]=[sum(xx) for xx in zip(centroids[j],cluster_affiliation[x,0][1:])]
      # print(clutser_point_count)
      for i in range(k):
        if clutser_point_count[i]!=0:
          centroids[i]=centroids[i]/clutser_point_count[i]
      # centroids=(centroids.T/clutser_point_count).T
      J=J/dimension
      if abs(J-Jprev)<=10**-5:
        flag=False
      Jprev=J
      print(J)
      # print(clutser_point_count)

        #TO DO
        #Terminate the while loop based on termination criteria. Write your code to turn flag = false



    return (centroids,cluster_affiliation)

"""#**Dataset Connection**

"""

data = pd.read_csv("/content/drive/MyDrive/Data Mining/data0.txt")
#print(data)
# print(data.shape)
row,col=data.shape
#print(col)
data=data.values
print(data)
row,col=data.shape
print(col)
print(len(data))

"""Driver funtion/Main Function"""

K=4
dimension=col-1

# save numpy array as csv file
from numpy import asarray
from numpy import savetxt

def main():
  start=time.time()
  sample_data=np.array(get_sample(data))
  # sample_data=data
  k=4
  centroids,cluster_affiliation=kmeans(sample_data,dimension,k)
  file1=open("out1.txt","w")
  for row in centroids:
    file1.write(str(row)+"\n")
  file1.close()
  f =  open('out2.txt','w')
  for i in cluster_affiliation:
    st = str(i[0][0])+" "+str(i[1])
    f.write(st+"\n")
  f.close()
  # print(centroids.shape)


  print('Duration: %s' % (time.time() - start))
  start=time.time()
  centroids,cluster_affiliation=kmeans2(sample_data,dimension,k)
  file1=open("out11.txt","w")
  for row in centroids:
    file1.write(str(row)+"\n")
  file1.close()
  f =  open('out22.txt','w')
  for i in cluster_affiliation:
    st = str(i[0][0])+" "+str(i[1])
    f.write(st+"\n")
  f.close()
  print('Duration: %s' % (time.time() - start))

if __name__ == "__main__":
  main()

a=np.array([[(0,2,3),1], [(1,3,4),0], [(2,3,1),1], [(0,2,4),1]])
k=2
print(a.shape)
centroids = np.array([[0 for _ in range(2)] for _ in range(k)])
clutser_point_count = np.array([0 for _ in range(k)])

for i in range(k):
          clutser_point_count[i] =a[:,1].tolist().count(i)
          for x,j in enumerate(a[:,1]):

            if j==i:
              centroids[j]=[sum(xx) for xx in zip(centroids[j],a[x,0][1:])]
print(centroids)
for i in range(k):
          if clutser_point_count[i]!=0:
            print(clutser_point_count[i] )
            centroids[i]=centroids[i]/clutser_point_count[i]

# print(centroids)
# print(clutser_point_count)
# print()
import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt  
import math
import random

def distance(a,b):
	return math.pow( (math.pow(a[0]-b[0],2) + math.pow(a[1]-b[1],2) + math.pow(a[2]-b[2],2)) ,0.5)

def assign_labels(img, centroid, index):
	x, y, temp = img.shape
	for i in xrange(x):
		for j in xrange(y):
			if np.array_equal(img[i,j], np.array([0,0,0])):
				index[i,j] = -1
				continue
			dist = 1000000000
			for k, l in enumerate(centroid):
				temp = distance(img[i,j], l)
				if temp < dist:
					index[i,j] = k
					dist = temp
	return index

def new_centroid(img, index, c):
	x, y, temp = img.shape
	centroid = [ [0 for i in xrange(3)] for j in xrange(c)]
	centroid = np.array(centroid)
	centroid_total = [ 0 for i in xrange(c)]
	for i in xrange(x):
		for j in xrange(y):
			if np.array_equal(img[i,j], np.array([0,0,0])):
				continue
			temp = int(index[i,j])
			centroid[temp,0] += img[i,j,0]
			centroid[temp,1] +=	img[i,j,1]
			centroid[temp,2] += img[i,j,2]
			centroid_total[temp] += 1
	for i in xrange(c):
		if centroid_total[i] == 0:
			centroid[i] = 0
		else:
			centroid[i] = centroid[i]*1.0 / centroid_total[i]
	return centroid

def create_index(filename, number_of_centroids):
	#c = int(raw_input('Enter the number of centroids: '))
	c = number_of_centroids
	img = Image.open(filename)
	img = np.array(img)
	x,y, temp = img.shape
	print 'RBG_Data: Creating index matrix | a variation of dimensional reduction'
	np.random.seed()
	#centroid =  np.array([ np.random.randint(0,256,3), np.random.randint(0,256,3)])
	centroid = [[ random.randint(0,256) for i in xrange(3)] for j in xrange(c)] 
	centroid = np.array(centroid)

	index = np.zeros((x,y)) - 1

	#number of iterations in K-Means
	for i in xrange(3):
		index = assign_labels(img[:,:,:3],centroid, index)
		centroid = new_centroid(img[:,:,:3], index, centroid.shape[0])
	index = index + 1
	
	return img, index


def display_index(index):
	x, y = index.shape
	# plt_x = np.empty((x*y,2))
	# plt_y = np.empty((x*y))
	plt_x =[]
	plt_y = []
	index_max = index.max()
	for i in xrange(x):
		for j in xrange(y):
			# if index[i,j]==0:
			# 	continue

			plt_x.append([i,j])
			plt_y.append(index[i,j]*1.5 / index_max)

	plt_x = np.array(plt_x)
	plt_y = np.array(plt_y)
	
	#change cmap color to change the range of colors that appear in output
	plt.scatter(plt_x[:,0],plt_x[:,1], c=plt_y, cmap='gray')
	plt.show()
import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt  
import math
import random
import pyfits

def distance(a,b):
	return abs(a-b)

def assign_labels(img, centroid, index):
	x, y = img.shape
	img_min = img.min()
	for i in xrange(x):
		for j in xrange(y):
			if img[i,j]==img_min:
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
	img_min = img.min()
	x, y = img.shape
	centroid = [ 0 for j in xrange(c)]
	centroid = np.array(centroid)
	centroid_total = [ 0 for i in xrange(c)]
	for i in xrange(x):
		for j in xrange(y):
			if img[i,j]==img_min:
				continue
			temp = int(index[i,j])
			centroid[temp] += img[i,j]
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
	img_temp = pyfits.open(filename)
	img = img_temp[0].data
	img_temp.close()
	img_max = img.max()
	img_min = img.min()
	x,y = img.shape

	#Report progress
	#print 'Progress...1%'
	print "X_Ray Data: Creating index matrix | a variation of dimensional reduction"
	np.random.seed()
	centroid = [ random.randint(0,img_max)  for j in xrange(c)] 
	centroid = np.array(centroid)

	index = np.zeros((x,y)) - 1
	#print '           5%'

	#number of iterations in K-Means
	for i in xrange(30):
		index = assign_labels(img,centroid, index)
		centroid = new_centroid(img, index, len(centroid))
	index = index + 1
	#print '           70%'
	return img, index, centroid

def display_index(index):
	# plt_x = np.empty((x*y,2))
	# plt_y = np.empty((x*y))
	x,y = index.shape
	plt_x =[]
	plt_y = []

	index_max = index.max()
	for i in xrange(x):
		for j in xrange(y):
			# if img[i,j]==img_min:
			# 	continue

			plt_x.append([i,j])
			plt_y.append(index[i,j])


	plt_x = np.array(plt_x)
	plt_y = np.array(plt_y)
	plt.scatter(plt_x[:,0],plt_x[:,1], c=plt_y, cmap='gray')
	plt.show()

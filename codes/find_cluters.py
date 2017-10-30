import x_ray_kmeans as idx
import rbg_kmeans as idx_rbg
import matplotlib.pyplot as plt
import numpy as np  

def boundary(index, i,j):
	x, y = index.shape
	x, y = x-1, y-1
	#print x,y
	if (i==0 or i==x or j==0 or j==y):
		return True
	for a in xrange(-1,2):
		for b in xrange(-1,2):
			if (a,b)==(0,0):
				continue
				
			if index[i,j] != index[i+a,j+b]:
				return True
	return False

def plot_labels(labels):
	index_max = int(index.max())
	for i in xrange(index_max+1):
		labels[i] = np.array(labels[i])

	# temp = np.array(labels[index_max])
	# plt.scatter(temp[:,0],temp[:,1],marker='.')
	# plt.show()

	f, ax = plt.subplots(1,index_max+1, sharey=True)
	for i in xrange(index_max+1):
		ax[i].scatter(labels[i][:,0],labels[i][:,1],marker='.')

	f.subplots_adjust(hspace=0.3)
	plt.show()


img, index = idx.create_index('../images/kepler.fits', 3)
#idx.display_index(index)

# img, index = idx_rbg.create_index('../images/circle.png',3)
# idx_rbg.display_index(index)

#explicitly delete img as it can be huge thereby occupying a large physical memory
del img
G = index
x,y = index.shape
index_max = int(index.max())
labels = [ [] for i in xrange(index_max+1)]

for i in xrange(x):
	for j in xrange(y):
		if not boundary(index, i, j):
			continue
		labels[int(index[i,j])].append([i,j])

plot_labels(labels)
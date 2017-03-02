# SamplingAlgorithm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
from scipy.spatial import Voronoi, voronoi_plot_2d



# --------------------------------------------------------------------------------------------------
# SAMPLER CLASS
# --------------------------------------------------------------------------------------------------
class Sampler:

	
	def __init__(self, img_data=None, filepath = None):
		if filepath:
			self.img_data = mpimg.imread(filepath)
		else:
			self.img_data = img_data
		self.sample = np.array([])
		self.fsize = (9,6)
		if img_data:
			self.height, self.width = self.img_data.shape[:2]
		else:
			self.width = 800 # needs to be 800
			self.height = 525 # needs to be 525



	def make_sample(self, method, numPoints=100, r=20, numCandidates=10):
		'''
		Will generate and set self.sample to a sample of specified attributes.

		method = 'random','best_candidate', or 'bridson' to generate samples with given method
		kwargs are
			- numPoints = number of samples to generate for best_candidate and random methods. 
			- r = radius used for bridson method
			- numCandidates = number of candidates to try for each point. Ignored if method = 'random'
		'''
		assert method in ['random','best_candidate', 'bridson']

		if method == 'random':
			self.sample = random_sampling(numPoints, self.width, self.height)
			return self.sample
		elif method == 'best_candidate':
			self.sample = best_candidate(numPoints, numCandidates, self.width, self.height)
			return self.sample
		else:
			self.sample = bridson_sample(r, numCandidates, self.width, self.height)
			return self.sample

	def plot_samp(self, figsize = None, ivl = 25):
		if not figsize:
			figsize = self.fsize
		return animate_plot(self.sample, self.width, self.height, ivl = ivl, figsize = self.fsize)

	def show_img(self):
		return plt.imshow(self.img_data)

	def sample_img(self, method='random', numPoints=100, r = 10, numCandidates=10):
		if not self.sample.size:
			self.make_sample(method,numPoints,r,numCandidates)
		return sample_image(self.sample, self.fsize, img_data=self.img_data)


# --------------------------------------------------------------------------------------------------
# PLOTTING
# --------------------------------------------------------------------------------------------------


def update_plot(num, data, line):
	line.set_data(data[...,:num])
	return line


def animate_plot(samp, width, height, ivl = 50, figsize = (9,6)):
	fig = plt.figure(figsize=figsize)
	l, = plt.plot([],[], '.r', ms = 8)
	plt.xlim(-10,width + 10)
	plt.ylim(-10, height + 10)

	plt.show()
	return animation.FuncAnimation(fig, update_plot, len(samp), fargs=(samp.T, l), interval = ivl, repeat = False)




# --------------------------------------------------------------------------------------------------
# RANDOM SAMPLING
# --------------------------------------------------------------------------------------------------

def random_sampling(numPoints, width, height):
	samples = [np.random.random(size = numPoints)*width, np.random.random(size = numPoints)*height ]
	return np.array(samples).T

# --------------------------------------------------------------------------------------------------
# BEST CANDIDATE
# --------------------------------------------------------------------------------------------------


def getDistance(p1, p2):
	distance = np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
	return distance

def best_candidate(numPoints, numCandidates, width, height):
	points =[(np.random.random()*width, np.random.random()*height)]
	print 'First Point:', points[0]
	for n in range(numPoints):
		# EACH POINT
		best_point = None
		max_dist = 0
		for i in range(numCandidates): 
			# CREATE A CANDIDATE FOR SINGLE POINT
			dists = [] # for this candidate, all the distances from each other point
			samp = (np.random.random()*width, np.random.random()*height)
			for p in points:
				# GET DISTANCE FOR OUR CANDIDATE FROM ALL OTHER CURRENT POINTS
				# STORE CANDIDATE DISTANCES IN 'DISTS' LIST
				dist = getDistance(samp, p)
				dists.append({'point': samp, 'distance':dist})
			# find the nearest point to samp via sorting by distance
			dists = sorted(dists, key = lambda r: r['distance'])
			if dists[0]['distance'] > max_dist:
				# if our min distance is larger than our current contender for max dist
				# it becomes our new contender
				max_dist = min(dists)['distance']
				best_point = min(dists)['point']
		points.append(best_point)
	return np.ceil(np.array(points)).astype('int')




# --------------------------------------------------------------------------------------------------
# BRIDSON
# --------------------------------------------------------------------------------------------------

def rand_annulus(ref, r, wt,ht):
	inWindow = False
	while not inWindow:
		theta = np.random.uniform(0,2*np.pi)
		r_dist = np.random.uniform(r, 2*r)
		x = np.cos(theta)*r_dist + ref[0]
		y = np.sin(theta)*r_dist + ref[1]
		if x > wt or x < 0:
			continue
		if y > ht or y <0:
			continue
		inWindow = True
	return (x,y) 


def bridson_sample(r, numCandidates, width, height):
	points =[]
	active = [(np.random.random()*width, np.random.random()*height)]
	finished = False
	print 'First Point:', active[0]
	# while we still have any active points
	while active:
		# choose an active point at random (SLOW)
		ref_point = active[np.random.choice(len(active))]
		point_found = False
		# generate a certain number of candidate new points
		for i in range(numCandidates):
			samp = rand_annulus(ref_point, r, width, height)
			valid = True
			# for each candidate, check if it's within distance r from ANY other point
			for p in points + active:
				if getDistance(p, samp) < r:
					valid = False
					break
			# it isn't, add it to active points
			if valid:
				active.append(samp)
				point_found = True
				break
		# if all candidates are invalid, deactive our current reference point
		if not point_found:
			points.append(ref_point)
			active.remove(ref_point)
	return np.ceil(np.array(points)).astype('int')


# --------------------------------------------------------------------------------------------------
# TESTING IT OUT
# --------------------------------------------------------------------------------------------------



def main():
	random_samps1000 =random_sampling(1000)

	bc500 = best_candidate(500,15)
	x1, y1 = bc500[:,0], bc500[:,1]

	bc500_20 = best_candidate(500,20)
	x2, y2 = bc500_20[:,0], bc500_20[:,1]

	bc1000 = best_candidate(1000, 15)
	x3, y3 = bc1000[:,0], bc1000[:,1]
		

	brid_samps15_10 = bridson_sample(15,10)
	x4 = brid_samps15_10[:,0]
	y4 = brid_samps15_10[:,1]

	# sampling gets slower as you raise the number of candidates to generate (2nd param)
	brid_samps15_20 = bridson_sample(15,20)
	x5 = brid_samps15_20[:,0]
	y5 = brid_samps15_20[:,1]


	# sampling gets better as you lower the allowed distance between points (1st parameter)
	brid_samps10 = bridson_sample(10,10)
	x6 = brid_samps10[:,0]
	y6 = brid_samps10[:,1]



	all_samples = [random_samps1000, bc500, bc500_20, bc1000, 
					brid_samps15_10, brid_samps15_20, brid_samps10]

	titles = ['1000 Random Samples', 'Best Candidate Sampling \n 500 Points, 15 Candidates', 
				'Best Candidate Sampling \n 500 Points, 20 Candidates', 'Best Candidate Sampling \n 1000 Points, 15 Candidates',
				'Bridson Sampling \n Min_dist = 15, NumCandidates = 10', 'Bridson Sampling \n Min_dist = 15, NumCandidates = 20',
				'Bridson Sampling \n Min_dist = 10, NumCandidates = 10']
	return all_samples, titles


# VORONOI OF IMAGE

#IMG
carmen = mpimg.imread('/Users/RickS/Pictures/IMG_0314.JPG')

def sample_image(samples, fsize, img_fp=None, img_data=None):
	if img_fp == None and img_data == None:
		print "No Image Data. Please pass a filepath or np array of image data."
		return
	# samples must have shape (n, 2)
	if img_fp:
		img = mpimg.imread(img_fp)
	else:
		img = img_data
	# swap axes so width x height is aligned with samples row/column
	# flip left to right so not upside down... it's werid i dunnno
	img = np.fliplr(img.swapaxes(0,1))
	samps = samples[::].astype('int')
	# i don't think this is necessary
	colors = np.array([img[s[0], s[1]] for s in samps])/255.

	vor = Voronoi(samps)
	vor.vertices # points that characterize the boundaries of the regions
	vor.regions # indices of vertices for each region
	vor.points # (same thing as samples1)
	vor.point_region # mapping from points to regions, # values are INDICES of vor.regions 

	fig = plt.figure(figsize = fsize)
	ax = plt.gca()
	voronoi_plot_2d(vor, ax = ax)

	for pt, reg_idx in enumerate(vor.point_region):
		cntrPt = vor.points[pt].astype('int')
		vert_idxs = vor.regions[reg_idx]
		if -1 in vert_idxs: continue
		verts = np.array([vor.vertices[ix] for ix in vert_idxs]).T
		ax.fill(verts[0],verts[1], color =  img[cntrPt[0],cntrPt[1]]/255., alpha = 0.88)

	ax_children = ax.get_children()
	line2ds = ax_children[-12:-10]
	lcollections = ax_children[:2]

	plt.show()
	return vor, line2ds, lcollections

newImg = '/Users/RickS/Documents/Programming/Metis/Bootcamp/investigations/rick/IMG_5791.jpg'


if __name__ == '__main__':
	all_samples, titles = main()
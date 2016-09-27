# Random_Sampling

Based off of Mike Bostocks ["Visualizing Algorithims"] (https://bost.ocks.org/mike/algorithms/). Random Sampling is used in image processing and feature recognition. The idea is that to convert light (or any continuous signal) into something useable/storable in a computer you need to convert it to discrete impulses. Choosing areas of the image to best characterize the image is called sampling. When choosing these points, you don't want to just choose evenly spaced points accross the image: 

*Don't do this:*
!(even_spaced){Images/even_spaced.png}

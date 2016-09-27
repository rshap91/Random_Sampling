# Random_Sampling

Based off of Mike Bostocks ["Visualizing Algorithims"] (https://bost.ocks.org/mike/algorithms/). Random Sampling is used in image processing and feature recognition. The idea is that to convert light (or any continuous signal) into something useable/storable in a computer you need to convert it to discrete impulses. Choosing areas of the image to best characterize the image is called sampling. When choosing these points, you don't want to just choose evenly spaced points accross the image: 

*Don't do this:*
![even_spaced](Images/even_spaced.png)

This is because choosing even spaced samples can lead to Moiree patterns, which are distinct ripples or other patterns that appear in the image when some of the light signals generated are too similar to one another. For example, if not corrected, the picture below of the brick wall will result in moiree patterns due to the repeating bricks.

![moiree brick wall](Images/moiree_brick_wall.jpg)


In digital photography, this is caused by a process called "aliasing".

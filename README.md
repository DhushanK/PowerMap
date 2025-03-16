# Car-Density-Tracking
**A computer vision based car identification and tracking system, while also identifying areas of repeat attendance, then representing it with a heat map that perpetually updates**

# **Technologies Used**
- OpenCV using Python for computer vision based object idenitification/tracking 
- Tensorflow using Python to gain pre trained models to base the object identification on
- matplotlib with Python to visualize data in graphs (heat map)

# **How does it work?**

# **Computer Vision Car Tracking**
Using a pre-trained model that identiifies various objects including cars, cars on each frame of the video is identified with the x and y coordinates of the object's border is idenitified. Following this, these borders are mapped onto a new canvas. The x and y coordinates are also presented within the border's, constantly updating as the cars move across the frame

# **Updating array corresponding to the frame**
After breaking up the frame's pixels into an array the size of the pixels on the x and y axis, with every movement in an area of pixels, the arrays count goes up throughout the course of the video

# **Visualizing the data as a heat map**
Next, the array is visualized as a heat map with the 2-D array representing the frame of the map while higher numbers correlate to a darker shade of red in that rea, indiciating high concentrations of vehicle activity in those areas throughout the course of the video. This map is accessible through clicking a button at the top of the frame

# **Credits**
Tensorflow model : https://github.com/tensorflow/tfjs-models/blob/master/coco-ssd/README.md


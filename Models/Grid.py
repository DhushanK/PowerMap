import cv2 #Use this to get your dimensions
import numpy
lastHope = cv2.VideoCapture("testVideos/cartop.mp4") #Change this for a new video and stuff the parameters into it, im tired
widthOfFrame = int(lastHope.get(cv2.CAP_PROP_FRAME_WIDTH))
heightOfFrame = int(lastHope.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(widthOfFrame,heightOfFrame) #FINALLLLLLLLY #Try to implement this as a class that returns these values to compare to, but lowk just use 1920 and 1080 for now

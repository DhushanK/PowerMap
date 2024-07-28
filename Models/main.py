from Detector import *
import os 
def main(): #Initializing all the variables in the constructor function in the following class 
    videoPath = "testVideos/cartop.mp4"
    configurationPath = os.path.join("Models","ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join("Models", "frozen_inference_graph.pb")
    classesPath = os.path.join("Models", "coco.names")

    detector = Detector(videoPath, configurationPath , modelPath, classesPath)
    detector.onVideo()      
if __name__ == '__main__':
    main()
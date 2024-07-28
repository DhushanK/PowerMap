#skyhigh, cartop, 0.3 conf
import cv2
import numpy as np
import time
import tkinter as tk
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import PowerNorm 

class Detector:
    def __init__(self, videoPath, configPath, modelPath, classesPath):
        self.heatmap_data = [[0 for _ in range(800)] for _ in range(600)]

        # Create a button to view the heatmap
        # ... (keep the existing initialization code)
        self.videoPath = videoPath #Establishing an connection to the video 
        self.configPath = configPath #Still establishing a connection but i lowk dont even know what a configuration file is in this context 
        self.modelPath = modelPath #Path to the trained model (from the internet) 
        self.classesPath = classesPath #Also a path but I lowk dont know what differentiates the classes it can access and cant 

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath) #Takes the paths as parameters to access the models 
        self.net.setInputSize(320,320) #The following lines sets various values of the video such as size and red/blue switches 
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)
        
        self.readClasses() #Sets up a line of code
        # Create Tkinter window and canvas
        self.root = tk.Tk()
        self.root.title("Object Tracking")
        self.heatmap_button = tk.Button(self.root, text="View Heatmap", command=self.show_heatmap)
        self.heatmap_button.pack()
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        # Dictionary to store object IDs and their corresponding canvas items
        self.object_rectangles = {}

    def update_heatmap(self, x, y):
        radius = 10
        for i in range(max(0, y-radius), min(600, y+(radius+1))):
            for j in range(max(0, x-radius), min(800, x+(radius+1))):
                self.heatmap_data[i][j] += 1
    # ... (keep other existing methods)

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()
        
        self.classesList.insert(0, '__Background__')
        self.colorList  = np.random.uniform(low = 0, high = 255, size = (len(self.classesList), 3))

        print(self.classesList)

    def generate_heatmap(self):
        fig, ax = plt.subplots(figsize=(16, 12))
        norm = PowerNorm(gamma=0.5)
        sns.heatmap(self.heatmap_data, ax=ax, cmap="YlOrRd", cbar=True, norm = norm)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.title("Heatmap of Car Density")
        return fig

    def show_heatmap(self):
        heatmap_window = tk.Toplevel(self.root)
        heatmap_window.title("Heatmap of Car Density")
        
        fig = self.generate_heatmap()
        canvas = FigureCanvasTkAgg(fig, master=heatmap_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        
    def onVideo(self):
        cap = cv2.VideoCapture(self.videoPath)
        if not cap.isOpened():
            print("Error opening video file")
            return

        zeroSpeedTime = 0

        while True:
            success, image = cap.read()
            if not success:
                break

            currentTime = time.time()
            fps = 1 / (currentTime - zeroSpeedTime)
            zeroSpeedTime = currentTime
            threshold = 0.3
            classLabelIDs, confidences, bboxs = self.net.detect(image, confThreshold=threshold)
            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1, -1)[0])
            confidences = list(map(float, confidences))

            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold=threshold, nms_threshold=0)

            if len(bboxIdx) != 0:
                for i in range(0, len(bboxIdx)):
                    bbox = bboxs[np.squeeze(bboxIdx[i])]
                    classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                    classLabel = self.classesList[classLabelID]
                    
                    x, y, w, h = bbox
                    
                    # Scale coordinates to fit the canvas
                    canvas_x = int(x * self.canvas.winfo_width() / image.shape[1])
                    canvas_y = int(y * self.canvas.winfo_height() / image.shape[0])
                    canvas_w = int(w * self.canvas.winfo_width() / image.shape[1])
                    canvas_h = int(h * self.canvas.winfo_height() / image.shape[0])
                    self.update_heatmap(canvas_x, canvas_y)

                    # Create or update rectangle on canvas
                    rect_id = f"{classLabel}_{i}"
                    if rect_id in self.object_rectangles:
                        self.canvas.coords(self.object_rectangles[rect_id]['rect'], 
                                        canvas_x, canvas_y, 
                                        canvas_x + canvas_w, canvas_y + canvas_h)
                        self.canvas.coords(self.object_rectangles[rect_id]['text'],
                                        canvas_x + 5, canvas_y + 5)
                        self.canvas.itemconfig(self.object_rectangles[rect_id]['text'],
                                            text=f"({canvas_x}, {canvas_y})")
                    else:
                        color = "red" if classLabel == "car" else "white" if classLabel == "person" else "white"
                        rect = self.canvas.create_rectangle(canvas_x, canvas_y, 
                                                        canvas_x + canvas_w, canvas_y + canvas_h, 
                                                        outline=color, width=2)
                        text = self.canvas.create_text(canvas_x + 5, canvas_y + 5,
                                                    text=f"({canvas_x}, {canvas_y})", fill=color, anchor='nw')
                        self.object_rectangles[rect_id] = {'rect': rect, 'text': text}
            #time.sleep(1)
    # ... (keep the rest of the method)

            self.root.update()

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.root.mainloop()

# ... (keep the rest of the code)
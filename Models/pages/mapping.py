from taipy.gui import Markdown, Gui, notify
import os
import sys

script_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(script_folder_path)

from Detector import *

text="A tool for building the future of EVs. Optimize EV charger locations using vehicle flow analysis."

configurationPath = os.path.join("Models","ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
modelPath = os.path.join("Models", "frozen_inference_graph.pb")
classesPath = os.path.join("Models", "coco.names")
imagePath = os.path.join("Models","Logo.png")

detector = Detector(configurationPath , modelPath, classesPath)

title="PowerMap"
content = imagePath

mapping_md = Markdown("""
                      
<|{content}|image|id=logo|>
### A tool for building the future of EVs. 
### Optimize EV charger locations using vehicle flow analysis.

                      

<|Begin Data Extraction|button|on_action=on_button_action|>
                      
""")

def on_button_action(state):
    notify(state, 'info', f'Running data extraction...')
    detector.run()

    
import gradio as gr
import os 
from ultralytics import YOLO
import cv2

model = YOLO("/media/yashas/Whatev/project/smoke_detector/gradio_app/smoke_detection.pt")

class Drone:
  def __init__(self) -> None:
    pass
  
  def generate_commands(self):
    #   This will generate commands for the object to move LEFT, RIGHT, UP or DOWN
        pass

  def calculate_distance(self):
    #   calculate the distance of the object from the center of the plane
        pass
  
  def manual_annotation(self):
    #   Users should be able to click on the object in video and gets its co-ordinates
        pass
  
  def detect_object_videowise(self, video):

        result = model.predict(source=video, save=True, name="result_video", verbose = True, device=0)

        print (result)

        files = os.listdir(result[0].save_dir)

        return os.path.join(result[0].save_dir, files[0])
  

    

# iface = gr.Interface(

#             fn = detect_object_videowise,

#             inputs=gr.Video(),

#             examples=['/media/yashas/Whatev/project/smoke_detector/gradio_app/bomb.mp4', '/media/yashas/Whatev/project/smoke_detector/gradio_app/Smoke stacks drone footage.mp4'],

#             cache_examples=True,

#             outputs="playable_video",

#             title = "Smoke detection from drone video",

            
#         )


# iface.launch()

drone = Drone()

drone.detect_object_videowise('/media/yashas/Whatev/project/smoke_detector/gradio_app/bomb.mp4')
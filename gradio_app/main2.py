import gradio as gr
import os 
from ultralytics import YOLO

model = YOLO("/media/yashas/Whatev/project/smoke_detector/gradio_app/smoke_detection.pt")

def detect_object_videowise(video):

  result = model.predict(source=video, save=True, name="result_video", verbose = False, stream=True)

  print (result)

  files = os.listdir(result[0].save_dir)

  return os.path.join(result[0].save_dir, files[0])

with gr.Blocks() as demo:
    video = gr.Video(label="Video Input")
    output = "playable_video"
    greet_btn = gr.Button("Greet")
    greet_btn.click(fn=detect_object_videowise, inputs=video, outputs=output, api_name="greet")

demo.launch()
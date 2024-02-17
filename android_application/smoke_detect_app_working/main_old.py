from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Ellipse
from math import sqrt

# Mock function to simulate object detection
def detect_objects(frame):
    # Placeholder implementation
    return [(100, 100, 200, 200)]  # Example bounding box coordinates

class TouchVideo(Video):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            center_x = self.x + self.width / 2
            center_y = self.y + self.height / 2
            distance = sqrt((center_x - touch.x) ** 2 + (center_y - touch.y) ** 2)
            App.get_running_app().distance_label.text = f'Distance from center: {distance:.2f}'
            return True
        return super(TouchVideo, self).on_touch_down(touch)

class VideoPlayerApp(App):
    distance_label = None
    paused = False

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Video
        self.video = TouchVideo(size_hint=(1, 0.8))
        layout.add_widget(self.video)

        # Button layout
        button_layout = BoxLayout(size_hint=(1, 0.1))
        layout.add_widget(button_layout)

        # Button to browse video
        browse_button = Button(text='Browse', size_hint=(0.2, 1))
        browse_button.bind(on_press=self.browse)
        button_layout.add_widget(browse_button)

        # Button to pause/resume video
        self.pause_button = Button(text='Pause', size_hint=(0.2, 1))
        self.pause_button.bind(on_press=self.pause_resume_video)
        button_layout.add_widget(self.pause_button)

        # Button to detect objects
        self.detect_button = Button(text='Detect Objects', size_hint=(0.2, 1))
        self.detect_button.bind(on_press=self.detect_objects)
        button_layout.add_widget(self.detect_button)

        # Label to display distance
        self.distance_label = Label(text='Distance from center: 0', size_hint=(1, 0.05))
        layout.add_widget(self.distance_label)

        # Label to display detected objects
        self.objects_label = Label(text='Detected Objects:', size_hint=(1, 0.05))
        layout.add_widget(self.objects_label)

        return layout

    def browse(self, instance):
        file_chooser = FileChooserListView(path='.')
        file_chooser.bind(selection=self.load_video)
        self.root.add_widget(file_chooser)

    def load_video(self, instance, value):
        if value:
            selected_file = value[0]
            self.video.source = selected_file
            self.video.state = 'play'

    def on_stop(self):
        self.video.state = 'stop'
        self.video = None

    def pause_resume_video(self, instance):
        if self.video.state == 'play':
            self.video.state = 'pause'
            self.paused = True
            self.pause_button.text = 'Resume'
        else:
            self.video.state = 'play'
            self.paused = False
            self.pause_button.text = 'Pause'

    def detect_objects(self, instance):
        if self.paused:
            # Capture frame
            frame = self.video.texture
            # Simulate object detection
            bounding_boxes = detect_objects(frame)
            detected_objects_text = ""
            for box in bounding_boxes:
                center_x = (box[0] + box[2]) / 2
                center_y = (box[1] + box[3]) / 2
                distance = sqrt((self.video.width / 2 - center_x) ** 2 + (self.video.height / 2 - center_y) ** 2)
                detected_objects_text += f'Bounding Box: {box}, Distance from center: {distance:.2f}\n'
            self.objects_label.text = detected_objects_text
        else:
            self.objects_label.text = "Video must be paused to detect objects."

if __name__ == '__main__':
    VideoPlayerApp().run()

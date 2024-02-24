from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.graphics import Color, Rectangle, Line
from math import sqrt
import kivy

kivy.require('1.9.0')

# Mock function to simulate object detection
def detect_objects(frame):
    # Placeholder implementation
    return [(100, 100, 200, 200)]  # Example bounding box coordinates

class TouchVideo(Video):
    def __init__(self, **kwargs):
        super(TouchVideo, self).__init__(**kwargs)
        self.rect = None
        self.lines = []

    def draw_lines(self):
        self.lines = []

        # Vertical line dividing the frame into left and right halves
        vertical_line_x = self.x + self.width / 2
        self.lines.extend([vertical_line_x, self.y, vertical_line_x, self.y + self.height])

        # Horizontal line dividing the frame into top and bottom halves
        horizontal_line_y = self.y + self.height / 2
        self.lines.extend([self.x, horizontal_line_y, self.x + self.width, horizontal_line_y])

        with self.canvas:
            Color(1, 1, 1)  # White color
            for i in range(0, len(self.lines), 4):
                Line(points=self.lines[i:i + 4], width=2)

    def on_size(self, instance, value):
        self.draw_lines()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            center_x = self.x + self.width / 2
            center_y = self.y + self.height / 2
            distance = sqrt((center_x - touch.x) ** 2 + (center_y - touch.y) ** 2)
            App.get_running_app().distance_label.text = f'Distance from center: {distance:.2f}'

            # Calculate movement needed to align with axes
            x_movement = center_x - touch.x
            y_movement = center_y - touch.y

            # Determine direction to move towards origin
            direction = ""
            if x_movement > 0:
                direction += "right"
            elif x_movement < 0:
                direction += "left"
            if y_movement > 0:
                direction += ", down"
            elif y_movement < 0:
                direction += ", up"
            if not direction:
                direction = "You are at the origin"

            App.get_running_app().move_label.text = f'Movement to align with axes: ({x_movement:.2f}, {y_movement:.2f})'
            App.get_running_app().direction_label.text = f'Direction to move towards origin: {direction}'

            # Draw rectangle around touch area
            if self.rect:
                self.remove_widget(self.rect)
            self.rect = Rectangle(pos=(touch.x - 15, touch.y - 15), size=(30, 30))
            self.canvas.add(Color(1, 0, 0, 0.5))  # Red color with 50% opacity
            self.canvas.add(self.rect)

            return True
        return super(TouchVideo, self).on_touch_down(touch)

class VideoPlayerApp(App):
    distance_label = None
    move_label = None
    direction_label = None
    objects_label = None
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
        self.distance_label = Label(text='Distance from center: 0', size_hint=(1, None), height=30)
        layout.add_widget(self.distance_label)

        # Label to display movement needed to align with axes
        self.move_label = Label(text='Movement to align with axes:', size_hint=(1, None), height=30)
        layout.add_widget(self.move_label)

        # Label to display direction to move towards origin
        self.direction_label = Label(text='Direction to move towards origin:', size_hint=(1, None), height=30)
        layout.add_widget(self.direction_label)

        # Label to display detected objects
        self.objects_label = Label(text='Detected Objects:', size_hint=(1, None), height=30)
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

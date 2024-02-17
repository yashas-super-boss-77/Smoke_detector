from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Ellipse
from math import sqrt

class VideoPlayerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')


        self.video = Video()
        layout.add_widget(self.video)
        
        browse_button = Button(text='Browse')
        browse_button.bind(on_press=self.browse)
        layout.add_widget(browse_button)

        # Button to pause/resume video
        self.pause_button = Button(text='Pause')
        self.pause_button.bind(on_press=self.pause_resume_video)
        layout.add_widget(self.pause_button)

        # Label to display distance
        self.distance_label = Label(text='Distance from center: 0')
        layout.add_widget(self.distance_label)
        
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
            self.pause_button.text = 'Resume'
        else:
            self.video.state = 'play'
            self.pause_button.text = 'Pause'

    def calculate_distance(self, touch):
        video_pos = self.video.to_local(*touch.pos)
        center_x = self.video.width / 2
        center_y = self.video.height / 2
        distance = sqrt((center_x - video_pos[0]) ** 2 + (center_y - video_pos[1]) ** 2)
        return distance
    
    def on_touch_down(self, touch):
        if self.video.collide_point(*touch.pos):
            distance = self.calculate_distance(touch)
            self.distance_label.text = f'Distance from center: {distance:.2f}'



if __name__ == '__main__':
    VideoPlayerApp().run()

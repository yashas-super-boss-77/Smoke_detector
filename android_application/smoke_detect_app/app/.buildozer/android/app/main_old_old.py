from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView, FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from math import sqrt
import os
import platform

class TouchVideo(Video):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            center_x = self.x + self.width / 2
            center_y = self.y + self.height / 2
            distance = sqrt((center_x - touch.x) ** 2 + (center_y - touch.y) ** 2)
            print(f"Distance from center: {distance:.2f}")
            App.get_running_app().distance_label.text = f'Distance from center: {distance:.2f}'
            return True
        return super(TouchVideo, self).on_touch_down(touch)

class VideoPlayerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Video
        self.video = TouchVideo()
        layout.add_widget(self.video)

        # Button to browse video
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
        if platform.system() == 'Linux':
            file_chooser = FileChooserListView()
            file_chooser.bind(on_submit=self.load_video)
            file_chooser.bind(on_cancel=self.dismiss_popup)
            self.popup = Popup(title='Choose a video file', content=file_chooser, size_hint=(None, None), size=(400, 400))
            self.popup.open()
        elif platform.system() == 'Android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            intent = Intent()
            intent.setAction(Intent.ACTION_GET_CONTENT)
            intent.setType("video/*")
            currentActivity = PythonActivity.mActivity
            currentActivity.startActivityForResult(intent, 1)

    def load_video(self, instance, value):
        if platform.system() == 'Linux':
            self.dismiss_popup()
            selected_file = value[0]
            self.video.source = selected_file
            self.video.state = 'play'
        elif platform.system() == 'Android':
            from jnius import autoclass
            Uri = autoclass('android.net.Uri')
            Intent = autoclass('android.content.Intent')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            uri = value[0]
            selected_file = activity.getContentResolver().openInputStream(uri)
            self.video.source = selected_file
            self.video.state = 'play'

    def dismiss_popup(self, instance):
        self.popup.dismiss()

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

if __name__ == '__main__':
    VideoPlayerApp().run()

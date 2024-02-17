import kivy
import random

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

kivy.require('1.9.0')

class App_pa(App):
    def build(self):
        
        layout = BoxLayout(padding=10)
        colors = ['red', 'green', 'blue', 'purple']

        for i in range(5):
            btn = Button(text="Button #%s" % (i+1),
                         background_color=random.choice(colors)
                         )

            layout.add_widget(btn)
        return layout
        return label

if __name__ == '__main__':
    app_pa = App_pa()
    app_pa.run()
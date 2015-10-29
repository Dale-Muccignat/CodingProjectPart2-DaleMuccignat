__author__ = 'Dale Muccignat'

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window


class GuiTest(App):
    def __init__(self):
        self.trip_details = []

    def build(self):
        Window.size = (350, 700)
        self.title = "Part 2"
        self.root = Builder.load_file('gui.kv')
        # self.state_codes =
        return self.root

    def update_button_press(self):
        print("update_button pressed")

    def change_state(self, state_code):
        print("changed")


GuiTest().run()

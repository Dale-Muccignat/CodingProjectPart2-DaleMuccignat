__author__ = 'Dale Muccignat'

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.core.window import Window
from currency import get_all_details


class GuiTest(App):
    current_state = StringProperty()
    country_names = ListProperty()


    def __init__(self, **kwargs):
        super(GuiTest, self).__init__(**kwargs)
        self.trip_details = []

    def build(self):
        Window.size = (350, 700)
        country_list = GuiTest.sort_trips()
        self.title = "Part 2"
        self.root = Builder.load_file('gui.kv')
        # print(country_list)
        # print(country_list[0])
        # Set current state to first country in list
        self.current_state = str(country_list[0])
        #
        self.country_names = country_list
        return self.root

    # def update_button_press(self):
    #     print("update_button pressed")
    #
    def change_state(self):
        self.root.ids.test_label.text = "woo"
        print("changed")

    @staticmethod
    def sort_trips():
        """ creates list of countries to display on spinner """
        trip_countries = []
        file = open("config.txt", mode="r", encoding="UTF-8")
        # Generates list of country names
        for line in file:
            parts = line.strip().split(",")
            trip_countries.append(parts[0])
        file.close()
        return sorted(trip_countries)


GuiTest().run()
# print(GuiTest().sort_trips())
__author__ = 'Dale Muccignat'

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ListProperty
import time
from kivy.core.window import Window
from currency import get_all_details
from trip import Details

# on_text_validate

class GuiTest(App):
    current_state = StringProperty()
    home_state = StringProperty()
    country_names = ListProperty()

    def __init__(self, **kwargs):
        super(GuiTest, self).__init__(**kwargs)
        self.trip_details = []

    def build(self):
        Window.size = (350, 700)
        country_list = GuiTest.sort_trips()
        self.title = "Part 2"
        self.root = Builder.load_file('gui.kv')
        # Set current state to first country in list
        self.current_state = str(country_list[0])
        # Add values to spinner
        self.country_names = country_list
        return self.root

    # def update_button_press(self):
    #     print("update_button pressed")

    def change_state(self, text):
        # self.root.ids.test_label.text = text
        print("country changed")

    @staticmethod
    def sort_trips():
        """ creates list of countries to display on spinner """
        trip_countries = []
        file = open("config.txt", mode="r", encoding="UTF-8")
        GuiTest.home_state = file.readline()
        # Generates list of country names
        for line in file:
            parts = line.strip().split(",")
            trip_countries.append(parts[0])
        file.close()
        return sorted(trip_countries)

    @staticmethod
    def get_current_country():
        details = Details()
        file = open("config.txt", mode="r", encoding="UTF-8")
        file.readline()
        for line in file:
            parts = line.strip().split(",")
            details.add(parts[0], parts[1], parts[2])
        current_country = details.current_country(GuiTest.get_current_time())
        file.close()
        return "Your Location: \n" + current_country

    @staticmethod
    def get_current_time():
        current_date = time.strftime("%Y/%m/%d")
        return current_date


GuiTest().run()
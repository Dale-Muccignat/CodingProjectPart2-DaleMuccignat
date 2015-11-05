from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ListProperty
import time
from kivy.core.window import Window
from currency import get_all_details
from currency import convert
from trip import Details

__author__ = 'Dale Muccignat'


class GuiTest(App):
    current_state = StringProperty()
    home_state = StringProperty()
    country_names = ListProperty()
    conversion_rate = 0

    def __init__(self, **kwargs):
        super(GuiTest, self).__init__(**kwargs)

    def build(self):
        Window.size = (350, 700)
        country_list = GuiTest.sort_trips()
        print(country_list)
        self.title = "Part 2"
        self.root = Builder.load_file('gui.kv')
        # Set current state to first country in list
        self.current_state = str(country_list[0])
        # Add values to spinner
        self.country_names = country_list
        return self.root

    def conversion_rate_update(self, from_currency, too_currency):
        """ Update currency conversion rate """
        self.conversion_rate = convert(1, from_currency, too_currency)
        print("Rate changed too: " + str(self.conversion_rate))

    def change_state(self, current_country):
        """ When country is changed, update currency"""
        country_dict = get_all_details()
        # Find currency code for current country
        too_currency = ""
        for parts in country_dict:
            if current_country == parts:
                values = country_dict[parts]
                too_currency = values[0]
        # Update conversion rate
        GuiTest().conversion_rate_update("AUD", too_currency)
        print("country changed too: " + current_country)

    def convert_amount(self, amount, key):
        """ Convert amount"""
        amount = float(amount)
        print("Rate: " + str(self.conversion_rate))
        if key == "True":
            print(amount * self.conversion_rate)
            return amount * self.conversion_rate
            # else:
            #     print(amount * (1 / self.conversion_rate))
            #     return amount * (1 / self.conversion_rate)

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
        """ Returns name of current country"""
        details = Details()
        file = open("config.txt", mode="r", encoding="UTF-8")
        file.readline()
        for line in file:
            parts = line.strip().split(",")
            details.add(parts[0], parts[1], parts[2])
        current_country = details.current_country(GuiTest.get_current_time())
        print("Current country: " + current_country)
        file.close()
        return "Your Location: \n" + current_country

    @staticmethod
    def get_current_time():
        """ Returns current time"""
        current_date = time.strftime("%Y/%m/%d")
        print(current_date)
        return current_date


GuiTest().run()

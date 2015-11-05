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

    def __init__(self, **kwargs):
        super(GuiTest, self).__init__(**kwargs)
        self.conversion_rate = 0

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

    def conversion_rate_update(self, from_currency, to_currency):
        """ Update currency conversion rate """
        self.conversion_rate = convert(1, from_currency, to_currency)
        print("Rate changed to: " + str(self.conversion_rate))
        # Error checking, enable input if success
        if self.conversion_rate == -1:
            self.root.ids.status_label.text = "Update Failed"
        else:
            self.root.ids.home_country_input.readonly = False
            self.root.ids.travel_country_input.readonly = False
            self.clear_inputs()

    def change_state(self, current_country):
        """ When country is changed, update currency"""
        country_dict = get_all_details()
        # Find currency code for current country
        to_currency = ""
        for parts in country_dict:
            if current_country == parts:
                values = country_dict[parts]
                to_currency = values[1]
        # Update conversion rate
        self.conversion_rate_update("AUD", to_currency)
        print("country changed to: " + current_country)

    def convert_amount(self, amount, key):
        """ Convert amount"""
        try:
            amount = float(amount)
            travel_country = self.root.ids.country_spinner.text
            travel_details = []
            file = open("currency_details.txt", mode="r", encoding="UTF-8")
            # Make list of details for travel country
            # As home country is always australia, details were manually entered
            for line in file:
                parts = line.strip().split(",")
                if parts[0] == travel_country:
                    travel_details.append(parts[1])
                    travel_details.append(parts[2])
            print("Rate: " + str(self.conversion_rate))
            # If key is true, user is converting from home
            if key:
                file.close()
                result = format(amount * self.conversion_rate, ".3f")
                self.root.ids.travel_country_input.text = str(result)
                self.root.ids.status_label.text = "AUD ($) to {} ({})".format(travel_details[0], travel_details[1])
                print(result)
            else:
                result = format(amount * (1 / self.conversion_rate), ".3f")
                self.root.ids.home_country_input.text = str(result)
                self.root.ids.status_label.text = "{} ({}) to AUD ($)".format(travel_details[0], travel_details[1])
                print(result)
        except ValueError:
            self.clear_inputs()
            self.root.ids.status_label.text = "Invalid Number!"

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

    def clear_inputs(self):
        self.root.ids.home_country_input.text = ""
        self.root.ids.travel_country_input.text = ""

GuiTest().run()

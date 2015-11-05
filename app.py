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
    home_country = StringProperty()
    travel_country = StringProperty()
    country_names = ListProperty()

    def __init__(self, **kwargs):
        super(GuiTest, self).__init__(**kwargs)
        self.conversion_rate = 0
        self.current_date = self.get_current_date()
        self.country_names = self.sort_trips()
        # Details lists of form [code, symbol]
        self.home_details = []
        self.travel_details = []

    def build(self):
        Window.size = (350, 700)
        self.title = "Part 2"
        self.root = Builder.load_file('gui.kv')
        # Add values to spinner
        return self.root

    def get_country_details(self):
        travel_country = self.travel_country
        home_country = self.home_country
        print(home_country)
        print(travel_country)
        country_details_dict = get_all_details()
        # Find currency code/symbol for home/travel country
        for parts in country_details_dict:
            if travel_country == parts:
                self.travel_details = country_details_dict[parts]
            if home_country == parts:
                self.home_details = country_details_dict[parts]

    def get_current_country(self):
        """ Returns name of current country"""
        details = Details()
        file = open("config.txt", mode="r", encoding="UTF-8")
        file.readline()
        for line in file:
            parts = line.strip().split(",")
            details.add(parts[0], parts[1], parts[2])
        current_country = details.current_country(self.current_date)
        file.close()
        print("Current country: " + current_country)
        return current_country

    def update_rate(self):
        """ When country is changed, update currency"""
        self.travel_country = self.root.ids.country_spinner.text
        # If spinner is blank, set spinner to current country
        if self.travel_country == "":
            self.root.ids.country_spinner.text = self.get_current_country()
            self.travel_country = self.root.ids.country_spinner.text
        # Retrieve country/trip details
        self.get_country_details()
        # Update conversion rate
        self.conversion_rate = convert(1, self.home_details[1], self.travel_details[1])
        print("Rate changed to: " + str(self.conversion_rate))
        # Error checking, enable input if success
        if self.conversion_rate == -1:
            self.root.ids.status_label.text = "Update Failed"
        else:
            self.root.ids.home_country_input.readonly = False
            self.root.ids.travel_country_input.readonly = False
            self.clear_inputs()
        print("country changed to: " + self.travel_country)

    def convert_amount(self, amount, key):
        """ Convert amount"""
        try:
            amount = float(amount)
            print("Rate: " + str(self.conversion_rate))
            # If key is true, user is converting from home
            if key:
                result = format(amount * self.conversion_rate, ".3f")
                self.root.ids.travel_country_input.text = str(result)
                self.root.ids.status_label.text = "{} ({}) to {} ({})".format(self.home_details[1], self.home_details[2], self.travel_details[1], self.travel_details[2])
                print(result)
            else:
                result = format(amount * (1 / self.conversion_rate), ".3f")
                self.root.ids.home_country_input.text = str(result)
                self.root.ids.status_label.text = "{} ({}) to {} ({})".format(self.travel_details[1], self.travel_details[2], self.home_details[1], self.home_details[2])
                print(result)
        except ValueError:
            self.clear_inputs()
            self.root.ids.status_label.text = "Invalid Number!"

    def clear_inputs(self):
        self.root.ids.home_country_input.text = ""
        self.root.ids.travel_country_input.text = ""

    def sort_trips(self):
        """ creates list of countries to display on spinner """
        trip_countries = []
        file = open("config.txt", mode="r", encoding="UTF-8")
        self.home_country = file.readline().strip()
        # Generates list of country names
        for line in file:
            parts = line.strip().split(",")
            trip_countries.append(parts[0])
        file.close()
        return sorted(trip_countries)

    @staticmethod
    def get_current_date():
        """ Returns current time"""
        current_date = time.strftime("%Y/%m/%d")
        print(current_date)
        return current_date

GuiTest().run()

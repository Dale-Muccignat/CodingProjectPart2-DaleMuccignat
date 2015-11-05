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
        self.country_names = sorted(self.sort_trips().keys())
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
                # If currency symbol is the same, and list not blank, return "Same"
                if self.travel_details != [] and country_details_dict[parts][2] == self.travel_details[2]:
                    return "Same"
                self.travel_details = country_details_dict[parts]
            else:
                self.toggle_inputs_readonly(True)
                self.root.ids.status_label.text = "Invalid Name!"
            if home_country == parts:
                self.home_details = country_details_dict[parts]
            else:
                self.toggle_inputs_readonly(True)
                self.root.ids.status_label.text = "Invalid Name!"

    def get_current_country(self):
        """ Returns name of current country"""
        details = Details()
        trip_countries_dict = self.sort_trips()
        for part in trip_countries_dict:
            details.add(trip_countries_dict[part][0], trip_countries_dict[part][1], trip_countries_dict[part][2])
        current_country = details.current_country(self.current_date)
        print("Current country: " + current_country)
        return current_country

    def update_rate(self, key):
        """ When country is changed, update currency"""
        self.travel_country = self.root.ids.country_spinner.text
        get_country_details = self.get_country_details()
        # If spinner is blank, set spinner to current country
        if self.travel_country == "":
            self.root.ids.country_spinner.text = self.get_current_country()
            self.travel_country = self.root.ids.country_spinner.text
        # Retrieve country/trip details
        # If currency is the same and function activated by spinner, don't update
        if get_country_details == "Same" and key:
            pass
        # If lists are still empty, don't update
        elif self.home_details == [] or self.travel_details == []:
            pass
        else:
            self.conversion_rate = convert(1, self.home_details[1], self.travel_details[1])
            # Update conversion rate
            print("Rate changed to: " + str(self.conversion_rate))
            # Error checking, enable input if success
            if self.conversion_rate == -1:
                self.root.ids.status_label.text = "Update Failed"
                self.toggle_inputs_readonly(True)
            else:
                self.clear_inputs()
                self.toggle_inputs_readonly(False)
                self.root.ids.status_label.text = "Updated at: " + time.strftime("%I:%M:%S%p")
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
                format_tuple_travel = (self.home_details[1], self.home_details[2], self.travel_details[1], self.travel_details[2])
                self.root.ids.status_label.text = "{} ({}) to {} ({})".format(*format_tuple_travel)
                print(result)
            else:
                result = format(amount / self.conversion_rate, ".3f")
                self.root.ids.home_country_input.text = str(result)
                format_tuple_home = (self.travel_details[1], self.travel_details[2], self.home_details[1], self.home_details[2])
                self.root.ids.status_label.text = "{} ({}) to {} ({})".format(*format_tuple_home)
                print(result)
        except ValueError:
            self.clear_inputs()
            self.root.ids.status_label.text = "Invalid Number!"

    def sort_trips(self):
        """ creates list of countries to display on spinner """
        trip_countries = {}
        #TODO Fix the silly error
        # try:
        #     file = open("config.txt", mode="r", encoding="UTF-8")
        #     self.home_country = file.readline().strip()
        #     # Generates list of country names
        #     for line in file:
        #         parts = line.strip().split(",")
        #         trip_countries[parts[0]] = (parts[0], parts[1], parts[2])
        #     file.close()
        # except FileNotFoundError:
        #     self.toggle_inputs_readonly(True)
        #     self.root.ids.status_label.text = "Config not found!"
        return trip_countries

    def clear_inputs(self):
        self.root.ids.home_country_input.text = ""
        self.root.ids.travel_country_input.text = ""

    def toggle_inputs_readonly(self, key):
        self.root.ids.home_country_input.readonly = key
        self.root.ids.travel_country_input.readonly = key

    @staticmethod
    def get_current_date():
        """ Returns current time"""
        current_date = time.strftime("%Y/%m/%d")
        print(current_date)
        return current_date

GuiTest().run()

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
    current_country = StringProperty()
    country_names = ListProperty()

    def __init__(self, **kwargs):
        super(GuiTest, self).__init__(**kwargs)
        self.conversion_rate = 0
        self.current_date = self.get_current_date()
        # Details lists of form [code, symbol]
        self.home_details = []
        self.travel_details = []
        # indicator whether symbol is the same
        self.update_indicator = True

    def build(self):
        Window.size = (350, 700)
        self.title = "Part 2"
        self.root = Builder.load_file('gui.kv')
        # Add values to spinner
        self.country_names = sorted(self.sort_trips().keys())
        # Get current country
        self.current_country = self.get_current_country()
        self.toggle_inputs_disabled(True)
        return self.root

    def toggle_inputs_disabled(self, key):
        """ Sets text input to readonly """
        self.root.ids.home_country_input.disabled = key
        self.root.ids.travel_country_input.disabled = key

    def clear_inputs(self):
        """ Clears text input """
        self.root.ids.home_country_input.text = ""
        self.root.ids.travel_country_input.text = ""

    def get_country_details(self):
        """ Retrieves country details for home/travel """
        travel_country = self.travel_country
        home_country = self.home_country
        country_details_dict = get_all_details()
        # Find currency code/symbol for home/travel country
        for parts in country_details_dict:
            if travel_country == parts:
                # If currency symbol is the same, and list not blank, return "Same"
                if self.travel_details and country_details_dict[parts][2] == self.travel_details[2]:
                    self.update_indicator = False
                self.travel_details = country_details_dict[parts]
            if home_country == parts:
                self.home_details = country_details_dict[parts]
        # If either list is blank, display error
        if not self.travel_details or not self.home_details:
            self.toggle_inputs_disabled(True)
            self.root.ids.status_label.text = "Invalid Name!"

    def update_rate(self, key):
        """ When country is changed/button pressed, update currency """
        # If activated by button (key=True) spinner is blank, set spinner to current country
        if self.root.ids.country_spinner.text == "" and key:
            self.root.ids.country_spinner.text = self.current_country
        self.travel_country = self.root.ids.country_spinner.text
        self.get_country_details()
        # Retrieve country/trip details
        # If currency is the same and function activated by spinner, don't update
        # If lists are still empty, don't update
        if (key or self.update_indicator) and self.travel_details and self.home_details:
            # Update conversion rate
            self.conversion_rate = convert(1, self.home_details[1], self.travel_details[1])
            # Error checking, enable input if conversion success
            if self.conversion_rate == -1:
                self.root.ids.status_label.text = "Update Failed"
                self.toggle_inputs_disabled(True)
            else:
                self.clear_inputs()
                self.toggle_inputs_disabled(False)
                self.root.ids.status_label.text = "Updated at: " + time.strftime("%I:%M:%S%p")
        # Reset indicators
        self.update_indicator = True

    def get_current_country(self):
        """ Returns name of current country """
        details = Details()
        trip_countries_dict = self.sort_trips()

        for part in trip_countries_dict:
            details.add(trip_countries_dict[part][0], trip_countries_dict[part][1], trip_countries_dict[part][2])
        current_country = details.current_country(self.current_date)
        print(current_country)
        return current_country

    def convert_amount(self, amount, key):
        """ Convert amount """
        try:
            amount = float(amount)
            # If key is true, user is converting from home
            if key:
                result = format(amount * self.conversion_rate, ".3f")
                self.root.ids.travel_country_input.text = str(result)
                self.root.ids.status_label.text = "{} ({}) to {} ({})".format(self.home_details[1],
                                                                              self.home_details[2],
                                                                              self.travel_details[1],
                                                                              self.travel_details[2])
            else:
                result = format(amount / self.conversion_rate, ".3f")
                self.root.ids.home_country_input.text = str(result)
                self.root.ids.status_label.text = "{} ({}) to {} ({})".format(self.travel_details[1],
                                                                              self.travel_details[2],
                                                                              self.home_details[1],
                                                                              self.home_details[2])
        except ValueError:
            self.clear_inputs()
            self.root.ids.status_label.text = "Invalid Number!"

    def sort_trips(self):
        """ creates list of countries to display on spinner """
        trip_countries = {}
        try:
            file = open("config.txt", mode="r", encoding="UTF-8")
            self.home_country = file.readline().strip()
            # Generates list of country names
            for line in file:
                parts = line.strip().split(",")
                trip_countries[parts[0]] = (parts[0], parts[1], parts[2])
            file.close()
        except FileNotFoundError:
            self.clear_inputs()
            self.toggle_inputs_disabled(True)
            self.root.ids.status_label.text = "Config not found!"
        return trip_countries

    @staticmethod
    def get_current_date():
        """ Returns current time """
        current_date = time.strftime("%Y/%m/%d")
        return current_date

GuiTest().run()

"""
Initial Web Scraping for Final Python Project.

Matt Renaud
"""

from html.parser import HTMLParser
import urllib.request
import datetime
import json

class WeatherScraper(HTMLParser):
    """A class that scrapes the weather."""

    def __init__(self):
        """Initialize the variables."""
        HTMLParser.__init__(self)
        self.key = ""
        self.value = ""
        self.weather_dict = dict()
        self.temp_dict = dict()
        self.counter = 0
        self.min = ""
        self.max = ""
        self.mean = ""
        self.td = False
        self.tr = False
        self.tbody = False
        self.inDay = False
        self.previous = True

    def handle_starttag(self, tag, attrs):
        """Htmlparser method that will handle the start of tags. Will stop parsing when there is no previous button on the page."""
        if tag == "tbody":
            self.tbody = True
        if tag == "tr" and self.tbody:
            self.tr = True
        if tag == "td" and self.tbody:
            self.td = True
        if tag == "abbr" and self.tbody:
            for name, value in attrs:
                if name == "title" and value != "Extreme" and value != "Average":
                    self.key = value
                    self.inDay = True
        if tag == "li":
            for name, value in attrs:
                if name == "class" and value == "previous disabled":
                    self.previous = False

    def handle_endtag(self, tag):
        """Htmlparser method that will handle the end of tags."""
        if tag == "tbody":
            self.tbody = False
        if tag == "td":
            self.td = False
        if tag == "tr":
            self.tr = False
            self.inDay = False
            self.counter = 0

    def handle_data(self, data):
        """Htmlparser method that will handle the data inside tags."""
        if(self.tr and self.td):

            self.counter += 1

            try:
                float(data)
            except Exception:
                return

            if "M" not in data and self.inDay:
                if(self.counter == 1):
                    self.max = data
                elif(self.counter == 2):
                    self.min = data
                elif(self.counter == 3):
                    self.mean = data

            if(self.inDay):
                self.temp_dict = {"Max Temp": self.max, "Min Temp": self.min, "Mean Temp": self.mean}
                self.weather_dict[self.key] = self.temp_dict

    def print(self):
        """Print the dictionary generated through scraping."""
        with open('weather_data.json', 'w', encoding='utf-8') as f:
            json.dump(self.weather_dict, f, ensure_ascii=False, indent=4)


def link():
    """Generate a link that will be used to scrape all weather data."""
    parser = WeatherScraper()
    cur_year = datetime.date.today().year
    cur_month = datetime.date.today().month
    while parser.previous:
        with urllib.request.urlopen('https://climate.weather.gc.ca/'
                                    'climate_data/daily_data_e.html?StationID=27174&timeframe=2&'
                                    'StartYear=1840&EndYear=2018&Day=1&Year='
                                    f'{cur_year}&Month={cur_month}#') as response:
            html = str(response.read())
            parser.feed(html)

            if cur_month != 1:
                cur_month -= 1
            else:
                cur_month = 12
                cur_year -= 1

    parser.print()
    return parser.weather_dict


if __name__ == "__main__":
    print(link())

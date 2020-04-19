"""
Module that handles the main inputs for the application.

Matt Renaud
"""

import db_operations
import scrape_weather
import plot_operations
import sqlite3
import matplotlib.pyplot as plt


class WeatherProcessor():
    """The main processing of the weather application."""

    def main(self):
        """Function that queries to update, download,
        or input data and uses other modules to plot."""
        db = db_operations.DBOperations()
        p = plot_operations.PlotOperations()

        update = input("Would you like to update the data? y/n: ")
        if update == "y" or update == "Y":
            dict = scrape_weather.link()
            db.reset_data()
            db.add_data(dict)
            print("Data has been updated.")

        download = input("Would you like to download the data? y/n: ")
        if download == "y" or download == "Y":
            db.download_data()
            print("Data has been downloaded.")

        startyear = input("Enter a starting year (eg 1996): ")
        endyear = input("Enter an ending year (eg 2020): ")
        p.graph(db.select_data(int(startyear), int(endyear)),
                startyear, endyear)
        plt.show()

if __name__ == "__main__":
    wp = WeatherProcessor()
    wp.main()

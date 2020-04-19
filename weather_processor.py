import db_operations
import scrape_weather
import plot_operations
import sqlite3
import matplotlib.pyplot as plt

class WeatherProcessor():

    def __init__(self):
        pass

    def main(self):
        db = db_operations.DBOperations()
        p = plot_operations.PlotOperations()

        update = input("Would you like to update the data? y/n: ")
        if update == "y":
            dict = scrape_weather.link()
            db.reset_data()
            db.add_data(dict)
            print("Data has been updated.")

        download = input("Would you like to download the data? y/n: ")
        if download == "y":
            db.download_data()
            print("Data has been downloaded.")

        startyear = input("Enter a start year: ")
        endyear = input("Enter a end year: ")

        p.month_dict = db.retrieve_data()
        p.graph()
        plt.show()

if __name__ == "__main__":
    wp = WeatherProcessor()
    wp.main()

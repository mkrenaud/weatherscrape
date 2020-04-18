import db_operations
import scrape_weather
import plot_operations
import sqlite3
import matplotlib.pyplot as plt

class WeatherProcessor():

    def __init__(self):
        pass

    def main(self):
        download = input("Would you like to download the data? y/n: ")
        if download == "y":
            download()
        startyear = input("Enter a start year")
        endyear = input("Enter a end year")
        db = db_operations.DBOperations()
        dict = scrape_weather.link()
        db.add_data(dict)
        p = plot_operations.PlotOperations()
        p.month_dict = db.retrieve_data()
        p.graph()
        plt.show()
    
    def download(self, json):
        pdb = scrape_weather.WeatherScraper()
        pdb.print()
        print("Data has been downloaded.")

if __name__ == "__main__":
    wp = WeatherProcessor()
    wp.main()

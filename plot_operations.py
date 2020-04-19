"""
Module that handles graphing of data recieved from a dictionary.

Matt Renaud
"""

import db_operations
import scrape_weather
import sqlite3
import matplotlib.pyplot as plt


class PlotOperations():
    """Class that handles all plot operations."""

    def __init__(self):
        """Initializations."""
        self.month_dict = {}

    def graph(self, dictionary, startYear, endYear):
        """A function that will take in a dictionary, start, and end year.
        Will graph the data with the dictionary values it recieves."""
        try:
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.boxplot(dictionary.values())
            ax.set_xlabel('Month')
            ax.set_ylabel('Mean Temperatures')
            ax.set_title(f'Monthly Temperature Distribution ' +
                         f'from {startYear} to {endYear}')
        except Exception as e:
            print("Error printing data", e)


if __name__ == "__main__":
    db = db_operations.DBOperations()
    p = PlotOperations()
    p.month_dict = db.retrieve_data()
    p.graph(p.month_dict, 1996, 2020)
    plt.show()

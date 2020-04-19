import db_operations
import scrape_weather
import sqlite3
import matplotlib.pyplot as plt

class PlotOperations():

    def __init__(self):
        self.month_dict = {}
    
    def graph(self, dictionary, startYear, endYear):
        try:
            fig, ax = plt.subplots(figsize=(12,5))
            ax.boxplot(dictionary.values())
            ax.set_xlabel('Month')
            ax.set_ylabel('Mean Temperatures')
            ax.set_title(f'Monthly Temperature Distribution from {startYear} to {endYear}')
        except Exception as e:
            print("Error printing data", e)


if __name__ == "__main__":
    db = db_operations.DBOperations()
    p = PlotOperations()
    p.month_dict = db.retrieve_data()
    p.graph(p.month_dict, 2020, 1996)
    plt.show()
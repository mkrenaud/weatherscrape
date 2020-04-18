import db_operations
import scrape_weather
import sqlite3
import matplotlib.pyplot as plt

class PlotOperations():

    def __init__(self):
        self.month_dict = {}
    
    def graph(self):
        try:
            fig, ax = plt.subplots(figsize=(12,5))
            ax.boxplot(self.month_dict.values())
            ax.set_xlabel('Month')
            ax.set_ylabel('Mean Temperatures')
            ax.set_title(f'Monthly Temperature Distribution')
        except Exception as e:
            print("Error printing data", e)


if __name__ == "__main__":
    db = db_operations.DBOperations()
    dict = scrape_weather.link()
    db.add_data(dict)
    p = PlotOperations()
    p.month_dict = db.retrieve_data()
    print(p.month_dict)
    p.graph()
    plt.show()
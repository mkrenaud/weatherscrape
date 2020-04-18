import db_operations
import scrape_weather
import sqlite3
import matplotlib.pyplot as plt

class PlotOperations():

    def __init__(self):
        self.month_dict = dict()
        self.month = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]
        self.temp_array = []
        try:
            self.conn = sqlite3.connect("temps.sqlite")
            self.cur = self.conn.cursor()
            print("It connected.")
        except Exception as e:
                    print("Error in Initialize", e)
    
    def graph(self):
        try:
            for month in self.month:
                month_q = "%" + month + "%"
                for row in self.cur.execute("SELECT * FROM samples WHERE sample_date LIKE ?", (month_q,)):
                    self.temp_array.append(row[5])
                    # print(data)
                # print(month, self.temp_array)
                # ax.boxplot(self.temp_array)
                self.month_dict[month] =  self.temp_array
                self.temp_array = []
            self.cur.close()
            self.conn.close()
            # print(self.month_dict)
            fig, ax = plt.subplots(figsize=(12,5))
            ax.boxplot(self.month_dict.values())
            # ax.set_xticklabels(self.month_dict.keys())
            ax.set_xlabel('Month')
            ax.set_ylabel('Mean Temperatures')
            ax.set_title(f'Monthly Temperature Distribution')

        except Exception as e:
            print("Error printing data", e)


if __name__ == "__main__":
    p = PlotOperations()
    p.graph()
    plt.show()
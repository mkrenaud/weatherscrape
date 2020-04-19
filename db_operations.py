import sqlite3
import scrape_weather
import datetime
import logging
import json
import matplotlib.pyplot as plt

class DBOperations():

    def __init__(self):
        self.select_dict = {}
        self.month_dict = {}
        self.month = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]
        self.temp_array = []
        try:
            self.conn = sqlite3.connect("temps.sqlite")
            self.cur = self.conn.cursor()
            self.cur.execute("""create table samples (id integer primary key autoincrement not null, sample_date text not null, location text not null,
                        min_temp real not null,
                        max_temp real not null,
                        avg_temp real not null);""")
        except Exception as e:
                print("Error in table initialization", e)

    def add_data(self, dictionary):
        sql = """insert into samples (sample_date, location, min_temp,
              max_temp, avg_temp)
              values (?, ?, ?, ?, ?)"""
        try:
            for k, v in dictionary.items():
                data = (k, "Winnipeg, MB", v["Max Temp"], v["Min Temp"], v["Mean Temp"])
                self.cur.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            print("Error adding data", e)

    def reset_data(self):
        try:
            sqlDrop = "DROP TABLE Samples"
            self.cur.execute(sqlDrop)
            self.cur.execute("""create table samples (id integer primary key autoincrement not null, sample_date text not null, location text not null,
                        min_temp real not null,
                        max_temp real not null,
                        avg_temp real not null);""")
        except Exception as e:
            print("Error in Initialize: ", e)

    def retrieve_data(self, **kwargs):
        for month in self.month:
            month_q = "%" + month + "%"
            for row in self.cur.execute("SELECT * FROM samples WHERE sample_date LIKE ?", (month_q,)):
                self.temp_array.append(row[5])
            self.month_dict[month] =  self.temp_array
            self.temp_array = []
        self.cur.close()
        self.conn.close()
        return self.month_dict

    def print_data(self):
        try:
            for row in self.cur.execute("select * from samples"):
                print(row)
            self.cur.close()
            self.conn.close()
        except Exception as e:
            print("Error printing data", e)

    def download_data(self):
        try: 
            with open('weather_data.json', 'w', encoding='utf-8') as f:
                for row in self.cur.execute("select * from samples"):
                    json.dump(row, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("Error downloading data", e)

    def select_data(self, startYear, endYear):
        while(startYear <= endYear):
            for month in self.month:
                year_q = "%" + str(startYear) + "%"
                month_q = "%" + month + "%"
                for row in self.cur.execute("SELECT * from samples WHERE sample_date LIKE ? AND sample_date LIKE ?", (year_q,month_q,)):
                    self.temp_array.append(row[5])
                if month in self.select_dict:
                    for values in self.temp_array:
                        self.select_dict[month].append(values)
                else:
                    self.select_dict[month] = self.temp_array
                self.temp_array = []
            startYear = startYear + 1
        return self.select_dict
                

if __name__ == "__main__":
    db = DBOperations()
    #print(db.retrieve_data())
    print(db.select_data(1996, 2020))

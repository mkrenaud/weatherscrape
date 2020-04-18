import sqlite3
import scrape_weather


class DBOperations():

    def __init__(self):
        try:
            self.conn = sqlite3.connect("temps.sqlite")
            self.cur = self.conn.cursor()
            sqlDrop = "DROP TABLE Samples"
            self.cur.execute(sqlDrop)
            self.cur.execute("""create table samples (id integer primary key autoincrement not null, sample_date text not null, location text not null,
                        min_temp real not null,
                        max_temp real not null,
                        avg_temp real not null);""")
        except Exception as e:
            print("Error in Initialize", e)

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

    def print_data(self):
        try:
            for row in self.cur.execute("select * from samples"):
                print(row)
            self.cur.close()
            self.conn.close()
        except Exception as e:
            print("Error printing data", e)


if __name__ == "__main__":
    dict = scrape_weather.link()
    db = DBOperations()
    db.add_data(dict)
    db.print_data()

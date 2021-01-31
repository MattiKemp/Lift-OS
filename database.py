import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta

# tutorial and error handling: https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

class Database:
    def __init__(self, user, password, host = '127.0.0.1', database = 'workout'):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.cnx = None
        try:
            self.cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("user or password error")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def add_time_now(self, name):
        cursor = self.cnx.cursor()
        date = datetime.now()
        add_time = ("INSERT INTO info_time "
                "(name, time)"
                "VALUES (%s, %s)")
        cursor.execute(add_time,(name, date))
        self.cnx.commit()
        cursor.close()

    def close(self):
        self.cnx.close()


def main():
    print('----database main----')
    db = Database('python','Hinoob22')
    db.add_time_now('matt')

if __name__ == '__main__':
    main()

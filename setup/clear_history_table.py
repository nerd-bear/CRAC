import sqlite3

db_connection = sqlite3.connect("./crac.db")
db_cursor = db_connection.cursor()
db_cursor.execute("DROP TABLE history")
db_cursor.execute("CREATE TABLE history(user_id, command, arguments, datetime)")
db_connection.commit()
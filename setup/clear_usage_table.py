import sqlite3

db_connection = sqlite3.connect("./crac.db")
db_cursor = db_connection.cursor()
db_cursor.execute("DROP TABLE usage")
db_cursor.execute("CREATE TABLE usage(command_name, arguments, level)")
db_connection.commit()
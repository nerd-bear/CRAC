import sqlite3
import datetime


def add_feedback(user_id: str, message: str) -> bool:
    """Uses SQLite to add user's feedback to feedback db table

    ### Params:
        `used_id`  `str`   The user id of the person who submitted the feedback.
        `message`  `str`   The name of the command that the user ran.

    ### Return:
        Returns a bool (True on success)
    """

    datetime_value = datetime.datetime.today().now().__format__("%S:%M:%H %d/%m/%y")

    db_connection = sqlite3.connect("./crac.db")
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        f'INSERT INTO feedback VALUES (\'{user_id}\', "{message}", "{datetime_value}")'
    )
    db_connection.commit()

    return True

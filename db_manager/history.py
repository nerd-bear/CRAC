import sqlite3
import datetime
import json

def add_history(user_id: int, command: str, arguments: list[str] = ["none"]) -> bool:
    """Uses SQLite to add user command to history of commands ran

    ### Params:
        `user_id`  `int`   The user id of the person who ran the command.
        `command`  `str`   The name of the command that the user ran.
        `arguments`  `list[str]`   The arguments passed in to the command, defaults to ["none"].

    ### Return:
        Returns a bool (True on success)
    """
    args_json = json.dumps(arguments)
    datetime_value = datetime.datetime.now().strftime("%S:%M:%H %d/%m/%y")
    
    db_connection = sqlite3.connect("./crac.db")
    db_cursor = db_connection.cursor()
    
    try:
        db_cursor.execute(
            "INSERT INTO history (user_id, command, arguments, datetime) VALUES (?, ?, ?, ?)",
            (user_id, command, args_json, datetime_value)
        )
        db_connection.commit()
        return True
    except sqlite3.Error as e:
        print(f"ERROR_LOG: SQLite error: {e}")
        return False
    finally:
        db_connection.close()
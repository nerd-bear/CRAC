import sqlite3
from typing import List, Tuple
import json

DB_PATH = "./crac.db"


def get_db_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_PATH)


def execute_query(query: str, params: Tuple = (), fetch: bool = False):
    """Execute a SQL query and optionally fetch results."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        conn.commit()
        return True


def get_usage(command_name: str) -> Tuple[str, str, str]:
    """Get usage information for a specific command.

    Args:
        command_name (str): The name of the command to retrieve.

    Returns:
        Tuple[str, str, str]: A tuple containing (command_name, arguments, level).
        Returns None if the command is not found.
    """
    query = "SELECT command_name, arguments, level FROM usage WHERE command_name = ?"
    result = execute_query(query, (command_name,), fetch=True)
    return result[0] if result else None


def get_all_usages() -> List[Tuple[str, str, str]]:
    """Get usage information for all commands.

    Returns:
        List[Tuple[str, str, str]]: A list of tuples, each containing (command_name, arguments, level).
    """
    query = "SELECT command_name, arguments, level FROM usage"
    return execute_query(query, fetch=True)


def add_usage(command_name: str, arguments: List[str], level: int) -> bool:
    """Add usage information for a command.

    Args:
        command_name (str): The name of the command to add.
        arguments (List[str]): The list of arguments the command accepts.
        level (int): The permission level of the command (0-3).

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    if not 0 <= level <= 3:
        raise ValueError("Level must be between 0 and 3")

    query = "INSERT INTO usage (command_name, arguments, level) VALUES (?, ?, ?)"
    args_json = json.dumps(arguments)
    return execute_query(query, (command_name, args_json, str(level)))
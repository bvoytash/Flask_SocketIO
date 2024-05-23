import sqlite3
import os

# Path to the SQLite database file
db_path = os.path.join(os.path.dirname(__file__), 'data.db')


def fetch_data_from_db():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM mouse_clicks')
        rows = cursor.fetchall()
        return rows


if __name__ == "__main__":
    data = fetch_data_from_db()
    print("Mouse Click Data:")
    for row in data:
        print(f"ID: {row[0]}, X: {row[1]}, Y: {row[2]}, Photo Path: {row[3]}")
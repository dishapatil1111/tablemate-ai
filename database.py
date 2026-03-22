import sqlite3


def create_database():

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        guests INTEGER,
        date TEXT,
        time TEXT,
        table_number INTEGER
    )
    """)

    conn.commit()
    conn.close()


def add_booking(name, guests, date, time, table_number):

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO reservations (name, guests, date, time, table_number) VALUES (?, ?, ?, ?, ?)",
        (name, guests, date, time, table_number)
    )

    conn.commit()
    conn.close()


def cancel_booking(reservation_id):

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM reservations WHERE id=?",
        (reservation_id,)
    )

    conn.commit()
    conn.close()


def get_bookings():

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reservations")

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_all_reservations():

    rows = get_bookings()

    data = []

    for r in rows:

        data.append({
            "id": r[0],
            "name": r[1],
            "guests": r[2],
            "date": r[3],
            "time": r[4],
            "table_number": r[5]
        })

    return data


def get_bookings_by_datetime(date, time):

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT table_number FROM reservations WHERE date=? AND time=?",
        (date, time)
    )

    rows = cursor.fetchall()

    conn.close()

    tables = [r[0] for r in rows]

    return tables


def get_bookings_by_table(table_id, date):

    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT time FROM reservations WHERE table_number=? AND date=?",
        (table_id, date)
    )

    rows = cursor.fetchall()

    conn.close()

    times = [r[0] for r in rows]

    return times
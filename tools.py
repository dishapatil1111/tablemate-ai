from database import (
    add_booking,
    cancel_booking,
    get_bookings,
    get_bookings_by_datetime
)
from tables import TABLES


def book_table(name, guests, date, time):

    if guests <= 0:
        return "❌ Invalid number of guests."

    booked_tables = get_bookings_by_datetime(date, time)

    sorted_tables = sorted(TABLES, key=lambda x: x["seats"])

    for table in sorted_tables:
        if table["seats"] >= guests and table["id"] not in booked_tables:
            add_booking(name, guests, date, time, table["id"])

            return f"""
✅ Reservation Confirmed!

👤 Name: {name}
👥 Guests: {guests}
📅 Date: {date}
⏰ Time: {time}
🍽 Table: {table['id']}
"""

    return "❌ No tables available for this time."


def cancel_reservation(reservation_id):
    cancel_booking(reservation_id)
    return f"✅ Reservation {reservation_id} cancelled."


def list_reservations():
    bookings = get_bookings()

    if not bookings:
        return "No reservations found."

    text = ""

    for b in bookings:
        text += f"""
ID: {b[0]}
Name: {b[1]}
Guests: {b[2]}
Date: {b[3]}
Time: {b[4]}
Table: {b[5]}

"""

    return text
from groq import Groq
import os
from dotenv import load_dotenv
import json
import re
from datetime import datetime, timedelta
from tools import book_table, cancel_reservation, list_reservations

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def normalize_datetime(date, time):

    # Normalize date
    if date.lower() == "today":
        date = datetime.now().strftime("%Y-%m-%d")

    elif date.lower() == "tomorrow":
        date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    # Normalize time
    time = time.lower().replace(" ", "")

    if "pm" in time:
        hour = int(time.replace("pm", ""))
        if hour != 12:
            hour += 12
        time = f"{hour:02d}:00"

    elif "am" in time:
        hour = int(time.replace("am", ""))
        time = f"{hour:02d}:00"

    return date, time


def run_agent(user_message):

    system_prompt = """
You are an AI restaurant reservation assistant.

STRICT RULES:
- Return ONLY valid JSON
- No explanation
- No extra text

Available actions:
1. book_table
2. cancel_reservation
3. list_reservations

BOOK FORMAT:
{
"action":"book_table",
"name":"Rahul",
"people":4,
"date":"tomorrow",
"time":"8pm"
}

CANCEL FORMAT:
{
"action":"cancel_reservation",
"id":2
}

LIST FORMAT:
{
"action":"list_reservations"
}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0
    )

    text = response.choices[0].message.content

    try:
        data = json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            data = json.loads(match.group())
        else:
            return "❌ Sorry, I couldn't understand."

    action = data.get("action")

    if action == "book_table":
        name = data.get("name")
        people = data.get("people")
        date = data.get("date")
        time = data.get("time")

        if not all([name, people, date, time]):
            return "❌ Missing booking details."

        date, time = normalize_datetime(date, time)

        return book_table(name, int(people), date, time)

    elif action == "cancel_reservation":
        return cancel_reservation(int(data.get("id")))

    elif action == "list_reservations":
        return list_reservations()

    return "❌ Invalid action."
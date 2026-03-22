#TableMate AI

TableMate AI is a simple web application that allows users to book restaurant tables using natural language. Instead of filling long forms, users can just type what they want (for example: *“Book a table for 4 tomorrow at 8pm”*) and the system handles the rest.

This project was built to explore how AI can be integrated into real-world applications like reservations and booking systems.

##  Live Demo

https://tablemate-ai.onrender.com

# Preview

![App Screenshot](restaurant ai ss1.PNG)


# What it can do

* Book tables using natural language input
* Handle reservations and store them in a database
* Show all bookings in an admin dashboard
* Cancel reservations from the admin panel
* Secure admin access with login authentication

# Tech Stack

* Backend: FastAPI
* AI Integration: LLM (Groq API)
* Database: SQLite
* Frontend: HTML, CSS, JavaScript
* Deployment: Render

# Security

The admin panel is protected using authentication, and sensitive data like API keys and credentials are stored using environment variables instead of being hardcoded.


# Running locally

Clone the repository:

```
git clone https://github.com/dishapatil1111/tablemate-ai.git
cd tablemate-ai
```

Install dependencies:

```
pip install -r requirements.txt
```

Create a `.env` file and add:

```
GROQ_API_KEY=your_api_key
ADMIN_USER=admin
ADMIN_PASS=admin123 
```

Run the app:

```
python app.py
```

# Future improvements

* Add user login system
* Improve mobile responsiveness
* Add conversation memory to AI
* Add analytics (bookings, peak hours, etc.)

---

## 👩‍💻 Author

Disha Patil

# 🎶 Sierra Leone Music API

A full-featured RESTful API for managing theatre-related entities like plays, actors, directors, showtimes, seats, tickets, prices, and user authentication, built with *FastAPI* and *SQLAlchemy*.

---

## 🚀 Features

- 🎭 Actor, Director & Play management
- 🕒 ShowTime & Seating arrangements
- 🎫 Ticket & Pricing system
- 🔐 User Authentication & Role-based Access (admin / customer)
- 📦 SQLite + SQLAlchemy ORM
- ✅ Clean JSON output with relational previews
- 📘 Interactive Swagger UI (/docs)

---

## 📁 Project Structure

app/ ├── main.py ├── models.py ├── schemas.py ├── database.py ├── routes/ │   ├── actorRoute.py │   ├── directorRoute.py │   ├── playRoute.py │   ├── customerRoute.py │   ├── showtimeRoute.py │   ├── seatRoute.py │   ├── ticketRoute.py │   ├── priceRoute.py │   └── auth.py ├── services/ │   └── [model_name]_service.py

---

## 🛠 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/sierra-leone-music-api.git
cd sierra-leone-music-api

2. Create Virtual Environment

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

3. Install Dependencies

pip install -r requirements.txt

4. Run the Application

uvicorn main:app --reload

Visit: http://127.0.0.1:8000/docs to use the Swagger UI.


---

🔑 Authentication & Authorization

Users must signup and login via /auth/signup and /auth/login

JWT token is returned and must be used as a Bearer token

Customers can only perform GET operations

Admins have full access



---

📌 Example JSON

Create Ticket

{
  "seat_id": 1,
  "show_time_id": 3,
  "customer_id": 2
}

Create Actor

{
  "name": "John Legend",
  "gender": "male",
  "date_of_birth": "1980-12-28"
}


---

🧪 Testing Endpoints

GET /plays/ – List all plays

GET /tickets/{id} – Detailed ticket info (seat, customer, time)

POST /auth/login – Login and get token

GET /me – Get current user info

GET /admin – Admin-only route



---

📌 Technologies Used

FastAPI

SQLAlchemy

SQLite

Pydantic

Python 3.10+

JWT / OAuth2



---

📋 End Note

This API was created as part of a group project for Object-Oriented Programming II at Limkokwing University. The focus was on real-world API design, data modeling, and secure role-based access control.

👩‍💻 Group Members

Adeola

Sarah Princess Okike

Valentine



---

Thank you for reviewing our work. We hope you enjoy using the Sierra Leone Music API! 🎧

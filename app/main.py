from fastapi import FastAPI
from app.bookings import app as booking_app
from app.users import app as users_app
from app.payments import app as payments_app

app = FastAPI()

app.mount("/api/users", users_app)
app.mount("/api/bookings", booking_app)
app.mount("/api/payments", payments_app)
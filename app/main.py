from fastapi import FastAPI
from bookings_service.bookings import app as booking_app
from users_service.users import app as users_app
from payments_service.payments import app as payments_app
from payments_service.models import Base
from database import engine, SessionLocal


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.mount("/api/users", users_app)
app.mount("/api/bookings", booking_app)
app.mount("/api/payments", payments_app)
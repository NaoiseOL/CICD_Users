from fastapi import APIRouter, HTTPException, status
from .schemas import Booking_Info

router = APIRouter()
bookings: list[Booking_Info] = []

@router.get("/")
def get_bookings():
    return bookings

@router.get("/{booking_id}")
def get_booking(booking_id: int):
    for b in bookings:
        if b.booking_id == booking_id:
            return b
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

@router.post("/", status_code=status.HTTP_201_CREATED)
def add_booking(booking: Booking_Info):
    if any(b.booking_id == booking.booking_id for b in bookings):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="booking_id already exists")
    bookings.append(booking)
    return booking

@router.put("/{booking_id}", status_code=status.HTTP_200_OK)
def update_booking(booking_id: int, new_booking: Booking_Info):
    for i, b in enumerate(bookings):
        if b.booking_id == booking_id:
            bookings[i] = new_booking
            return new_booking
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(booking_id: int):
    for i, b in enumerate(bookings):
        if b.booking_id == booking_id:
            bookings.pop(i)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
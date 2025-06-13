import enum
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship
from database import Base

class UserRole(enum.Enum):
    admin = "admin"
    customer = "customer"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(SqlEnum(UserRole), default=UserRole.customer)



class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gender = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)

    plays = relationship("Play", back_populates="actor")


class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date_of_birth = Column(Date, nullable=True)
    citizenship = Column(String, nullable=True)

    plays = relationship("Play", back_populates="director")


class Play(Base):
    __tablename__ = "plays"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    duration = Column(Integer)
    genre = Column(String)
    synopsis = Column(Text, nullable=True)
    actor_id = Column(Integer, ForeignKey("actors.id"))
    director_id = Column(Integer, ForeignKey("directors.id"))

    actor = relationship("Actor", back_populates="plays")
    director = relationship("Director", back_populates="plays")
    show_times = relationship("ShowTime", back_populates="play")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    telephone = Column(String, index=True)

    tickets = relationship("Ticket", back_populates="customer")


class ShowTime(Base):
    __tablename__ = "show_times"

    id = Column(Integer, primary_key=True, index=True)  # Added ID for primary key
    date_time = Column(DateTime, index=True)
    play_id = Column(Integer, ForeignKey("plays.id"))

    play = relationship("Play", back_populates="show_times")
    tickets = relationship("Ticket", back_populates="show_time")
    prices = relationship("Price", back_populates="show_time")


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    row_number = Column(Integer)
    seat_number = Column(Integer)

    tickets = relationship("Ticket", back_populates="seat")
    prices = relationship("Price", back_populates="seat")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    seat_id = Column(Integer, ForeignKey("seats.id"))
    show_time_id = Column(Integer, ForeignKey("show_times.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))

    seat = relationship("Seat", back_populates="tickets")
    show_time = relationship("ShowTime", back_populates="tickets")
    customer = relationship("Customer", back_populates="tickets")





class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    seat_id = Column(Integer, ForeignKey("seats.id"))
    show_time_id = Column(Integer, ForeignKey("show_times.id"))
    price = Column(Integer)

    seat = relationship("Seat", back_populates="prices")
    show_time = relationship("ShowTime", back_populates="prices")





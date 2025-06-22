from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    customer = "customer"

# PREVIEW SCHEMAS
class SeatPreview(BaseModel):
    id: int
    row_number: int
    seat_number: int

    class Config:
        orm_mode = True

class ShowTimePreview(BaseModel):
    id: int
    date_time: datetime
    class Config:
        orm_mode = True

class CustomerPreview(BaseModel):
    id: int
    name: str

    class Config:
        form_attribute = True

class PlayPreview(BaseModel):
    id: int
    title: str

    class Config:
        form_attribute = True

class ActorPreview(BaseModel):
    id: int
    name: str

    class Config:
        form_attribute = True

class DirectorPreview(BaseModel):
    id: int
    name: str

    class Config:
        form_attribute = True


# USER
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.customer

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    role: Optional[UserRole]
    password: Optional[str]

class UserOut(UserBase):
    id: int

    class Config:
        form_attribute = True

# ACTOR
class ActorBase(BaseModel):
    name: str
    gender: Optional[str]
    date_of_birth: Optional[date]

class ActorCreate(ActorBase):
    pass

class ActorUpdate(BaseModel):
    name: Optional[str]
    gender: Optional[str]
    date_of_birth: Optional[date]

class Actor(ActorBase):
    id: int

    class Config:
        form_attribute = True

# DIRECTOR

class DirectorBase(BaseModel):
    name: str
    date_of_birth: Optional[date]
    citizenship: Optional[str]

class DirectorCreate(DirectorBase):
    pass

class DirectorUpdate(BaseModel):
    name: Optional[str]
    date_of_birth: Optional[date]
    citizenship: Optional[str]

class Director(DirectorBase):
    id: int

    class Config:
        form_attribute = True

# PLAY

class PlayBase(BaseModel):
    title: str
    duration: int
    genre: str
    synopsis: Optional[str]
    actor_id: int
    director_id: int

class PlayCreate(PlayBase):
    pass

class PlayUpdate(BaseModel):
    title: Optional[str]
    duration: Optional[int]
    genre: Optional[str]
    synopsis: Optional[str]
    actor_id: Optional[int]
    director_id: Optional[int]

class Play(PlayBase):
    id: int

    class Config:
        form_attribute = True

# CUSTOMER

class CustomerBase(BaseModel):
    name: str
    telephone: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str]
    telephone: Optional[str]

class Customer(CustomerBase):
    id: int

    class Config:
        form_attribute = True

# SHOWTIME

class ShowTimeBase(BaseModel):
    date_time: datetime
    play_id: int

class ShowTimeCreate(ShowTimeBase):
    pass

class ShowTimeUpdate(BaseModel):
    date_time: Optional[datetime]
    play_id: Optional[int]

class ShowTime(ShowTimeBase):
    id: int

    class Config:
        form_attribute = True

# SEAT

class SeatBase(BaseModel):
    row_number: int
    seat_number: int

class SeatCreate(SeatBase):
    pass

class SeatUpdate(BaseModel):
    row_number: Optional[int]
    seat_number: Optional[int]

class Seat(SeatBase):
    id: int

    class Config:
        form_attribute = True
# TICKET

class TicketBase(BaseModel):
    seat_id: int
    show_time_id: int
    customer_id: int

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    seat_id: Optional[int]
    show_time_id: Optional[int]
    customer_id: Optional[int]

class Ticket(TicketBase):
    id: int

    class Config:
        form_attribute = True

# PRICE

class PriceBase(BaseModel):
    seat_id: int
    show_time_id: int
    price: int

class PriceCreate(PriceBase):
    pass

class PriceUpdate(BaseModel):
    seat_id: Optional[int]
    show_time_id: Optional[int]
    price: Optional[int]

class Price(PriceBase):
    id: int

    class Config:
        form_attribute = True

# RELATIONS

class PlayWithDetails(Play):
    actor: ActorPreview
    director: DirectorPreview

class ShowTimeWithPlay(ShowTime):
    play: PlayPreview
    tickets: List['Ticket']
    prices: List['Price']

class TicketWithDetails(Ticket):
    seat: SeatPreview
    show_time: ShowTimePreview
    customer: CustomerPreview

class SeatWithDetails(Seat):
    tickets: List[Ticket]
    prices: List[Price]

class PriceWithDetails(Price):
    seat: SeatPreview
    show_time: ShowTimePreview

class ActorWithPlays(Actor):
    plays: List[PlayPreview]

class DirectorWithPlays(Director):
    plays: List[PlayPreview]

class CustomerWithTickets(Customer):
    tickets: List[Ticket]

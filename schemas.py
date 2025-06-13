from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional,List
from datetime import date, datetime



class UserRole(str, Enum):
    admin = "admin"
    customer = "customer"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.customer


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True


class ActorBase(BaseModel):
    name: str
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None


class ActorCreate(ActorBase):
    pass


class ActorUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None



class Actor(ActorBase):
    id: int

    class Config:
        form_attributes = True



class DirectorBase(BaseModel):
    name: str
    date_of_birth: Optional[date] = None
    citizenship: Optional[str] = None



class DirectorCreate(DirectorBase):
    pass



class DirectorUpdate(BaseModel):
    name:  Optional[str] = None
    date_of_birth: Optional[date] = None
    citizenship: Optional[str] = None



class Director(DirectorBase):
    id: int

    class Config:
        form_attributes = True


class PlayBase(BaseModel):
    title: str
    duration: int
    genre: str
    synopsis: Optional[str] = None
    actor_id: int
    director_id: int


class PlayCreate(PlayBase):
    pass



class PlayUpdate(BaseModel):
    title: Optional[str] = None
    duration: Optional[int] = None
    genre: Optional[str] = None
    synopsis: Optional[str] = None
    actor_id: Optional[int] = None
    director_id: Optional[int] = None


class Play(PlayBase):
    id: int

    class Config:
        from_attributes = True



class CustomerBase(BaseModel):
    name: str
    telephone: str



class CustomerCreate(CustomerBase):
    pass



class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    telephone: Optional[str] = None


class Customer(CustomerBase):
    id: int

    class Config:
        from_attributes = True


class ShowTimeBase(BaseModel):
    date_time: datetime
    play_id: int



class ShowTimeCreate(ShowTimeBase):
    pass



class ShowTimeUpdate(BaseModel):
    date_time: datetime
    play_id: int

class ShowTime(ShowTimeBase):
    id: int

    class Config:
        from_attributes = True


class SeatBase(BaseModel):
    RowNo: int
    SeatNo: int

class SeatCreate(SeatBase):
    pass


class SeatUpdate(BaseModel):
    RowNo: Optional[int]
    SeatNo: Optional[int]

class Seat(SeatBase):
    id: int

    class Config:
        from_attributes = True



class TicketBase(BaseModel):
    TicketNo: str
    ShowTime_Play_PlayId: int  # Still keep for creation
    ShowTime_DateAndTime: datetime
    Customer_CustomerId: int
    Seat_RowNo: List[int]
    Seat_SeatNo: List[int]



class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    TicketNo: Optional[str]


class Ticket(TicketBase):
    id : int

    class Config:
        from_attributes = True


class PriceBase(BaseModel):
    seat_id: int
    show_time_id: int
    price: int

class PriceCreate(PriceBase):
    pass


class PriceUpdate(BaseModel):
    seat_id:  Optional[int] = None
    show_time_id:  Optional[int] = None
    price:  Optional[int] = None


class Price(PriceBase):
    id: int

    class Config:
        form_attributes = True


# Relationships
class ActorWithRelations(ActorBase):
    id: int
    plays: List[Play]

    class Config:
        from_attributes = True


class DirectorWithRelations(Director):
    plays: List[Play]


class PlayWithRelations(Play):
    actor: Actor
    director: Director
    show_times: List[ShowTime]


class CustomerWithRelations(Customer):
    tickets: List[Ticket]


class ShowTimeWithRelations(ShowTime):
    play: Play
    tickets: List[Ticket]
    prices: List[Price]


class PriceWithRelations(Price):
    seat: Seat
    show_time: ShowTime











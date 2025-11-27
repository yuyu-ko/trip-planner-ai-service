from pydantic import BaseModel
from typing import List, Optional

class TripRequest(BaseModel):
    city: str
    startDate: str
    endDate: str
    preferences: List[str]
    budgetLevel: str

class Activity(BaseModel):
    time: str
    title: str
    description: str
    location: str
    imageUrl: Optional[str] = None

class DayPlan(BaseModel):
    dayNumber: int
    date: str
    activities: List[Activity]

class ItineraryResponse(BaseModel):
    tripId: str | None = None
    days: List[DayPlan]

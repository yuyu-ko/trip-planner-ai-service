import os
import json
from openai import OpenAI
from schemas import TripRequest, ItineraryResponse, DayPlan, Activity
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================
#  Main AI Itinerary Generator
# ============================
async def generate_itinerary(trip: TripRequest) -> ItineraryResponse:

    prompt = f"""
    You are a travel planning AI. Generate a strict JSON itinerary.

    City: {trip.city}
    Start: {trip.startDate}
    End: {trip.endDate}
    Budget: {trip.budgetLevel}
    Preferences: {trip.preferences}

    Rules:
    - Use real Google Maps places.
    - Group nearby attractions on same day.
    - Minimize travel distance.
    - Each activity: include transportation details inside description (mode, minutes, cost).
    - Add "daySummary" (3-5 sentences).
    - First activity of Day 1 has no transportation info.
    - Include hotel/accommodation.
    - Plan activities until 8 PM each day.
    - Should recommend hotels to be the last activity of each day.

    Return ONLY valid JSON matching this:

    {{
      "days": [
         {{
           "dayNumber": 1,
           "date": "2025-01-01",
           "activities": [
                {{
                  "time": "09:00",
                  "title": "Breakfast at ...",
                  "description": "Main description. Transportation info included here.",
                  "location": "Exact Google Maps place"
                }}
           ]
         }}
      ]
    }}

    IMPORTANT:
    - No commentary
    - No markdown
    - Only valid JSON


    """

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    full_text = ""

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            full_text += delta

    # full_text 現在是完整 JSON 字串
    data = json.loads(full_text)
    return ItineraryResponse(**data)

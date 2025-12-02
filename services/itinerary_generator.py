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
    You are an expert travel planning AI. Generate a strict JSON itinerary.
    
    User Request:
    - City: {trip.city}
    - Start Date: {trip.startDate}
    - End Date: {trip.endDate}
    - Budget: {trip.budgetLevel}
    - Preferences: {trip.preferences}

    STRICT RULES:
    1. **NO DUPLICATES**: Do NOT repeat the same attraction, restaurant, or activity. Each activity must be unique across the entire trip.
       - *Exception*: You can return to the same Hotel/Accommodation at the end of every day (unless it's a multi-city trip).
    2. **High Quality**: Recommend ONLY places that are highly rated (4.0+ stars).
    3. **Real Names**: In the 'location' field, use the **specific Google Maps POI Name** (e.g., "Senso-ji", "Tokyo Tower"), NOT just the address.
    4. **Route Logic**: Group nearby attractions to minimize travel time.
    5. **Daily Schedule**: Plan from ~9 AM to ~9 PM.
    6. **Dates**: Calculate the specific date for each day starting from {trip.startDate}.

    Return ONLY valid JSON matching this structure:
    {{
      "days": [
         {{
           "dayNumber": 1,
           "date": "YYYY-MM-DD", 
           "activities": [
                {{
                  "time": "09:00",
                  "title": "Specific Place Name",
                  "description": "Description with transport info (e.g. 15 min taxi from last stop).",
                  "location": "Specific Place Name, City" 
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
        response_format={"type": "json_object"}, # 加上這行，保證 JSON 不會爛掉
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

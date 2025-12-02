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
    You are an expert travel planning AI. Your task is to generate a strict JSON itinerary based on the user's request.

    User Request:
    - City: {trip.city}
    - Start Date: {trip.startDate}
    - End Date: {trip.endDate}
    - Budget: {trip.budgetLevel}
    - Preferences: {trip.preferences}
    
    Rules:
    1. **High Quality Only**: Recommend ONLY places that are highly rated (4.0+ stars on Google Maps). Avoid obscure or low-rated locations.
    2. **Real Names**: In the 'location' field, provide the **specific Google Maps POI Name** (e.g., "Senso-ji", "Tokyo Tower"), NOT just the street address.
    3. **Route Logic**: Group nearby attractions to minimize travel time.
    4. **Accommodation**: The last activity of each day MUST be the hotel/accommodation.
    5. **Dates**: Calculate the specific date for each day starting from {trip.startDate}.

    Return ONLY valid JSON matching this:
    {{
      "days": [
         {{
           "dayNumber": 1,
           "date": "YYYY-MM-DD",
           "activities": [
                {{
                  "time": "09:00",
                  "title": "Exact Place Name", 
                  "description": "Activity description. (Transport: 10 mins taxi)",
                  "location": "Place Name, City"  <-- 重點：這裡要是「名稱+城市」，不要只寫地址
                }}
           ]
         }}
      ]
    }}

    IMPORTANT CONSTRAINTS:
    - Return ONLY valid JSON.
    - NO introductory text (like "Here is your itinerary...").
    - NO markdown formatting (like ```json ... ```).
    - Ensure the JSON can be parsed by Python's json.loads().
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

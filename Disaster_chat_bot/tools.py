from langchain_core.tools import tool
from rag.vectorstore import retriever
import requests
from typing import Optional

@tool
def get_weather(
    location: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None
):
    """
Get current weather information for a location.
"""

    if latitude is not None and longitude is not None:
        url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current="
        "temperature_2m,"
        "apparent_temperature,"
        "relative_humidity_2m,"
        "rain,"
        "precipitation,"
        "weather_code,"
        "cloud_cover,"
        "surface_pressure,"
        "wind_speed_10m,"
        "wind_direction_10m,"
        "wind_gusts_10m"
        "&timezone=auto"
        )

        response = requests.get(url)

        return response.json()["current"]

    elif location:
        url =(
            "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={location}&count=1"
        )
        
        response = requests.get(url)
        data = response.json()
        
        if "results" not in data:
            return "Location not found"
        
        place = data["results"][0]
        latitude = place["latitude"]
        longitude = place["longitude"]
        
        url = (
                "https://api.open-meteo.com/v1/forecast"
                f"?latitude={latitude}"
                f"&longitude={longitude}"
                "&current="
                "temperature_2m,"
                "apparent_temperature,"
                "relative_humidity_2m,"
                "rain,"
                "precipitation,"
                "weather_code,"
                "cloud_cover,"
                "surface_pressure,"
                "wind_speed_10m,"
                "wind_direction_10m,"
                "wind_gusts_10m"
                "&timezone=auto"
            )
        
        response = requests.get(url)
        
        return response.json()["current"]    

    
@tool
def retrieve_disaster_info(query: str):
    """
    Search the disaster knowledge base.
    Use this when the user asks about disaster
    safety, evacuation, flood procedures, etc.
    """
    docs = retriever.invoke(query)
    
    context = ""
    
    for doc in docs:
        context += doc.page_content
        context += "\n\n"
        
    return context

@tool
def query_disaster_reports(
    location: str | None = None,
    disaster_type: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None
):
    """
    Find recent, latest, last disaster reports based on location, disaster type,
    and date range.
    """
    return {
        "type":"Flood",
        "location" : "Kollam"
    }
    # cursor = connection.cursor(dictionary=True)

    # query = """
    #     SELECT
    #         image_id,
    #         user_id,
    #         image_path,
    #         disaster_type,
    #         latitude,
    #         longitude,
    #         created_at,
    #         description,
    #         status
    #     FROM disaster_uploads
    #     WHERE 1=1
    # """

    # params = []

    # if disaster_type:
    #     query += " AND disaster_type = %s"
    #     params.append(disaster_type)

    # if start_date:
    #     query += " AND created_at >= %s"
    #     params.append(start_date)

    # if end_date:
    #     query += " AND created_at < %s"
    #     params.append(end_date)

    # query += " ORDER BY created_at DESC LIMIT 20"

    # cursor.execute(query, params)

    # reports = cursor.fetchall()

    # cursor.close()
    # connection.close()

    # return reports
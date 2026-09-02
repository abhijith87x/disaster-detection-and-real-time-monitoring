import requests
from database import get_db

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("DisasterServer")


# =========================================================
# WEATHER TOOL
# =========================================================

@mcp.tool()
def get_weather(location: str):
    """
    Get current weather information for a location.
    """

    # Geocoding
    geo_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={location}&count=1"
    )

    response = requests.get(geo_url)
    response.raise_for_status()

    data = response.json()

    if "results" not in data:
        return {
            "error": "Location not found"
        }

    place = data["results"][0]

    latitude = place["latitude"]
    longitude = place["longitude"]

    # Weather
    weather_url = (
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

    response = requests.get(weather_url)
    response.raise_for_status()

    return response.json()["current"]


# =========================================================
# DISASTER REPORTS TOOL
# =========================================================

@mcp.tool()
def query_disaster_reports(
    location: str | None = None,
    disaster_type: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None
):
    print("reached")
    mydb = get_db()
    cursor = mydb.cursor(dictionary=True)
    
    """
    Query recent, latest disaster reports from MySQL Based on user query.
    """
    
    query = """
        SELECT *
        FROM disaster_uploads
        WHERE 1=1
    """

    params = []

    if location:
        query += " AND district = %s"
        params.append(location)

    if disaster_type:
        query += " AND disaster_type = %s"
        params.append(disaster_type)

    if start_date:
        query += " AND created_at >= %s"
        params.append(start_date)

    if end_date:
        query += " AND created_at <= %s"
        params.append(end_date)


    try:
        print("query, para", query,params)
        cursor.execute(query, params)

        results = cursor.fetchall()
        print(results)
        return results

    finally:
        cursor.close()
        mydb.close()


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":
    mcp.run()
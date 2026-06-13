import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone


load_dotenv()

API_KEY = os.getenv("LTA_API_KEY")

BASE_URL = "https://datamall2.mytransport.sg/ltaodataservice/v3/BusArrival"


def calculate_minutes(estimated_arrival):
    if not estimated_arrival:
        return "-"

    arrival_time = datetime.fromisoformat(estimated_arrival)
    now = datetime.now(timezone.utc).astimezone()

    difference = arrival_time - now
    minutes = round(difference.total_seconds() / 60)

    if minutes <= 0:
        return "Arriving"

    return f"{minutes} mins"


def get_bus_arrivals(bus_stop_code):
    if not API_KEY:
        return {"error": "LTA_API_KEY not found. Check your .env file."}

    headers = {
        "AccountKey": API_KEY,
        "accept": "application/json"
    }

    params = {
        "BusStopCode": bus_stop_code
    }

    try:
        response = requests.get(
            BASE_URL,
            headers=headers,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = []

        for service in data.get("Services", []):
            bus_no = service.get("ServiceNo")

            next_bus = service.get("NextBus", {})
            next_bus2 = service.get("NextBus2", {})
            next_bus3 = service.get("NextBus3", {})
            estimated_arrival = next_bus.get("EstimatedArrival")

            results.append({
                "bus_no": bus_no,

                "arrival1": calculate_minutes(
                    next_bus.get("EstimatedArrival")
                ),

                "arrival2": calculate_minutes(
                    next_bus2.get("EstimatedArrival")
                ),

                "arrival3": calculate_minutes(
                    next_bus3.get("EstimatedArrival")
                ),

                "load": next_bus.get("Load"),
                "feature": next_bus.get("Feature"),
                "type": next_bus.get("Type")
            })

        return results

    except requests.exceptions.RequestException as error:
        return {"error": str(error)}
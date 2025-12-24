from datetime import datetime
from flights import load_flights
from hotels import load_hotels

# Load flights and hotels

flights = load_flights()
hotels = load_hotels()

# Helpers

def parse_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format")


def calculate_days_and_nights(start_date: str, end_date: str):
    start = parse_date(start_date)
    end = parse_date(end_date)

    if start > end:
        raise ValueError("Starting date cannot be after end date.")

    days = (end - start).days + 1
    nights = days - 1

    return days, nights

# Budget Estimation Tool for only flights, only hotels and a full trip

def estimate_flight_budget(flight):
    """
    Used when user only books a flight
    """
    return {
        "flight_cost": flight["price"],
        "total_budget": flight["price"]
    }


def estimate_hotel_budget(hotel, days):
    """
    Used when user only books a hotel
    """
    nights = max(1, days - 1)
    hotel_cost = hotel["price_per_night"] * nights
    misc_cost = 1500 * days

    return {
        "hotel_cost": hotel_cost,
        "misc_cost": misc_cost,
        "total_budget": hotel_cost + misc_cost
    }


def estimate_full_trip_budget(flight, hotel, days):
    """
    Used ONLY for full trip
    """
    nights = max(1, days - 1)

    flight_cost = flight["price"]
    hotel_cost = hotel["price_per_night"] * nights
    misc_cost = 1500 * days

    return {
        "flight_cost": flight_cost,
        "hotel_cost": hotel_cost,
        "misc_cost": misc_cost,
        "total_budget": flight_cost + hotel_cost + misc_cost
    }
import json
import os
from datetime import datetime
from typing import List,Dict,Optional

# Path handling

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir,'data','flights.json')

# Core data loader

def load_flights() -> List[Dict]:
    """
    Load flight data from flights.json
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f'flights.json not found at {data_path}')
    
    with open(data_path,'r',encoding='utf-8')as file:
        return json.load(file)
    
# Flight search logic

def search_flights(source_city: str,
        destination_city: str,
        travel_date: Optional[str] = None,
        sort_by: str = 'price') -> List[Dict]:
    """
    Search flights by source and destination
    Parameters:
    - source_city (str)
    - destination_city (str)
    - travel_date (yyyy-mm-dd) [optional]
    - sort_by: 'price'
    Returns:
    - a list of matching flight dictionaries
    """
    # Load flight data

    flights = load_flights()

    # Filter by cities
      
    if not source_city or not destination_city:
        raise ValueError("source_city and destination_city are required")

    results = []
    for flight in flights:
        if (flight["from"].strip().lower() == source_city.strip().lower()
            and flight["to"].strip().lower() == destination_city.strip().lower()):
            results.append(flight)
    
    # Optional: filter by date

    if travel_date:
        results = [
            flight for flight in results
            if flight["departure_time"].startswith(travel_date)
        ]

    # Sort results

    if sort_by == "price":
        results.sort(key=lambda x: x["price"])

    elif sort_by == "duration":
        def duration(t):
            dep = datetime.fromisoformat(t["departure_time"])
            arr = datetime.fromisoformat(t["arrival_time"])
            return (arr - dep).total_seconds()
        results.sort(key=duration)
    
    else:
        raise ValueError(f"Invalid sort_by value: {sort_by}. Expected 'price' or 'duration'.")
    return results

# Helper (for UI use later)

def format_flight(flight: Dict) -> str:
    """
    Convert flight dictionary into readable string
    """
    return (
        f"{flight['airline']} | "
        f"{flight['from']} -> {flight['to']} | "
        f"₹{flight['price']} | "
        f"Dep: {flight['departure_time']} | "
        f"Arr: {flight['arrival_time']}"
    )

# Local test block

if __name__ == "__main__":
    test_results = search_flights(
        source_city="Hyderabad",
        destination_city="Delhi",
        sort_by="price"
    )

    print(f'Found {len(test_results)} flights')

    for flight in test_results:
        print(format_flight(flight))
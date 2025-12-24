import json
import os
from typing import List,Dict,Optional

# Path handling

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir,'data','places.json')

# Core data loader

def load_places() -> List[Dict]:
    """
    Load place data from places.json
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f'places.json not found at {data_path}')
    
    with open(data_path,'r',encoding='utf-8')as file:
        return json.load(file)
    
# Places search logic

def search_places(
        city: str,
        place_type: Optional[str] = None,
        name: Optional[str] = None,
        sort_by: str = "rating"
    ) -> List[Dict]:
    """
    Search places using parameters like:
    - city (str),
    - type (str) [optional],
    - name (str) [optional],
    - sort_by: rating
    Returns:
    - a list of matching places dictionaries
    """
    # Load places data

    places = load_places()

    # Normalise inputs

    city = city.strip().lower()
    name = name.strip().lower() if name else None
    place_type = place_type.strip().lower() if place_type else None

    # Filter places

    if not city:
        raise ValueError("city is required")

    results = []
    for place in places:

        if place['city'].strip().lower() != city:
            continue

        if name and name not in place['name'].strip().lower():
            continue

        if place_type and place['type'].strip().lower() != place_type:
            continue
        
        results.append(place)

    # Sorting logic

    if sort_by == 'rating':
        results.sort(key=lambda x:x['rating'],reverse=True)

    elif sort_by == 'name':
        results.sort(key=lambda x:x['name'])

    else:
        raise ValueError(f"invalid sort_by value: {sort_by}. Expected 'rating' or 'name'.")
    
    return results

# Helper (for UI use later)

def format_place(place: Dict) -> str:
    return (
        f"{place['name']} | "
        f"{place['city']} | "
        f"{place['type']} | "
        f"{place['rating']}★"
    )

# Local test block

if __name__ == "__main__":
    test_results=search_places(city= "Kolkata")
    print(f"Found {len(test_results)} places:\n")

    for place in test_results:
        print(format_place(place))
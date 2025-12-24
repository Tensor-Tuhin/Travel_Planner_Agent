import json
import os
from typing import List,Dict,Optional

# Path handling

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir,'data','hotels.json')

# Core data loader

def load_hotels() -> List[Dict]:
    """
    Load hotel data from hotels.json
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f'hotels.json not found at {data_path}')
    
    with open(data_path,'r',encoding='utf-8')as file:
        return json.load(file)
    
# Hotel search logic

def search_hotels(
        city: str,
        name: Optional[str] = None,
        star: Optional[int] = None,
        sort_by: str = 'price'
    ) -> List[Dict]:
    """
    Search hotels using parameters like:
    - city (str)
    - name (str) [optional]
    - star (int) [optional]
    - sort_by: 'price per night'
    Returns:
    - a list of matching hotel dictionaries
    """
    # Load hotel data

    hotels = load_hotels()

    # Normalise inputs

    city = city.strip().lower()
    name = name.strip().lower() if name else None

    # Filter hotels

    if not city:
        raise ValueError('city is required')

    results = []
    for hotel in hotels:
        
        if hotel['city'].strip().lower() != city:
            continue

        if name and name not in hotel['name'].strip().lower():
            continue

        if star is not None and hotel['stars'] != star:
            continue

        results.append(hotel)
    
    # Sorting logic

    if sort_by == 'price':
        results.sort(key=lambda x:x['price_per_night'])

    elif sort_by == 'stars':
        results.sort(key=lambda x:x['stars'],reverse=True)

    else:
        raise ValueError(f'invalid sort_by value {sort_by}. Expected "price_per_night" or "stars".')
    
    return results
    
# Helper (for UI use later)

def format_hotel(hotel: Dict) -> str:
    return (
        f"{hotel['name']} | "
        f"{hotel['city']} | "
        f"{hotel['stars']}★ | "
        f"₹{hotel['price_per_night']} | "
        f"Amenities: {', '.join(hotel['amenities'])}"
    )

# Local test block

if __name__ == "__main__":
    test_results=search_hotels(city= "Kolkata")
    print(f"Found {len(test_results)} hotels:\n")

    for hotel in test_results:
        print(format_hotel(hotel))
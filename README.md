# ✈️ Travel Planner Application (Python + Streamlit)

##  Project Overview

This project is a Travel Planner application developed using Python and Streamlit.  
It enables users to plan their travel by exploring flights, hotels, places to visit, itineraries, weather forecasts, and estimated budgets.

The application follows a modular design, where each feature/tool is implemented in a separate Python file. This makes the project easy to understand, maintain, and extend.


##  File-wise Explanation

### - app.py
This is the main application file built using Streamlit.

- Provides the complete user interface
- Handles user interaction through sidebar navigation
- Displays results such as flights, hotels, itineraries, weather, and budget
- Manages multi-step user flow using Streamlit session state


### - flights.py

- Loads flight data from flights.json
- Filters flights based on:
  - source city
  - destination city
  - optional travel date
- Supports alternate flight suggestions if no flights are found on a selected date
- Formats flight details for display in the UI


### - hotels.py

- Loads hotel data from hotels.json
- Filters hotels by city
- Allows users to select a hotel
- Formats hotel details such as price, rating, and amenities for display


### - places.py

- Loads places data from places.json
- Filters tourist places based on city
- Used for showing attractions and generating itineraries
- Supports splitting places across multiple days for itinerary planning


### - weather.py

- Uses the Open-Meteo API (no API key required)
- Fetches daily maximum temperature forecasts
- Weather data is shown only for relevant travel dates
- Includes fallback handling if weather data is unavailable


### - budget.py

- Calculates estimated costs based on user selections
- Uses separate functions for:
  - flight-only budget
  - hotel-only budget
  - full trip budget
- Budget includes:
  - flight cost
  - hotel cost (based on number of nights)
  - miscellaneous daily expenses


##  Dataset Files (JSON)

### - flights.json
Contains flight information such as:
- airline name
- source city
- destination city
- departure time
- arrival time
- ticket price


### - hotels.json
Contains hotel information such as:
- hotel name
- city
- star rating
- price per night
- available amenities


### - places.json
Contains tourist place information such as:
- place name
- city
- short description

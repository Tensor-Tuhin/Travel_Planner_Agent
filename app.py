import streamlit as st
from datetime import date, timedelta

# IMPORTING THE FUNCTIONS FROM THE TOOLS

from flights import search_flights, format_flight
from hotels import search_hotels, format_hotel
from places import search_places, format_place
from weather import get_weather_forecast
from budget import (
    estimate_flight_budget,
    estimate_hotel_budget,
    estimate_full_trip_budget
)

# SESSION STATE
defaults = {
    "page": "Plan a Full Trip",
    "flights": None,
    "selected_flight": None,
    "hotels": None,
    "selected_hotel": None,
    "days": None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# SIDEBAR
st.sidebar.title("Travel ✈️🏨Planner 🏖️🌤️")
st.sidebar.subheader("A Rule-based Agent that helps to plan your next trip, find flights, hotels and suggests places to visit")
st.session_state.page = st.sidebar.radio(
    "Choose an option",
    [
        "Plan a Full Trip",
        "Only Flights",
        "Staycation and Hotels",
        "Explore Places in a City"
    ]
)

# PLAN A FULL TRIP

if st.session_state.page == "Plan a Full Trip":

    st.title("Plan Your Trip - Flights✈️, Hotels🛏️ and Itinerary📅")

    source = st.text_input("Where are you travelling from?").strip().lower()
    destination = st.text_input("Where are you travelling to?").strip().lower()
    travel_date = st.text_input("Travel date (YYYY-MM-DD) — optional").strip()

    if st.button("Search Flights"):
        flights = search_flights(
            source_city=source,
            destination_city=destination,
            travel_date=travel_date if travel_date else None
        )

        if not flights and travel_date:
            alt = search_flights(source, destination, None)
            if not alt:
                st.error("No flights available for this route. We are sorry for the inconvenience.")
                st.session_state.flights = None
            else:
                st.warning("No flights on selected date. Showing alternate dates.")
                st.session_state.flights = alt
        else:
            if not flights:
                st.error("No flights available for this route. We are sorry for the inconvenience.")
                st.session_state.flights = None
            else:
                st.session_state.flights = flights

        st.session_state.selected_flight = None
        st.session_state.selected_hotel = None

    if st.session_state.flights:
        st.subheader("Available Flights🛫")
        for i, f in enumerate(st.session_state.flights):
            st.write(f"{i+1}. {format_flight(f)}")

        f_choice = st.number_input(
            "Choose a flight from the above options",
            min_value=1,
            max_value=len(st.session_state.flights),
            step=1
        )

        if st.button("Confirm Flight"):
            st.session_state.selected_flight = st.session_state.flights[f_choice - 1]

    if st.session_state.selected_flight:
        st.subheader("Available Hotels🏨")
        st.session_state.hotels = search_hotels(destination)

        for i, h in enumerate(st.session_state.hotels):
            st.write(f"{i+1}. {format_hotel(h)}")

        h_choice = st.number_input(
            "Choose a hotel from the above options",
            min_value=1,
            max_value=len(st.session_state.hotels),
            step=1
        )

        if st.button("Confirm Hotel"):
            st.session_state.selected_hotel = st.session_state.hotels[h_choice - 1]

    if st.session_state.selected_hotel:
        days = st.number_input("How many days should I create an itinerary for?", min_value=1, step=1)

        if st.button("Generate Trip Plan"):
            places = search_places(destination)

            st.subheader("Your Itinerary📅")
            per_day = max(1, len(places) // days)
            if days <= 5:
                for d in range(days):
                    st.write(f"*Day {d+1}*")
                    for p in places[d*per_day:(d+1)*per_day]:
                        st.write(f"- {p['name']}")
            if days > 5:
                st.write("Currently unable to provide itinerary for more than 5 days")            
                st.write("So here is an itinerary for the first 5 days of your trip. Sorry for the inconvenience:")
                for d in range(5):
                    st.write(f"*Day {d+1}*")
                    for p in places[d*per_day:(d+1)*per_day]:
                        st.write(f"- {p['name']}")

            flight_date = date.fromisoformat(
                st.session_state.selected_flight["departure_time"][:10]
            )

            st.subheader("Weather Forecast⛅")
            forecast = get_weather_forecast(
                destination,
                flight_date,
                flight_date + timedelta(days=days)
            )

            if forecast:
                for day in forecast:
                    st.write(f"{day['date']} → {day['max_temp']}°C")
            else:
                st.warning("Weather data not available.")

            st.subheader("Estimated Budget💸")
            budget = estimate_full_trip_budget(
                st.session_state.selected_flight,
                st.session_state.selected_hotel,
                days
            )

            for k, v in budget.items():
                st.write(f"*{k.replace('_',' ').title()}*: ₹{v}")

# FLIGHT FINDER

elif st.session_state.page == "Only Flights":

    st.title("Flight Finder✈️")

    source = st.text_input("From").strip().lower()
    destination = st.text_input("To").strip().lower()
    travel_date = st.text_input("Travel date (YYYY-MM-DD) — optional").strip()

    if st.button("Search Flights"):
        flights = search_flights(source, destination, travel_date if travel_date else None)

        if not flights and travel_date:
            alt = search_flights(source, destination, None)
            if not alt:
                st.error("No flights available for this route. We are sorry for the inconvenience.")
                st.session_state.flights = None
            else:
                st.warning("No flights on selected date. Showing alternate dates.")
                st.session_state.flights = alt
        else:
            if not flights:
                st.error("No flights available for this route. We are sorry for the inconvenience.")
                st.session_state.flights = None
            else:
                st.session_state.flights = flights

    if st.session_state.flights:
        st.subheader("Available Flights🛫")
        for i, f in enumerate(st.session_state.flights):
            st.write(f"{i+1}. {format_flight(f)}")

        choice = st.number_input(
            "Choose a flight from the above options",
            min_value=1,
            max_value=len(st.session_state.flights),
            step=1
        )

        if st.button("Confirm Flight"):
            budget = estimate_flight_budget(st.session_state.flights[choice - 1])
            st.subheader("Estimated Budget💸")
            for k, v in budget.items():
                st.write(f"*{k.replace('_',' ').title()}*: ₹{v}")

# FIND HOTELS

elif st.session_state.page == "Staycation and Hotels":

    st.title("Plan Your Stay🏨")

    city = st.text_input("For which city should I search available hotels/resorts in?").strip().lower()

    if st.button("Search Hotels"):
        st.session_state.hotels = search_hotels(city)
        st.session_state.selected_hotel = None

    if not st.session_state.hotels:
            st.error("No hotels available for this city. We are sorry for the inconvenience.")
            st.session_state.hotels = None    

    if st.session_state.hotels:
        st.subheader("Available Hotels🏠")
        for i, h in enumerate(st.session_state.hotels):
            st.write(f"{i+1}. {format_hotel(h)}")

        h_choice = st.number_input(
            "Choose a hotel from the above options",
            min_value=1,
            max_value=len(st.session_state.hotels),
            step=1
        )

        if st.button("Confirm Hotel"):
            st.session_state.selected_hotel = st.session_state.hotels[h_choice - 1]

    if st.session_state.selected_hotel:
        days = st.number_input("How many days will you stay?", min_value=1, step=1)

        want_itinerary = st.radio(
            "Do you want an itinerary?⛱️",
            ["No", "Yes"],
            index=None
        )

        if want_itinerary == "Yes":
            places = search_places(city)
            st.subheader("Your Itinerary📅")
            per_day = max(1, len(places) // days)
            if days <= 5:
                for d in range(days):
                    st.write(f"*Day {d+1}*")
                    for p in places[d*per_day:(d+1)*per_day]:
                        st.write(f"- {p['name']}")
            if days > 5:
                st.write("Currently unable to provide itinerary for more than 5 days")            
                st.write("So here is an itinerary for the first 5 days of your trip. Sorry for the inconvenience:")
                for d in range(5):
                    st.write(f"*Day {d+1}*")
                    for p in places[d*per_day:(d+1)*per_day]:
                        st.write(f"- {p['name']}")

        st.subheader("Estimated Budget💸")
        budget = estimate_hotel_budget(st.session_state.selected_hotel, days)
        for k, v in budget.items():
            st.write(f"*{k.replace('_',' ').title()}*: ₹{v}")

# FIND PLACES

elif st.session_state.page == "Explore Places in a City":

    st.title("Explore Places to Visit⛱️")

    city = st.text_input("Which city are you interested in?").strip().lower()

    if st.button("Show Places"):
        st.session_state.places = search_places(city)

    if not st.session_state.places:
        st.error("Currently not showing tourist attraction spots for this city. We are sorry for the inconvenience.")
        st.session_state.places = None

    if "places" in st.session_state and st.session_state.places:
        st.subheader("Places to Visit🖼️")
        for p in st.session_state.places:
            st.write(format_place(p))

        want_itinerary = st.radio(
            "Do you want an itinerary?",
            ["No", "Yes"],
            index=None
        )

        if want_itinerary == "Yes":
            days = st.number_input("How many days should I create the itinerary for?", min_value=1, step=1)
            per_day = max(1, len(st.session_state.places) // days)
            st.subheader("Your Itinerary📅")
            if days <= 5:
                for d in range(days):
                    st.write(f"*Day {d+1}*")
                    for p in st.session_state.places[d*per_day:(d+1)*per_day]:
                        st.write(f"- {p['name']}")
            if days > 5:
                st.write("Currently unable to provide itinerary for more than 5 days")            
                st.write("So here is an itinerary for the first 5 days of your trip. Sorry for the inconvenience:")
                for d in range(5):
                    st.write(f"*Day {d+1}*")
                    for p in st.session_state.places[d*per_day:(d+1)*per_day]:
                        st.write(f"- {p['name']}")
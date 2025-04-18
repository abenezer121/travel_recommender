# Travel Assistant - Country Recommendations and Visa Information

This project provides a recommendation system to help users choose countries based on their safety preferences, visa requirements, flight information, weather conditions, and more. It uses data from external APIs and CSV files to generate recommendations tailored to the user's preferences.



## Overview

This project provides a comprehensive travel assistant that takes into account:
- Safety preferences (based on the Global Peace Index).
- Visa requirements (checking if the user can travel to a destination without a visa).
- Flight cost estimation (getting flight details between two locations).
- Weather conditions (checking if the destination's weather fits the user's preference).
- Country descriptions (fetching Wikipedia summaries for destinations).

The system uses several external APIs and CSV data files to gather the necessary information.

---

## Features

- **Safety-based recommendations**: Filters countries by their safety index (Global Peace Index).
- **Visa-free travel**: Allows the user to select countries based on whether they are visa-free for the user’s origin country.
- **Flight cost estimation**: Estimates the cost of a flight between the origin and destination, including flight details (airline, flight number, etc.).
- **Weather check**: Retrieves the current weather for the destination country and checks if it meets the user's preference (warm, mild, or cold).
- **Country descriptions**: Fetches a brief Wikipedia summary of the country or city to provide more context.

---
## how to run 

- interests=cultural,nature safety_preference=safe preferred_weather=warm visa_free_only=True origin=Ethiopia python3 run.py

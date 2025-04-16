from safety import get_countries_by_safety
from visa import get_visa_requirements
from utils.api_clients import ApiClient

user_preferences = {
    "safety_preference": "safe",  
    "budget_level": "low",        
    "preferred_weather": "warm",  
    "interests": ["culture", "nature"],
    "visa_free_only": True,
    "origin": "Ethiopia"
}

weather_api_key = "2e17671e38744e91496556f4b6648c20"
flight_api_key = "d52fcb0beba249cdddc32165ed343498"
api_client = ApiClient(weather_api_key, flight_api_key)

safety_recommended_countries = get_countries_by_safety(user_preferences["safety_preference"])

visa_choiced = get_visa_requirements(user_preferences["origin"], safety_recommended_countries, user_preferences["visa_free_only"])

for visa in visa_choiced[:3]:
    flight_info = api_client.get_flight_cost(user_preferences["origin"], visa["country"].lower())
    visa['flight_info'] = flight_info
    temperature = api_client.get_weather_by_country(visa["country"])
    visa['is_warm'] = temperature >= 20
    visa["country_description"] = api_client.get_city_description(visa["country"])

for visa in visa_choiced[:3]:
    print(visa)






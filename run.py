
from safety import get_countries_by_safety
from visa import get_visa_requirements
from utils.api_clients import ApiClient
from utils.recommender import TravelRecommender
user_preferences = {
    "safety_preference": "safe",  # safe | moderate | risky
    "preferred_weather": "warm",  # warm | cold
    "interests": ["culture", "nature"], # cultural | natural | mixed
    "visa_free_only": False, # True | False
    "origin": "Ethiopia" # origin country to start
}

weather_api_key = "2e17671e38744e91496556f4b6648c20"
flight_api_key = "d52fcb0beba249cdddc32165ed343498"
api_client = ApiClient(weather_api_key, flight_api_key)

recommender = TravelRecommender(weather_api_key, flight_api_key)
recommendations = recommender.get_recommendations(user_preferences)
    
  
for i, rec in enumerate(recommendations, 1):
        print(f"\nRecommendation #{i}: {rec['country']}")
        print(f"  Safety Score: {rec['safety_score']} (Trend: {'↑' if rec['safety_trend'] > 0 else '↓'})")
        print(f"  Current Temperature: {rec['temperature']}°C")
        print(f"  Flight Price: ${rec['flight_info']['price']:.2f}")
        print(f"  Match Score: {rec['match_score']}/100")
        print(f"\n  Description: {rec['description'][:200]}...")
        print(f"\n  Recommended heritage site: {rec['recommended_heritage_site']}...")
        print(f"\n  All Heritage Site: {rec['overall_heritage_sites']}...")

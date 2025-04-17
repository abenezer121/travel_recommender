
import os
from safety import get_countries_by_safety
from visa import get_visa_requirements
from utils.api_clients import ApiClient
from utils.recommender import TravelRecommender

interests_str = os.getenv('interests', 'culture,nature')  # default if not set
interests = [interest.strip() for interest in interests_str.split(',')]
user_preferences = {
    "safety_preference": os.getenv('safety_preference', 'moderate'),  # safe | moderate | risky
    "preferred_weather": os.getenv('preferred_weather', 'warm') ,  # warm | cold
    "interests": interests, # cultural | natural | mixed
    "visa_free_only": os.getenv('visa_free_only', 'False').lower() == 'true', # True | False
    "origin": os.getenv('origin', 'USA') # origin country to start use USA for united states of america
}

print(user_preferences)

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

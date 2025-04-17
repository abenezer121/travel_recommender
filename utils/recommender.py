from safety import get_countries_by_safety
from utils.api_clients import ApiClient
from visa import get_visa_requirements


class TravelRecommender:
    def __init__(self, weather_api_key, flight_api_key):
        self.api_client = ApiClient(weather_api_key, flight_api_key)
    
    def get_recommendations(self, user_preferences):
       
        #  Get safe countries based on user preference
        safety_countries = get_countries_by_safety(user_preferences["safety_preference"])
        
        # Filter by visa requirements
        visa_countries = get_visa_requirements(
            user_preferences["origin"],
            safety_countries[:10],
            user_preferences.get("visa_free_only", True)
        )
        
       
        recommendations = []
        for country in visa_countries[:6]:  
            try:
               
                temperature = self.api_client.get_weather_by_country(country["country"])
                
               
                if user_preferences["preferred_weather"] == "warm" and temperature < 20:
                    continue
                if user_preferences["preferred_weather"] == "cool" and temperature >= 20:
                    continue
                
              
                flight_info = self.api_client.get_flight_cost(
                    user_preferences["origin"],
                    country["country"]
                )
                
               
                description = self.api_client.get_city_description(country["country"])
                
              
                unesco_data = ApiClient.scrape_unesco_list()
              
                heritage_sites = []
                for entry in unesco_data:
                  
                    if entry["country"].lower() == country["country"].lower():
                        heritage_sites = entry["heritage_sites"]
                        break
            
                filtered_sites = []
                if "interests" in user_preferences:
                    for site in heritage_sites:
                        site_category = site["category"].lower()
                        if ("culture" in user_preferences["interests"] and 
                            ("cultural" in site_category or "mixed" in site_category)):
                            filtered_sites.append(site)
                        elif ("nature" in user_preferences["interests"] and 
                              ("natural" in site_category or "mixed" in site_category)):
                            filtered_sites.append(site)
                
                
                recommendation = {
                    "country": country["country"],
                    "country_code": country["code"],
                    "safety_score": country["avg_gpi"],
                    "safety_trend": country["trend"],
                    "temperature": temperature,
                    "flight_info": flight_info,
                    "description": description,
                    "recommended_heritage_site": filtered_sites[:3], 
                    "overall_heritage_sites" : heritage_sites,
                    "match_score": self._calculate_match_score(
                        country, 
                        temperature, 
                        flight_info, 
                        len(filtered_sites),
                        user_preferences
                    )
                }
                
                recommendations.append(recommendation)
            except Exception as e:
                print(f"Error processing {country['country']}: {str(e)}")
                continue
        
    
        return sorted(recommendations, key=lambda x: x["match_score"], reverse=True)[:3]
    
    def _calculate_match_score(self, country, temperature, flight_info, heritage_count, preferences):
       
        score = 0
        
      
        safety_score = (3 - country["avg_gpi"]) * 20  
        score += safety_score
        
      
        if preferences["preferred_weather"] == "warm" and temperature >= 20:
            score += 20
        elif preferences["preferred_weather"] == "cool" and temperature < 20:
            score += 20
        else:
            score += 10  
            
        
        max_flight_price = 2000  
        flight_price_score = (1 - (flight_info["price"] / max_flight_price)) * 20
        score += flight_price_score
        
      
        heritage_score = min(heritage_count, 3) * 5 
        score += heritage_score
        
        
        score += 5
        
        return min(100, max(0, round(score)))
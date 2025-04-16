import requests


class ApiClient:
    def __init__(self, weather_api_key, flight_api_key):
        self.weather_api_key = weather_api_key
        self.flight_api_key = flight_api_key

    def get_weather_by_country(self, country_name):
        url = f"http://api.weatherstack.com/current"
        params = {'access_key': self.weather_api_key, 'query': country_name}
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                temperature = data['current']['temperature']
                return temperature
            else:
                return 25
        except Exception as e:
            print(f"Error occurred: {e}")
            return 25

    def get_flight_cost(self, origin, destination, default_price=1000):
        def get_country_qid(country_name_or_code):
            try:
                url = "https://www.wikidata.org/w/api.php"
                params = {
                    "action": "wbsearchentities",
                    "language": "en",
                    "format": "json",
                    "search": country_name_or_code,
                    "type": "item"
                }
                response = requests.get(url, params=params, timeout=10).json()
                return response.get("search", [{}])[0].get("id")
            except Exception as e:
                print(f"Error fetching country QID: {e}")
                return None

        def get_airports_from_wikidata(country_name_or_code):
            try:
                country_qid = get_country_qid(country_name_or_code)
                if not country_qid:
                    return {"error": "Country not found in Wikidata"}

                query = f"""
                SELECT ?airport ?iata ?label WHERE {{
                ?airport wdt:P31 wd:Q1248784;
                         wdt:P17 wd:{country_qid};
                         wdt:P238 ?iata;
                         rdfs:label ?label.
                FILTER(LANG(?label) = "en")
                }}
                """
                url = "https://query.wikidata.org/sparql"
                headers = {"Accept": "application/json"}
                response = requests.get(url, params={"query": query}, headers=headers, timeout=10)
                return response.json()
            except Exception as e:
                print(f"Error fetching airports: {e}")
                return {"error": str(e)}

        origin_airports = get_airports_from_wikidata(origin)
        dest_airports = get_airports_from_wikidata(destination)

        if "error" in origin_airports or "error" in dest_airports:
            error_msg = origin_airports.get("error") or dest_airports.get("error")
            return {
                "success": False,
                "price": default_price * 1.5,
                "details": f"Error: {error_msg}"
            }

        if not origin_airports.get("results", {}).get("bindings") or not dest_airports.get("results", {}).get("bindings"):
            return {
                "success": False,
                "price": default_price * 1.3,
                "details": "No airports found for one or both countries"
            }

        origin_iata = origin_airports["results"]["bindings"][0]["iata"]["value"]
        dest_iata = dest_airports["results"]["bindings"][0]["iata"]["value"]

        try:
            url = f'https://api.aviationstack.com/v1/routes?access_key={self.flight_api_key}&dep_iata={origin_iata}&arr_iata={dest_iata}'
            response = requests.get(url, timeout=10)
            data = response.json()

            if 'data' in data and data['data']:
                flights = []
                for route in data['data']:
                    flights.append({
                        "airline": route['airline']['name'],
                        "flight_number": route['flight']['number'],
                        "departure": route['departure']['airport'],
                        "arrival": route['arrival']['airport']
                    })
                price = default_price * 0.9
                return {
                    "success": True,
                    "price": price,
                    "details": flights
                }
            else:
                return {
                    "success": False,
                    "price": default_price * 1.2,
                    "details": "No direct flights found"
                }
        except Exception as e:
            return {
                "success": False,
                "price": default_price * 1.5,
                "details": f"API Error: {str(e)}"
            }

    def get_city_description(self, city_name):
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{city_name}"
        response = requests.get(url)
        return response.json().get("extract", "No description available.")

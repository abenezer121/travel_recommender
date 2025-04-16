import pandas as pd

def get_visa_requirements(origin_country, safety_recommended_countries, visa_free_only=True):
    
    df = pd.read_csv("data/passport-power.csv")
    
    country_map = {}
    for index, row in df.iterrows():
        origin = row['origin'].lower()  
        destination = row['destination'].lower()  
        visa_requirement = row['requirement']  
        
        if origin not in country_map:
            country_map[origin] = []
        
        country_map[origin].append({
            'destination': destination,
            'visa_requirement': visa_requirement
        })

    lowered_origin = origin_country.lower()  
    
    visa_choiced = []
    if lowered_origin in country_map:
        for country in safety_recommended_countries:
            data = country_map[lowered_origin]
            for country_data in data:
                if country["country"].lower() == country_data["destination"].lower():
                    if visa_free_only and country_data["visa_requirement"] == "visa_free":
                        visa_choiced.append(country)
                        break
                    elif not visa_free_only:
                        visa_choiced.append(country)
                        break
    return visa_choiced

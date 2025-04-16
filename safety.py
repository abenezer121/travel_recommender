import pandas as pd

def get_countries_by_safety(user_safety_preference, trend_weight=0.5):
   
    df = pd.read_csv("data/gpi.csv")
    
   
    year_columns = [col for col in df.columns if col.isdigit()]
    df["avg_gpi"] = df[year_columns].mean(axis=1)
    df["trend"] = df[year_columns[-1]] - df[year_columns[0]]
    df["trend_score"] = -df["trend"]
    
    
    df["final_score"] = (1 - trend_weight) * (1 / df["avg_gpi"]) + trend_weight * df["trend_score"]

    if user_safety_preference == "safe":
        df_filtered = df[df["avg_gpi"] <= 1.6]
    elif user_safety_preference == "moderate":
        df_filtered = df[(df["avg_gpi"] > 1.6) & (df["avg_gpi"] <= 2.3)]
    elif user_safety_preference == "risky":
        df_filtered = df[df["avg_gpi"] > 2.3]
    else:
        raise ValueError("Invalid safety preference: choose 'safe', 'moderate', or 'risky'")

    top_countries = df_filtered.sort_values(by="final_score", ascending=False).head(25)

    return [
        {
            "country": row["Country"],
            "code": row["iso3c"],
            "avg_gpi": round(row["avg_gpi"], 3),
            "trend": round(row["trend"], 3)
        }
        for _, row in top_countries.iterrows()
    ]

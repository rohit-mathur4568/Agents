def get_travel_insights(df):
    most_popular = df["Destination"].value_counts().idxmax()
    avg_cost = round(df["Total Cost"].mean(), 2)
    most_transport = df["Transportation type"].value_counts().idxmax()
    most_accommodation = df["Accommodation type"].value_counts().idxmax()

    male_count = df[df["Traveler gender"].str.lower() == "male"].shape[0]
    female_count = df[df["Traveler gender"].str.lower() == "female"].shape[0]

    top_country = df["Traveler nationality"].value_counts().idxmax()
    top_vehicle = df["Transportation type"].value_counts().idxmax()

    return {
        "popular_destination": most_popular,
        "average_cost": avg_cost,
        "transport": most_transport,
        "accommodation": most_accommodation,
        "male_count": male_count,
        "female_count": female_count,
        "top_country": top_country,
        "top_vehicle": top_vehicle
    }


def recommend_destination(df, budget):
    filtered = df[df["Total Cost"] <= budget]

    if len(filtered) == 0:
        return "No destination found in this budget."

    return filtered["Destination"].value_counts().idxmax()


def chat_with_agent(df, user_query):
    query = user_query.lower()

    if "male" in query:
        male_count = df[df["Traveler gender"].str.lower() == "male"].shape[0]
        return f"Total male travelers are {male_count}"

    elif "female" in query:
        female_count = df[df["Traveler gender"].str.lower() == "female"].shape[0]
        return f"Total female travelers are {female_count}"

    elif "country" in query or "nationality" in query:
        country_counts = df["Traveler nationality"].value_counts().head(5)
        return "Top countries/nationalities:\n" + country_counts.to_string()

    elif "vehicle" in query or "transport" in query:
        vehicle_counts = df["Transportation type"].value_counts().head(5)
        return "Top vehicles/transport types:\n" + vehicle_counts.to_string()

    elif "popular" in query:
        return f"The most popular destination is {df['Destination'].value_counts().idxmax()}"

    elif "average cost" in query or "cost" in query:
        return f"The average trip cost is {round(df['Total Cost'].mean(), 2)}"

    elif "hotel" in query or "accommodation" in query:
        return f"The most preferred accommodation is {df['Accommodation type'].value_counts().idxmax()}"

    else:
        return "Sorry, I can answer questions about male/female count, country, vehicle, popular destination, cost, and accommodation."
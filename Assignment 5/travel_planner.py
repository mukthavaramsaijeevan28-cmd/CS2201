TOURIST_PLACES_KB = {
    "Paris": {"tags": ["tourist places"], "base_cost": 200},
    "Tuscany": {"tags": ["wine"], "base_cost": 150},
    "Tokyo": {"tags": ["food"], "base_cost": 250},
}

WINE_ONTOLOGY_KB = {
    "Tuscany": {"famous_for": "Chianti Classico", "type": "Red Wine"},
    "Paris": {"famous_for": "Bordeaux", "type": "Luxury Blend"},
    "Tokyo": {"famous_for": "Sake", "type": "Rice Wine"}
}

FOOD_RECOMMENDATION_KB = {
    "Paris": "Croissants & Escargot",
    "Tuscany": "Handmade Pasta & Truffles",
    "Tokyo": "Sushi & Ramen"
}

class AITravelPlanner:
    def __init__(self, tourist_kb, wine_kb, food_kb):
        self.tourist_kb = tourist_kb
        self.wine_kb = wine_kb
        self.food_kb = food_kb

    def suggest_trip(self, user_preference, max_budget):
        itineraries = []
        
        for destination, info in self.tourist_kb.items():

            if user_preference in info["tags"] and info["base_cost"] <= max_budget:
                wine_profile = self.wine_kb.get(destination, {})
                food_profile = self.food_kb.get(destination, "Local Cuisine")
                
                plan = {
                    "Destination": destination,
                    "Estimated Base Cost": f"${info['base_cost']}",
                    "Local Delicacy": food_profile,
                    "Wine/Drink Pairing": f"{wine_profile.get('famous_for', 'N/A')} ({wine_profile.get('type', 'N/A')})"
                }
                itineraries.append(plan)
                
        return itineraries

print("INTERACTIVE AI TRAVEL PLANNER")
print("Available preferences: wine, food, tourist places\n")


while True:
    user_vibe = input("What is your main preference? (wine / food / tourist places): ").strip().lower()
    if user_vibe in ["wine", "food", "tourist places"]:
        break
    print("Invalid preference! Please choose exactly from: wine, food, or tourist places.")


while True:
    try:
        user_budget = float(input("What is your maximum base budget in USD? (e.g., 200): "))
        if user_budget <= 0:
            print("Budget must be a positive number greater than 0. Please try again.")
            continue
        break  
    except ValueError:
        print("Invalid input! Please enter a valid number for the budget.")


planner = AITravelPlanner(TOURIST_PLACES_KB, WINE_ONTOLOGY_KB, FOOD_RECOMMENDATION_KB)
recommendations = planner.suggest_trip(user_vibe, user_budget)


print("\nYOUR PERSONALIZED TRAVEL RECOMMENDATION")
if recommendations:
    for rec in recommendations:
        print(f"\nDestination Match: {rec['Destination']}")
        print(f"Cost: {rec['Estimated Base Cost']}")
        print(f"Food to try: {rec['Local Delicacy']}")
        print(f"Recommended Drink: {rec['Wine/Drink Pairing']}")
else:
    print("Sorry! No destinations in our knowledge base match both your preference and budget constraints.")
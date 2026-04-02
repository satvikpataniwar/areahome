import json
import random

areas = [
    "Gachibowli", "Kondapur", "Madhapur", "Hitech City", 
    "Kukatpally", "Banjara Hills", "Jubilee Hills", "Miyapur", "Manikonda", "Nallagandla",
    "ECIL", "Secunderabad", "Begumpet", "Ameerpet", "SR Nagar", "Dilsukhnagar", 
    "LB Nagar", "Uppal", "Boduppal", "Hayathnagar", "Vanasthalipuram", "Saroornagar",
    "Mehdipatnam", "Tolichowki", "Attapur", "Rajendra Nagar", "Shamshabad",
    "Nanakramguda", "Kokapet", "Narsingi", "Gandipet", "Patancheru", "Kompally",
    "Alwal", "Malkajgiri", "Nacharam", "Kothapet", "Chanda Nagar", "Bachupally",
    "Nizampet", "Pragathi Nagar", "Film Nagar", "Panjagutta", "Khairatabad",
    "Masab Tank", "Nampally", "Abids", "Himayatnagar", "Narayanguda", "Tarnaka"
]

coordinates = {
    "Gachibowli": [17.4401, 78.3489], "Kondapur": [17.4622, 78.3568], "Madhapur": [17.4483, 78.3915], 
    "Hitech City": [17.4435, 78.3772], "Kukatpally": [17.4849, 78.4069], "Banjara Hills": [17.4156, 78.4398], 
    "Jubilee Hills": [17.4313, 78.4071], "Miyapur": [17.4968, 78.3614], "Manikonda": [17.3995, 78.3854], 
    "Nallagandla": [17.4645, 78.3188], "ECIL": [17.4728, 78.5630], "Secunderabad": [17.4399, 78.4983], 
    "Begumpet": [17.4447, 78.4664], "Ameerpet": [17.4375, 78.4483], "SR Nagar": [17.4431, 78.4440], 
    "Dilsukhnagar": [17.3688, 78.5247], "LB Nagar": [17.3457, 78.5522], "Uppal": [17.4018, 78.5602], 
    "Boduppal": [17.4138, 78.5794], "Hayathnagar": [17.3195, 78.6019], "Vanasthalipuram": [17.3364, 78.5562], 
    "Saroornagar": [17.3516, 78.5323], "Mehdipatnam": [17.3929, 78.4326], "Tolichowki": [17.4005, 78.4144], 
    "Attapur": [17.3670, 78.4287], "Rajendra Nagar": [17.3142, 78.4037], "Shamshabad": [17.2625, 78.3965],
    "Nanakramguda": [17.4137, 78.3414], "Kokapet": [17.3957, 78.3248], "Narsingi": [17.3820, 78.3541], 
    "Gandipet": [17.3879, 78.3155], "Patancheru": [17.5287, 78.2667], "Kompally": [17.5519, 78.4839],
    "Alwal": [17.5050, 78.5042], "Malkajgiri": [17.4520, 78.5332], "Nacharam": [17.4241, 78.5620], 
    "Kothapet": [17.3686, 78.5385], "Chanda Nagar": [17.4916, 78.3275], "Bachupally": [17.5458, 78.3842],
    "Nizampet": [17.5186, 78.3860], "Pragathi Nagar": [17.5097, 78.3916], "Film Nagar": [17.4093, 78.4079], 
    "Panjagutta": [17.4261, 78.4518], "Khairatabad": [17.4111, 78.4619], "Masab Tank": [17.3986, 78.4552], 
    "Nampally": [17.3850, 78.4687], "Abids": [17.3888, 78.4735], "Himayatnagar": [17.4005, 78.4841], 
    "Narayanguda": [17.3980, 78.4879], "Tarnaka": [17.4300, 78.5375]
}

rent_rules = {
    "high": ["Jubilee Hills", "Banjara Hills", "Film Nagar", "Panjagutta"],
    "mid_high": ["Gachibowli", "Madhapur", "Hitech City", "Begumpet"],
    "mid": ["Kondapur", "Manikonda", "Nanakramguda", "Kokapet", "Narsingi"],
    "mid_low": ["Kukatpally", "Miyapur", "Nallagandla", "Ameerpet", "SR Nagar", "Himayatnagar"],
    "low": ["ECIL", "Uppal", "Boduppal", "Malkajgiri", "Kompally", "Alwal", "Nacharam",
            "Dilsukhnagar", "LB Nagar", "Hayathnagar", "Vanasthalipuram", "Saroornagar",
            "Mehdipatnam", "Tolichowki", "Attapur", "Rajendra Nagar", "Shamshabad",
            "Nampally", "Abids", "Narayanguda", "Masab Tank", "Kothapet",
            "Tarnaka", "Secunderabad", "Patancheru", "Bachupally", "Nizampet", "Chanda Nagar", "Pragathi Nagar", "Khairatabad"]
}

def get_rent(area, bhk):
    if area in rent_rules["high"]: r = random.randint(25000, 65000)
    elif area in rent_rules["mid_high"]: r = random.randint(15000, 45000)
    elif area in rent_rules["mid"]: r = random.randint(12000, 30000)
    elif area in rent_rules["mid_low"]: r = random.randint(8000, 22000)
    else: r = random.randint(6000, 18000)
    return r + (bhk-1) * 3000

it_areas = ["Hitech City", "Madhapur", "Gachibowli", "Kondapur"]

properties = []
id_counter = 1

for _ in range(80):
    area = random.choice(areas)
    bhk = random.randint(1, 4)
    bath = min(bhk, 3)
    sqft = bhk * random.randint(450, 700)
    
    lat = coordinates[area][0] + random.uniform(-0.005, 0.005)
    lng = coordinates[area][1] + random.uniform(-0.005, 0.005)
    
    furnished = random.choice(["Unfurnished", "Semi-Furnished", "Furnished"])
    soc_type = random.choice(["family", "bachelor", "mixed"])
    
    bachelor_friendly = True if area in rent_rules["mid_high"] or area in rent_rules["low"] or soc_type == "bachelor" else random.choice([True, False])
    girl_friendly = True if area in rent_rules["high"] or soc_type == "family" else random.choice([True, False])
    
    tags = []
    if area in it_areas: tags.append("Near IT Hub")
    if random.random() > 0.5: tags.append("Safe Area")
    if random.random() > 0.6: tags.append("Metro Access")
    if girl_friendly: tags.append("Girl Friendly")
    if bachelor_friendly: tags.append("Bachelor Friendly")
    
    tenant_type = "family" if soc_type == "family" else ("bachelor" if soc_type == "bachelor" else "any")
    
    prop = {
        "id": id_counter,
        "title": f"{furnished} {bhk}BHK Apartment in {area}",
        "address": f"Plot {random.randint(10, 100)}, Near Main Road, {area}, Hyderabad",
        "area": area,
        "rent_monthly": get_rent(area, bhk),
        "bedrooms": bhk,
        "bathrooms": bath,
        "sqft": sqft,
        "lat": round(lat, 5),
        "lng": round(lng, 5),
        "description": f"Excellent {bhk}BHK apartment available for rent in {area}. Comes with 24/7 security.",
        "furnished": furnished,
        "parking": random.choice([True, False]),
        "floor": random.randint(1, 10),
        "building_age": random.randint(1, 15),
        "owner_name": random.choice(["Rajesh", "Suresh", "Ravi", "Kiran", "Anita", "Priya"]),
        "contact": "9" + "".join([str(random.randint(0, 9)) for _ in range(9)]),
        "image_url": f"https://picsum.photos/seed/{id_counter+42}/800/500",
        "tags": list(set(tags))[:3],
        "tenant_type": tenant_type,
        "bachelor_friendly": bachelor_friendly,
        "girl_friendly": girl_friendly,
        "society_type": soc_type
    }
    properties.append(prop)
    id_counter += 1

with open("properties.json", "w", encoding="utf-8") as f:
    json.dump(properties, f, indent=2)

print("Generated properties.json")

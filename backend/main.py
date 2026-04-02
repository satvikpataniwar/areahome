from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json, os, asyncio
import google.generativeai as genai
from dotenv import load_dotenv
from enrichment import get_water_score, get_weather_score, get_area_scores, get_social_scores

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

with open("properties.json", "r", encoding="utf-8") as f:
    ALL_PROPERTIES = json.load(f)

# 🟢 CHANGED: Added amenities for ALL Hyderabad areas
AREA_AMENITIES = {
    "Gachibowli": [
        {"name": "IKEA Hyderabad", "type": "mall", "lat": 17.4355, "lng": 78.3487},
        {"name": "Continental Hospital", "type": "hospital", "lat": 17.4313, "lng": 78.3579},
        {"name": "Gachibowli Stadium", "type": "gym", "lat": 17.4399, "lng": 78.3488},
        {"name": "More Supermarket", "type": "supermarket", "lat": 17.4400, "lng": 78.3500},
        {"name": "DLF Cybercity", "type": "it_hub", "lat": 17.4418, "lng": 78.3810}
    ],
    "Kondapur": [
        {"name": "Botanical Garden", "type": "park", "lat": 17.4508, "lng": 78.3916},
        {"name": "Forum Sujana Mall", "type": "mall", "lat": 17.4814, "lng": 78.3741},
        {"name": "Apollo Pharmacy", "type": "hospital", "lat": 17.4600, "lng": 78.3700},
        {"name": "BigBazaar Kondapur", "type": "supermarket", "lat": 17.4550, "lng": 78.3800},
        {"name": "Raheja Mindspace", "type": "it_hub", "lat": 17.4517, "lng": 78.3833}
    ],
    "Madhapur": [
        {"name": "Cyber Towers", "type": "it_hub", "lat": 17.4476, "lng": 78.3813},
        {"name": "Hyderabad Central Mall", "type": "mall", "lat": 17.4509, "lng": 78.3763},
        {"name": "Apollo Pharmacy", "type": "hospital", "lat": 17.4480, "lng": 78.3790},
        {"name": "Reliance Fresh", "type": "supermarket", "lat": 17.4490, "lng": 78.3800},
        {"name": "Shilparamam", "type": "temple", "lat": 17.4559, "lng": 78.3800}
    ],
    "Hitech City": [
        {"name": "Cyber Pearl", "type": "it_hub", "lat": 17.4508, "lng": 78.3764},
        {"name": "Westin Hotel Gym", "type": "gym", "lat": 17.4462, "lng": 78.3729},
        {"name": "Hitech City Metro", "type": "transport", "lat": 17.4485, "lng": 78.3719},
        {"name": "Inorbit Mall", "type": "mall", "lat": 17.4344, "lng": 78.3890},
        {"name": "MaxCure Hospital", "type": "hospital", "lat": 17.4520, "lng": 78.3750}
    ],
    "Banjara Hills": [
        {"name": "GVK One Mall", "type": "mall", "lat": 17.4234, "lng": 78.4468},
        {"name": "KBR National Park", "type": "park", "lat": 17.4237, "lng": 78.4191},
        {"name": "Care Hospital", "type": "hospital", "lat": 17.4230, "lng": 78.4456},
        {"name": "Spencer's Supermarket", "type": "supermarket", "lat": 17.4250, "lng": 78.4430},
        {"name": "Birla Mandir", "type": "temple", "lat": 17.4062, "lng": 78.4691}
    ],
    "Jubilee Hills": [
        {"name": "KBR Park", "type": "park", "lat": 17.4237, "lng": 78.4191},
        {"name": "Apollo Hospital", "type": "hospital", "lat": 17.4360, "lng": 78.4403},
        {"name": "Anytime Fitness", "type": "gym", "lat": 17.4326, "lng": 78.4082},
        {"name": "BigBazaar Jubilee Hills", "type": "supermarket", "lat": 17.4310, "lng": 78.4100}
    ],
    "Kukatpally": [
        {"name": "KPHB Metro Station", "type": "transport", "lat": 17.4939, "lng": 78.3936},
        {"name": "JNTU Hyderabad", "type": "school", "lat": 17.4939, "lng": 78.3920},
        {"name": "Kukatpally Area Hospital", "type": "hospital", "lat": 17.4950, "lng": 78.3940},
        {"name": "DMart Kukatpally", "type": "supermarket", "lat": 17.4955, "lng": 78.3960}
    ],
    "Miyapur": [
        {"name": "Miyapur Metro Station", "type": "transport", "lat": 17.5133, "lng": 78.3553},
        {"name": "Bhavya Nilayam Temple", "type": "temple", "lat": 17.5116, "lng": 78.3567},
        {"name": "DMart Miyapur", "type": "supermarket", "lat": 17.5120, "lng": 78.3580},
        {"name": "SLG Hospital", "type": "hospital", "lat": 17.5100, "lng": 78.3540}
    ],
    "Manikonda": [
        {"name": "Lanco Hills IT Park", "type": "it_hub", "lat": 17.4063, "lng": 78.3803},
        {"name": "Manikonda Lake Park", "type": "park", "lat": 17.4010, "lng": 78.3750},
        {"name": "Reliance Fresh Manikonda", "type": "supermarket", "lat": 17.4050, "lng": 78.3800}
    ],
    "Nallagandla": [
        {"name": "Nallagandla Lake", "type": "park", "lat": 17.4618, "lng": 78.3245},
        {"name": "ISB Hyderabad", "type": "school", "lat": 17.4604, "lng": 78.3328},
        {"name": "Nallagandla Clinic", "type": "hospital", "lat": 17.4610, "lng": 78.3300}
    ],
    "ECIL": [
        {"name": "ECIL Metro Station", "type": "transport", "lat": 17.4695, "lng": 78.5547},
        {"name": "Aditya Hospital ECIL", "type": "hospital", "lat": 17.4700, "lng": 78.5560},
        {"name": "DMart ECIL", "type": "supermarket", "lat": 17.4680, "lng": 78.5530},
        {"name": "ECIL Park", "type": "park", "lat": 17.4710, "lng": 78.5580}
    ],
    "Secunderabad": [
        {"name": "Paradise Circle", "type": "mall", "lat": 17.4377, "lng": 78.4987},
        {"name": "Secunderabad Station Metro", "type": "transport", "lat": 17.4345, "lng": 78.5014},
        {"name": "Apollo Hospital Sec'bad", "type": "hospital", "lat": 17.4400, "lng": 78.5000},
        {"name": "Rashtrapathi Road Market", "type": "supermarket", "lat": 17.4350, "lng": 78.5000}
    ],
    "Begumpet": [
        {"name": "Begumpet Airport Road", "type": "transport", "lat": 17.4437, "lng": 78.4685},
        {"name": "Hyderabad Central Mall Begumpet", "type": "mall", "lat": 17.4450, "lng": 78.4690},
        {"name": "Care Hospital Begumpet", "type": "hospital", "lat": 17.4440, "lng": 78.4670},
        {"name": "Reliance Mart", "type": "supermarket", "lat": 17.4460, "lng": 78.4700}
    ],
    "Ameerpet": [
        {"name": "Ameerpet Metro", "type": "transport", "lat": 17.4374, "lng": 78.4487},
        {"name": "SR Nagar Market", "type": "supermarket", "lat": 17.4380, "lng": 78.4480},
        {"name": "Sunshine Hospital", "type": "hospital", "lat": 17.4390, "lng": 78.4490},
        {"name": "Ameerpet Coaching Hubs", "type": "school", "lat": 17.4370, "lng": 78.4470}
    ],
    "SR Nagar": [
        {"name": "SR Nagar Metro", "type": "transport", "lat": 17.4445, "lng": 78.4387},
        {"name": "SR Nagar Market", "type": "supermarket", "lat": 17.4440, "lng": 78.4380},
        {"name": "Uma Hospital", "type": "hospital", "lat": 17.4450, "lng": 78.4400}
    ],
    "Dilsukhnagar": [
        {"name": "Dilsukhnagar Metro", "type": "transport", "lat": 17.3686, "lng": 78.5249},
        {"name": "Moosarambagh Market", "type": "supermarket", "lat": 17.3700, "lng": 78.5240},
        {"name": "Kamineni Hospital", "type": "hospital", "lat": 17.3690, "lng": 78.5220}
    ],
    "LB Nagar": [
        {"name": "LB Nagar Metro", "type": "transport", "lat": 17.3500, "lng": 78.5500},
        {"name": "LB Nagar Market", "type": "supermarket", "lat": 17.3510, "lng": 78.5510},
        {"name": "Citizens Hospital LB Nagar", "type": "hospital", "lat": 17.3520, "lng": 78.5490}
    ],
    "Uppal": [
        {"name": "Uppal Metro", "type": "transport", "lat": 17.4011, "lng": 78.5593},
        {"name": "Uppal Market", "type": "supermarket", "lat": 17.4020, "lng": 78.5600},
        {"name": "Pranaam Hospital", "type": "hospital", "lat": 17.4000, "lng": 78.5580}
    ],
    "Mehdipatnam": [
        {"name": "Mehdipatnam Metro", "type": "transport", "lat": 17.3924, "lng": 78.4290},
        {"name": "BigBazaar Mehdipatnam", "type": "supermarket", "lat": 17.3930, "lng": 78.4300},
        {"name": "Medicover Hospital", "type": "hospital", "lat": 17.3920, "lng": 78.4280}
    ],
    "Tolichowki": [
        {"name": "Tolichowki Masjid", "type": "temple", "lat": 17.4031, "lng": 78.4090},
        {"name": "Reliance Fresh Tolichowki", "type": "supermarket", "lat": 17.4040, "lng": 78.4100},
        {"name": "Tolichowki Hospital", "type": "hospital", "lat": 17.4020, "lng": 78.4080}
    ],
    "Kompally": [
        {"name": "Kompally Market", "type": "supermarket", "lat": 17.5531, "lng": 78.4810},
        {"name": "Global Hospital Kompally", "type": "hospital", "lat": 17.5540, "lng": 78.4820},
        {"name": "Kompally Lake", "type": "park", "lat": 17.5550, "lng": 78.4800}
    ],
    "Bachupally": [
        {"name": "Bachupally Market", "type": "supermarket", "lat": 17.5337, "lng": 78.3840},
        {"name": "Bachupally Hospital", "type": "hospital", "lat": 17.5345, "lng": 78.3850},
        {"name": "Nizampet Park", "type": "park", "lat": 17.5300, "lng": 78.3900}
    ],
    "Nizampet": [
        {"name": "Nizampet Market", "type": "supermarket", "lat": 17.5230, "lng": 78.3900},
        {"name": "Nizampet Hospital", "type": "hospital", "lat": 17.5240, "lng": 78.3910},
        {"name": "Nizampet Lake", "type": "park", "lat": 17.5220, "lng": 78.3890}
    ],
    "Himayatnagar": [
        {"name": "Himayatnagar Metro", "type": "transport", "lat": 17.4120, "lng": 78.4820},
        {"name": "Apollo Hospital Jubilee Hills", "type": "hospital", "lat": 17.4130, "lng": 78.4830},
        {"name": "More Supermarket Himayatnagar", "type": "supermarket", "lat": 17.4115, "lng": 78.4810},
        {"name": "Hyderabad Club Park", "type": "park", "lat": 17.4100, "lng": 78.4800}
    ],
    "Panjagutta": [
        {"name": "Panjagutta Metro", "type": "transport", "lat": 17.4261, "lng": 78.4498},
        {"name": "Panjagutta Market", "type": "supermarket", "lat": 17.4270, "lng": 78.4510},
        {"name": "Yashoda Hospital", "type": "hospital", "lat": 17.4255, "lng": 78.4490}
    ],
    "Nanakramguda": [
        {"name": "Financial District IT Park", "type": "it_hub", "lat": 17.4230, "lng": 78.3470},
        {"name": "Nanakramguda Market", "type": "supermarket", "lat": 17.4235, "lng": 78.3490},
        {"name": "Omega Hospital", "type": "hospital", "lat": 17.4220, "lng": 78.3480}
    ],
    "Kokapet": [
        {"name": "Kokapet IT Zone", "type": "it_hub", "lat": 17.4110, "lng": 78.3290},
        {"name": "Kokapet Market", "type": "supermarket", "lat": 17.4120, "lng": 78.3300},
        {"name": "Kokapet Lake", "type": "park", "lat": 17.4100, "lng": 78.3280}
    ],
    "Narsingi": [
        {"name": "Narsingi Lake", "type": "park", "lat": 17.3960, "lng": 78.3450},
        {"name": "Narsingi Market", "type": "supermarket", "lat": 17.3970, "lng": 78.3460},
        {"name": "Narsingi Hospital", "type": "hospital", "lat": 17.3950, "lng": 78.3440}
    ],
    "Gandipet": [
        {"name": "Gandipet Lake (Osman Sagar)", "type": "park", "lat": 17.3740, "lng": 78.3310},
        {"name": "Gandipet Market", "type": "supermarket", "lat": 17.3760, "lng": 78.3330}
    ],
    "Tarnaka": [
        {"name": "Tarnaka Metro", "type": "transport", "lat": 17.4324, "lng": 78.5403},
        {"name": "Osmania University", "type": "school", "lat": 17.4148, "lng": 78.5256},
        {"name": "Tarnaka Market", "type": "supermarket", "lat": 17.4330, "lng": 78.5410},
        {"name": "Care Hospital Tarnaka", "type": "hospital", "lat": 17.4320, "lng": 78.5395}
    ],
    "Film Nagar": [
        {"name": "Film Nagar Lake", "type": "park", "lat": 17.4031, "lng": 78.4080},
        {"name": "Ramoji Film City", "type": "mall", "lat": 17.2543, "lng": 78.6808},
        {"name": "Film Nagar Hospital", "type": "hospital", "lat": 17.4040, "lng": 78.4090},
        {"name": "More Supermarket Film Nagar", "type": "supermarket", "lat": 17.4025, "lng": 78.4070}
    ],
    "Khairatabad": [
        {"name": "Khairatabad Metro", "type": "transport", "lat": 17.4197, "lng": 78.4570},
        {"name": "Hussain Sagar Lake", "type": "park", "lat": 17.4239, "lng": 78.4738},
        {"name": "Khairatabad Market", "type": "supermarket", "lat": 17.4200, "lng": 78.4580}
    ],
    "Masab Tank": [
        {"name": "Masab Tank Metro", "type": "transport", "lat": 17.4031, "lng": 78.4498},
        {"name": "Koti Hospital", "type": "hospital", "lat": 17.4040, "lng": 78.4510},
        {"name": "Masab Tank Market", "type": "supermarket", "lat": 17.4020, "lng": 78.4490}
    ],
    "Malkajgiri": [
        {"name": "Malkajgiri Metro", "type": "transport", "lat": 17.4581, "lng": 78.5251},
        {"name": "Malkajgiri Market", "type": "supermarket", "lat": 17.4590, "lng": 78.5260},
        {"name": "Malkajgiri Hospital", "type": "hospital", "lat": 17.4575, "lng": 78.5245}
    ],
    "Alwal": [
        {"name": "Alwal Market", "type": "supermarket", "lat": 17.5007, "lng": 78.5090},
        {"name": "Alwal Hospital", "type": "hospital", "lat": 17.5015, "lng": 78.5100},
        {"name": "Alwal Lake", "type": "park", "lat": 17.5000, "lng": 78.5080}
    ],
    "Boduppal": [
        {"name": "Boduppal Market", "type": "supermarket", "lat": 17.4151, "lng": 78.5891},
        {"name": "Boduppal Hospital", "type": "hospital", "lat": 17.4160, "lng": 78.5900}
    ],
    "Hayathnagar": [
        {"name": "Hayathnagar Market", "type": "supermarket", "lat": 17.3342, "lng": 78.6015},
        {"name": "Hayathnagar Hospital", "type": "hospital", "lat": 17.3350, "lng": 78.6020}
    ],
    "Vanasthalipuram": [
        {"name": "Vanasthalipuram Market", "type": "supermarket", "lat": 17.3368, "lng": 78.5510},
        {"name": "Vanasthalipuram Hospital", "type": "hospital", "lat": 17.3380, "lng": 78.5520}
    ],
    "Saroornagar": [
        {"name": "Saroornagar Market", "type": "supermarket", "lat": 17.3491, "lng": 78.5387},
        {"name": "Saroornagar Hospital", "type": "hospital", "lat": 17.3500, "lng": 78.5395}
    ],
    "Attapur": [
        {"name": "Attapur Market", "type": "supermarket", "lat": 17.3588, "lng": 78.4198},
        {"name": "Attapur Hospital", "type": "hospital", "lat": 17.3595, "lng": 78.4205}
    ],
    "Rajendra Nagar": [
        {"name": "Rajendra Nagar Market", "type": "supermarket", "lat": 17.3269, "lng": 78.4408},
        {"name": "Rajendra Nagar Hospital", "type": "hospital", "lat": 17.3280, "lng": 78.4420},
        {"name": "Rajendra Nagar Lake", "type": "park", "lat": 17.3260, "lng": 78.4395}
    ],
    "Shamshabad": [
        {"name": "RGIA Airport", "type": "transport", "lat": 17.2403, "lng": 78.4294},
        {"name": "Shamshabad Market", "type": "supermarket", "lat": 17.2550, "lng": 78.4280},
        {"name": "Shamshabad Hospital", "type": "hospital", "lat": 17.2560, "lng": 78.4290}
    ],
    "Patancheru": [
        {"name": "Patancheru Market", "type": "supermarket", "lat": 17.5310, "lng": 78.2600},
        {"name": "Patancheru Hospital", "type": "hospital", "lat": 17.5320, "lng": 78.2610}
    ],
    "Chanda Nagar": [
        {"name": "Chanda Nagar Market", "type": "supermarket", "lat": 17.4933, "lng": 78.3240},
        {"name": "Chanda Nagar Hospital", "type": "hospital", "lat": 17.4940, "lng": 78.3250},
        {"name": "Chanda Nagar Lake", "type": "park", "lat": 17.4920, "lng": 78.3230}
    ],
    "Pragathi Nagar": [
        {"name": "Pragathi Nagar Market", "type": "supermarket", "lat": 17.5197, "lng": 78.3720},
        {"name": "Pragathi Nagar Hospital", "type": "hospital", "lat": 17.5205, "lng": 78.3730}
    ],
    "Nacharam": [
        {"name": "Nacharam IT Park", "type": "it_hub", "lat": 17.4031, "lng": 78.5558},
        {"name": "Nacharam Market", "type": "supermarket", "lat": 17.4040, "lng": 78.5565},
        {"name": "Nacharam Hospital", "type": "hospital", "lat": 17.4025, "lng": 78.5550}
    ],
    "Kothapet": [
        {"name": "Kothapet Metro", "type": "transport", "lat": 17.3688, "lng": 78.5310},
        {"name": "Kothapet Market", "type": "supermarket", "lat": 17.3695, "lng": 78.5320},
        {"name": "Kothapet Hospital", "type": "hospital", "lat": 17.3680, "lng": 78.5300}
    ],
    "Nampally": [
        {"name": "Nampally Railway Station", "type": "transport", "lat": 17.3864, "lng": 78.4683},
        {"name": "Nampally Market", "type": "supermarket", "lat": 17.3870, "lng": 78.4690},
        {"name": "Gandhi Hospital", "type": "hospital", "lat": 17.3852, "lng": 78.4780}
    ],
    "Abids": [
        {"name": "Abids Metro", "type": "transport", "lat": 17.3868, "lng": 78.4762},
        {"name": "Hyderabad City Center", "type": "mall", "lat": 17.3875, "lng": 78.4770},
        {"name": "Nizam's Museum", "type": "park", "lat": 17.3880, "lng": 78.4760}
    ],
    "Narayanguda": [
        {"name": "Narayanguda Market", "type": "supermarket", "lat": 17.3932, "lng": 78.4882},
        {"name": "Osmania Hospital", "type": "hospital", "lat": 17.3940, "lng": 78.4890}
    ],
    "Himayatnagar": [
        {"name": "Himayatnagar Metro", "type": "transport", "lat": 17.4120, "lng": 78.4820},
        {"name": "More Supermarket", "type": "supermarket", "lat": 17.4115, "lng": 78.4810},
        {"name": "Care Hospital", "type": "hospital", "lat": 17.4130, "lng": 78.4830}
    ]
}

class SearchRequest(BaseModel):
    query: str

class ChatRequest(BaseModel):
    message: str
    context: str = ""

# 🟢 CHANGED: parse_requirements now understands social context (bachelor/girl/family)
def parse_requirements(query: str) -> dict:
    prompt = f"""
You are a rental property assistant for Hyderabad, India.
Extract search requirements from this user query: "{query}"

Return ONLY a valid JSON object with exactly these keys. No explanation. No markdown.
{{
  "max_rent": <integer in rupees, default 50000. Convert "20k"=20000, "1 lakh"=100000>,
  "min_bedrooms": <integer, default 1>,
  "preferred_areas": <list of area names matching exactly from the full Hyderabad area list. Extract ANY area mentioned. ECIL, Gachibowli, Madhapur, Hitech City, Kukatpally, Banjara Hills, Jubilee Hills, Miyapur, Manikonda, Nallagandla, Kondapur, ECIL, Secunderabad, Begumpet, Ameerpet, SR Nagar, Dilsukhnagar, LB Nagar, Uppal, Boduppal, Hayathnagar, Vanasthalipuram, Saroornagar, Mehdipatnam, Tolichowki, Attapur, Rajendra Nagar, Shamshabad, Nanakramguda, Kokapet, Narsingi, Gandipet, Patancheru, Kompally, Alwal, Malkajgiri, Nacharam, Kothapet, Chanda Nagar, Bachupally, Nizampet, Pragathi Nagar, Film Nagar, Panjagutta, Khairatabad, Masab Tank, Nampally, Abids, Himayatnagar, Narayanguda, Tarnaka. Empty list = search all>,
  "priorities": {{
    "water_supply": <0-10>,
    "safety": <0-10>,
    "schools": <0-10>,
    "it_proximity": <0-10>,
    "transport": <0-10>,
    "greenness": <0-10>,
    "weather": <0-10>,
    "gym": <0-10>,
    "temple": <0-10>
  }},
  "furnished_pref": <"any" or "Furnished" or "Semi-Furnished" or "Unfurnished">,
  "social_context": {{
    "is_girl": <true if user says she is a girl/woman/female, else false>,
    "is_bachelor": <true if user mentions bachelor/single/working professional alone, else false>,
    "wants_families_nearby": <true if user wants families around, false if user wants bachelors around, null if not mentioned>,
    "safety_priority": <"high" if girl/safety focused, "normal" otherwise>,
    "special_notes": <any special requirements like "no families", "only girls hostel", "near college" etc>
  }}
}}

Examples:
- "I am a girl I want 2bhk in ECIL under 20k and only families around" -> is_girl=true, wants_families_nearby=true, safety_priority=high
- "I want 3bhk in Gachibowli I want bachelors around" -> is_bachelor=false, wants_families_nearby=false
- "bachelor flat near IT companies" -> is_bachelor=true
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception as e:
        return {
            "max_rent": 50000, "min_bedrooms": 1, "preferred_areas": [],
            "priorities": {"water_supply": 5, "safety": 5, "schools": 5, "it_proximity": 5, "transport": 5, "greenness": 5, "weather": 5, "gym": 3, "temple": 3},
            "furnished_pref": "any",
            "social_context": {"is_girl": False, "is_bachelor": False, "wants_families_nearby": None, "safety_priority": "normal", "special_notes": ""}
        }

def generate_property_tags(prop: dict, scores: dict) -> list:
    tags = []
    if scores.get("Safety", 0) >= 7.5:
        tags.append({"label": "Safe Area", "color": "green"})
    if scores.get("Water Supply", 0) >= 7.5:
        tags.append({"label": "Good Water Supply", "color": "blue"})
    if scores.get("Greenness", 0) >= 7.5:
        tags.append({"label": "Green Surroundings", "color": "emerald"})
    if scores.get("IT Hub", 0) >= 8.0:
        tags.append({"label": "Near IT Hub", "color": "purple"})
    if scores.get("Transport", 0) >= 8.0:
        tags.append({"label": "Metro Access", "color": "indigo"})
    if scores.get("Schools", 0) >= 8.0:
        tags.append({"label": "Near Schools", "color": "amber"})
    if prop.get("rent_monthly", 0) < 20000:
        tags.append({"label": "Affordable", "color": "teal"})
    if prop.get("bachelor_friendly", False):
        tags.append({"label": "Bachelor Friendly", "color": "violet"})
    if prop.get("girl_friendly", False):
        tags.append({"label": "Girl Friendly", "color": "pink"})
    return tags[:4]

async def enrich_property(prop: dict, requirements: dict) -> dict:
    water_result, weather_result = await asyncio.gather(
        get_water_score(prop["lat"], prop["lng"], prop["area"]),
        get_weather_score(prop["lat"], prop["lng"])
    )
    weather_score, weather_details = weather_result
    area_scores = get_area_scores(prop["area"])
    social_scores = get_social_scores(prop["area"])
    score_breakdown = {
        "Water Supply": water_result,
        "Safety": area_scores["Safety"],
        "IT Hub": area_scores["IT Hub"],
        "Schools": area_scores["Schools"],
        "Transport": area_scores["Transport"],
        "Greenness": area_scores["Greenness"],
        "Weather": weather_score
    }
    priorities = requirements.get("priorities", {})
    social_context = requirements.get("social_context", {})
    priority_map = {
        "water_supply": "Water Supply",
        "safety": "Safety",
        "it_proximity": "IT Hub",
        "schools": "Schools",
        "transport": "Transport",
        "greenness": "Greenness",
        "weather": "Weather"
    }
    weighted = 0
    total_w = 0
    for pk, sk in priority_map.items():
        w = priorities.get(pk, 5)
        v = score_breakdown.get(sk, 6)
        weighted += w * v
        total_w += w

    # 🟢 NEW: Apply social context bonuses/penalties
    social_bonus = 0
    if social_context.get("is_girl"):
        # Boost properties with high girl-friendly score
        girl_score = social_scores.get("Girl Friendly", 6.0)
        social_bonus += (girl_score - 6.0) * 2
    wants_families = social_context.get("wants_families_nearby")
    if wants_families is True:
        family_score = social_scores.get("Family Score", 7.0)
        social_bonus += (family_score - 5.0)
        prop_type = prop.get("society_type", "mixed")
        if prop_type == "family":
            social_bonus += 5
    elif wants_families is False:
        bachelor_score = social_scores.get("Bachelor Score", 6.0)
        social_bonus += (bachelor_score - 5.0)
        prop_type = prop.get("society_type", "mixed")
        if prop_type == "bachelor" or prop.get("bachelor_friendly", False):
            social_bonus += 5

    max_rent = requirements.get("max_rent", 50000)
    price_ratio = max(0, 1 - (prop["rent_monthly"] / max_rent))
    price_score = min(10, price_ratio * 10 + 4)
    if total_w > 0:
        base = (weighted / total_w)
        final_score = int(base * 0.70 * 10 + price_score * 0.25 + social_bonus * 0.05)
    else:
        final_score = 60
    final_score = max(10, min(100, final_score))
    tags = generate_property_tags(prop, score_breakdown)

    match_prompt = f"""
User wants: "{requirements.get('query', '')}"
Social context: Girl={social_context.get('is_girl', False)}, Wants families={social_context.get('wants_families_nearby')}, Bachelor={social_context.get('is_bachelor', False)}
Property: {prop['bedrooms']}BHK in {prop['area']} at Rs{prop['rent_monthly']}/month, {prop['sqft']}sqft, {prop['furnished']}.
Society type: {prop.get('society_type', 'mixed')}, Bachelor friendly: {prop.get('bachelor_friendly', False)}, Girl friendly: {prop.get('girl_friendly', False)}
Top scores: Water={score_breakdown['Water Supply']}, Safety={score_breakdown['Safety']}, IT Hub={score_breakdown['IT Hub']}

Write ONE sentence (max 25 words) saying why this property specifically matches what they asked for. Be specific about area and their unique requirements.
Return ONLY the sentence.
"""
    try:
        match_response = model.generate_content(match_prompt)
        match_reason = match_response.text.strip().strip('"')
    except:
        match_reason = f"Well-located {prop['bedrooms']}BHK in {prop['area']} matching your requirements."

    return {
        **prop,
        "score": final_score,
        "score_breakdown": score_breakdown,
        "weather_details": weather_details,
        "match_reason": match_reason,
        "nearby_amenities": AREA_AMENITIES.get(prop["area"], []),
        "tags": tags
    }

@app.post("/api/search")
async def search_properties(request: SearchRequest):
    requirements = parse_requirements(request.query)
    requirements["query"] = request.query
    max_rent = requirements.get("max_rent", 50000)
    min_bedrooms = requirements.get("min_bedrooms", 1)
    preferred_areas = requirements.get("preferred_areas", [])
    furnished_pref = requirements.get("furnished_pref", "any")
    social_context = requirements.get("social_context", {})
    filtered = []
    for prop in ALL_PROPERTIES:
        if prop["rent_monthly"] > max_rent:
            continue
        if prop["bedrooms"] < min_bedrooms:
            continue
        if preferred_areas and prop["area"] not in preferred_areas:
            continue
        if furnished_pref != "any" and prop["furnished"] != furnished_pref:
            continue
        # 🟢 NEW: Filter by social context
        wants_families = social_context.get("wants_families_nearby")
        if wants_families is False:
            # User wants bachelor-friendly area — skip strict family-only properties
            if prop.get("tenant_type") == "family":
                continue
        filtered.append(prop)
    if not filtered:
        filtered = sorted(ALL_PROPERTIES, key=lambda x: x["rent_monthly"])[:8]
    if len(filtered) > 12:
        filtered = filtered[:12]
    results = await asyncio.gather(*[enrich_property(p, requirements) for p in filtered])
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return {"results": list(results), "total": len(results), "query": request.query, "requirements": requirements}

# 🟢 NEW: AI Chatbot endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest):
    prompt = f"""
You are AreaHome AI Assistant, an expert on Hyderabad rental properties and neighborhoods.
You have deep knowledge of all areas: Gachibowli, ECIL, Kondapur, Madhapur, Hitech City, Kukatpally, Banjara Hills, Jubilee Hills, Miyapur, Manikonda, Nallagandla, Secunderabad, Begumpet, Ameerpet, SR Nagar, Dilsukhnagar, LB Nagar, Uppal, Mehdipatnam, Tolichowki, Kompally, Bachupally, Nizampet, Tarnaka, Film Nagar, Panjagutta, Himayatnagar, and all other Hyderabad areas.

Context from search: {request.context}

User message: {request.message}

Answer helpfully and specifically about Hyderabad. If they ask about:
- Area comparisons: compare rent, safety, transport, amenities
- Bachelor vs family friendly: give honest area recommendations  
- Girl safety: recommend safe gated areas, mention security features
- Budget: suggest realistic areas for their budget
- Commute: suggest areas close to their workplace

Keep answer under 150 words. Be conversational and helpful. Use ₹ for rupees.
"""
    try:
        response = model.generate_content(prompt)
        return {"reply": response.text.strip()}
    except Exception as e:
        return {"reply": "Sorry, I'm having trouble connecting. Please try again!"}

@app.get("/")
def root():
    return {"status": "AreaHome API running", "city": "Hyderabad"}

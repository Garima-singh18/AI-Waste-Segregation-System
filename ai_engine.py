import os
import json
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# =========================================================
# GEMINI CLIENT
# =========================================================

client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception:
        client = None


# =========================================================
# LOCAL WASTE KNOWLEDGE
# =========================================================

WASTE_KNOWLEDGE = {

    # =====================================================
    # PLASTIC
    # =====================================================

    "Plastic": {

        "keywords": [
            "plastic",
            "plastic bottle",
            "water bottle",
            "mineral water bottle",
            "soft drink bottle",
            "cold drink bottle",
            "juice bottle",
            "shampoo bottle",
            "lotion bottle",
            "oil bottle",
            "detergent bottle",
            "handwash bottle",
            "plastic container",
            "plastic box",
            "plastic cup",
            "plastic glass",
            "plastic spoon",
            "plastic fork",
            "plastic plate",
            "plastic straw",
            "plastic bag",
            "polythene",
            "polybag",
            "plastic packet",
            "plastic wrapper",
            "chips packet",
            "chips wrapper",
            "lays packet",
            "lays wrapper",
            "kurkure packet",
            "kurkure wrapper",
            "namkeen packet",
            "snack packet",
            "snack wrapper",
            "biscuit packet",
            "biscuit wrapper",
            "cookie packet",
            "food packet",
            "food wrapper",
            "chocolate wrapper",
            "candy wrapper",
            "toffee wrapper",
            "ice cream wrapper",
            "ice cream cup",
            "milk packet",
            "milk pouch",
            "bread packet",
            "bread wrapper",
            "chips pouch",
            "packaging plastic",
            "thermocol",
            "styrofoam",
            "plastic toy",
            "plastic hanger",
            "plastic bucket",
            "plastic mug",
            "plastic tub",
            "plastic basket",
            "plastic chair",
            "plastic comb",
            "plastic toothbrush",
            "toothbrush",
            "plastic cap",
            "bottle cap",
            "plastic lid",
            "plastic pipe",
            "plastic wire",
            "plastic packaging",
            "cling film",
            "plastic film",
            "bubble wrap",
            "plastic tape",
            "synthetic packaging"
        ],

        "result": {
            "waste_name": "Plastic Waste",
            "category": "Plastic",
            "biodegradable": "No",
            "recyclable": "Depends",
            "disposal_method":
                "Keep plastic waste separate from wet waste and place it in an appropriate dry/plastic waste collection. "
                "Clean recyclable plastic should preferably be sent to a recycling facility.",
            "environmental_impact":
                "Plastic can remain in the environment for a very long time and can contribute to land and water pollution. "
                "Some plastic packaging is difficult to recycle.",
            "reuse_or_recycling":
                "Reusable plastic containers can be reused where safe. Suitable plastic materials can be collected and sent to recycling facilities.",
            "awareness_tip":
                "Reduce single-use plastic and prefer reusable alternatives whenever possible."
        }
    },


    # =====================================================
    # ORGANIC / FOOD
    # =====================================================

    "Organic": {

        "keywords": [
            "food",
            "food waste",
            "food scraps",
            "food leftovers",
            "leftover food",
            "leftovers",
            "kitchen waste",
            "kitchen scraps",
            "organic waste",
            "banana",
            "banana peel",
            "banana skin",
            "apple",
            "apple core",
            "apple peel",
            "mango",
            "mango peel",
            "orange peel",
            "orange",
            "lemon peel",
            "lemon",
            "fruit",
            "fruit waste",
            "fruit peel",
            "fruit scraps",
            "vegetable",
            "vegetable waste",
            "vegetable peel",
            "vegetable scraps",
            "potato peel",
            "potato skin",
            "onion peel",
            "onion skin",
            "carrot peel",
            "cucumber peel",
            "tomato",
            "tomato waste",
            "cabbage waste",
            "spinach waste",
            "leaf",
            "leaves",
            "dry leaves",
            "plant waste",
            "garden waste",
            "grass",
            "grass clippings",
            "flowers",
            "flower waste",
            "tea leaves",
            "tea waste",
            "coffee grounds",
            "coffee waste",
            "eggshell",
            "egg shell",
            "bread",
            "stale bread",
            "rice waste",
            "cooked rice",
            "dal waste",
            "vegetable scraps",
            "fruit scraps",
            "compost waste",
            "biodegradable waste"
        ],

        "result": {
            "waste_name": "Organic Waste",
            "category": "Organic",
            "biodegradable": "Yes",
            "recyclable": "No",
            "disposal_method":
                "Place organic waste in a wet-waste collection bin or composting system. "
                "Avoid mixing it with recyclable dry waste.",
            "environmental_impact":
                "Organic waste can create unpleasant conditions and greenhouse gas emissions when poorly managed. "
                "Proper composting can convert it into useful organic material.",
            "reuse_or_recycling":
                "Food scraps, fruit peels, vegetable waste and garden waste can often be composted.",
            "awareness_tip":
                "Separate wet organic waste and compost suitable food and garden waste."
        }
    },


    # =====================================================
    # PAPER
    # =====================================================

    "Paper": {

        "keywords": [
            "paper",
            "paper waste",
            "newspaper",
            "old newspaper",
            "newspaper paper",
            "magazine",
            "old magazine",
            "notebook",
            "old notebook",
            "copy",
            "paper sheet",
            "writing paper",
            "printed paper",
            "office paper",
            "document paper",
            "book",
            "old book",
            "textbook",
            "paper bag",
            "paper packet",
            "paper wrapper",
            "paper cup",
            "paper plate",
            "paper box",
            "paperboard",
            "cardboard",
            "cardboard box",
            "carton",
            "cartoon box",
            "shipping box",
            "delivery box",
            "corrugated box",
            "tissue paper",
            "paper towel",
            "receipt",
            "bill paper",
            "envelope",
            "paper envelope",
            "calendar",
            "paper calendar",
            "brochure",
            "flyer",
            "pamphlet",
            "poster",
            "paper packaging"
        ],

        "result": {
            "waste_name": "Paper Waste",
            "category": "Paper",
            "biodegradable": "Yes",
            "recyclable": "Yes",
            "disposal_method":
                "Keep paper clean and dry and place it in a paper or dry recyclable waste collection.",
            "environmental_impact":
                "Paper is biodegradable and recyclable, but excessive paper consumption increases the demand for natural resources.",
            "reuse_or_recycling":
                "Paper can be reused for notes, crafts and packaging, and clean paper can be sent for recycling.",
            "awareness_tip":
                "Use both sides of paper and recycle clean paper whenever possible."
        }
    },


    # =====================================================
    # GLASS
    # =====================================================

    "Glass": {

        "keywords": [
            "glass",
            "glass bottle",
            "glass jar",
            "glass container",
            "glass cup",
            "glass glass",
            "glass plate",
            "glass bowl",
            "broken glass",
            "glass pieces",
            "mirror",
            "glass mirror",
            "window glass",
            "glass window",
            "medicine glass bottle",
            "perfume bottle",
            "glass perfume bottle",
            "sauce bottle",
            "jam jar",
            "pickle jar",
            "food jar",
            "glass packaging"
        ],

        "result": {
            "waste_name": "Glass Waste",
            "category": "Glass",
            "biodegradable": "No",
            "recyclable": "Yes",
            "disposal_method":
                "Separate glass from other waste. Handle broken glass carefully and place it in a suitable glass collection container.",
            "environmental_impact":
                "Glass does not biodegrade easily, but it can be recycled repeatedly and therefore should be properly collected.",
            "reuse_or_recycling":
                "Glass bottles and jars can often be reused or sent to glass recycling facilities.",
            "awareness_tip":
                "Reuse glass containers where safe and separate them for recycling."
        }
    },


    # =====================================================
    # METAL
    # =====================================================

    "Metal": {

        "keywords": [
            "metal",
            "metal waste",
            "iron",
            "steel",
            "aluminium",
            "aluminum",
            "aluminium can",
            "aluminum can",
            "tin can",
            "metal can",
            "soda can",
            "cold drink can",
            "soft drink can",
            "food can",
            "tin container",
            "metal container",
            "metal bottle",
            "metal spoon",
            "metal fork",
            "metal plate",
            "metal box",
            "metal wire",
            "metal pipe",
            "copper",
            "brass",
            "zinc",
            "steel utensil",
            "iron utensil",
            "metal utensil",
            "scrap metal",
            "metal scrap",
            "aluminium foil",
            "aluminum foil",
            "foil",
            "metal lid",
            "metal cap"
        ],

        "result": {
            "waste_name": "Metal Waste",
            "category": "Metal",
            "biodegradable": "No",
            "recyclable": "Yes",
            "disposal_method":
                "Separate metal waste from general and wet waste and send it to an appropriate metal recycling or scrap collection service.",
            "environmental_impact":
                "Metal production requires energy and natural resources. Recycling metals reduces the need for new raw materials.",
            "reuse_or_recycling":
                "Most common metal waste can be recycled and converted into new metal products.",
            "awareness_tip":
                "Separate metal waste and send it to an authorized recycling or scrap collection service."
        }
    },


    # =====================================================
    # E-WASTE
    # =====================================================

    "E-Waste": {

        "keywords": [
            "e waste",
            "e-waste",
            "electronic waste",
            "electronics",
            "electronic item",
            "mobile",
            "mobile phone",
            "phone",
            "smartphone",
            "iphone",
            "android phone",
            "tablet",
            "ipad",
            "laptop",
            "computer",
            "desktop",
            "monitor",
            "screen",
            "television",
            "tv",
            "keyboard",
            "mouse",
            "printer",
            "scanner",
            "router",
            "modem",
            "wifi router",
            "charger",
            "mobile charger",
            "laptop charger",
            "adapter",
            "power adapter",
            "earphone",
            "earphones",
            "headphone",
            "headphones",
            "speaker",
            "bluetooth speaker",
            "smartwatch",
            "watch",
            "camera",
            "digital camera",
            "remote",
            "remote control",
            "calculator",
            "hard disk",
            "ssd",
            "usb",
            "pen drive",
            "memory card",
            "cable",
            "computer cable",
            "electronic cable",
            "game console",
            "gaming console",
            "keyboard",
            "mouse",
            "webcam",
            "microphone",
            "power bank",
            "inverter",
            "electronic appliance",
            "electric appliance"
        ],

        "result": {
            "waste_name": "Electronic Waste",
            "category": "E-Waste",
            "biodegradable": "No",
            "recyclable": "Depends",
            "disposal_method":
                "Do not put electronic items in regular household waste. "
                "Take them to an authorized e-waste collection or recycling facility.",
            "environmental_impact":
                "Electronic waste may contain valuable materials as well as substances that require controlled handling.",
            "reuse_or_recycling":
                "Working electronics can be repaired, reused or donated. Damaged devices should be sent to authorized e-waste recyclers.",
            "awareness_tip":
                "Repair, reuse or donate working electronics and dispose of damaged electronics through authorized e-waste channels."
        }
    },


    # =====================================================
    # HAZARDOUS
    # =====================================================

    "Hazardous": {

        "keywords": [
            "battery",
            "used battery",
            "dead battery",
            "lithium battery",
            "battery cell",
            "car battery",
            "chemical",
            "chemical waste",
            "paint",
            "paint can",
            "pesticide",
            "pesticide bottle",
            "insecticide",
            "fertilizer",
            "cleaning chemical",
            "bleach",
            "acid",
            "solvent",
            "thinner",
            "oil waste",
            "used oil",
            "motor oil",
            "medical waste",
            "medicine",
            "medicine strip",
            "expired medicine",
            "tablet medicine",
            "syringe",
            "needle",
            "razor blade",
            "sanitary pad",
            "diaper",
            "disinfectant",
            "toxic waste",
            "hazardous waste"
        ],

        "result": {
            "waste_name": "Hazardous Waste",
            "category": "Hazardous",
            "biodegradable": "Depends",
            "recyclable": "Depends",
            "disposal_method":
                "Do not mix hazardous materials with normal household waste. "
                "Use an appropriate authorized collection or disposal facility.",
            "environmental_impact":
                "Improperly discarded hazardous materials may contaminate soil and water and can create health and safety risks.",
            "reuse_or_recycling":
                "Some hazardous materials can be safely recovered or recycled through specialized facilities.",
            "awareness_tip":
                "Never mix hazardous waste with regular household garbage."
        }
    },


    # =====================================================
    # TEXTILE
    # =====================================================

    "Textile": {

        "keywords": [
            "cloth",
            "clothes",
            "clothing",
            "textile",
            "fabric",
            "shirt",
            "t-shirt",
            "tshirt",
            "old shirt",
            "old t shirt",
            "jeans",
            "old jeans",
            "trouser",
            "pants",
            "shorts",
            "dress",
            "saree",
            "old saree",
            "kurta",
            "jacket",
            "sweater",
            "coat",
            "scarf",
            "shawl",
            "sock",
            "socks",
            "shoe",
            "shoes",
            "slipper",
            "sandals",
            "bag",
            "cloth bag",
            "cotton cloth",
            "cotton",
            "wool",
            "woolen clothes",
            "curtain",
            "bedsheet",
            "bed sheet",
            "blanket",
            "towel",
            "carpet",
            "rug",
            "textile waste"
        ],

        "result": {
            "waste_name": "Textile Waste",
            "category": "Textile",
            "biodegradable": "Depends",
            "recyclable": "Depends",
            "disposal_method":
                "Donate clean and usable clothes. Damaged textiles should be sent to suitable textile collection or recycling programs where available.",
            "environmental_impact":
                "Textile waste contributes to landfill waste and the production of clothing consumes water, energy and raw materials.",
            "reuse_or_recycling":
                "Clothing can be donated, repaired, reused as cleaning material or sent to textile recycling programs.",
            "awareness_tip":
                "Repair, reuse or donate clothing before throwing it away."
        }
    }
}


# =========================================================
# NORMALIZE USER INPUT
# =========================================================

def normalize_text(text):

    text = str(text).lower().strip()

    # Remove unnecessary punctuation
    text = re.sub(r"[^a-zA-Z0-9\s\-]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text


# =========================================================
# SMART LOCAL ANALYSIS
# =========================================================

def local_waste_analysis(waste_text):

    text = normalize_text(waste_text)

    best_category = None
    best_keyword = None
    best_score = 0

    # -----------------------------------------------------
    # Search all categories
    # -----------------------------------------------------

    for category, data in WASTE_KNOWLEDGE.items():

        for keyword in data["keywords"]:

            keyword_normalized = normalize_text(keyword)

            # Exact phrase match
            if keyword_normalized in text:

                score = len(keyword_normalized.split()) * 10

                if score > best_score:
                    best_score = score
                    best_category = category
                    best_keyword = keyword

            # Individual word matching
            else:

                keyword_words = keyword_normalized.split()
                text_words = text.split()

                matching_words = sum(
                    1 for word in keyword_words
                    if word in text_words
                )

                if matching_words > 0:

                    score = matching_words * 3

                    if score > best_score:
                        best_score = score
                        best_category = category
                        best_keyword = keyword

    # -----------------------------------------------------
    # If a category was found
    # -----------------------------------------------------

    if best_category:

        result = WASTE_KNOWLEDGE[best_category]["result"].copy()

        # Make the displayed waste name more specific
        user_text = str(waste_text).strip()

        if best_keyword:
            result["waste_name"] = user_text.title()

        result["source"] = "Local Waste Intelligence"

        return result

    # -----------------------------------------------------
    # Generic intelligent fallback
    # -----------------------------------------------------

    return {
        "waste_name": str(waste_text).strip().title(),
        "category": "Other",
        "biodegradable": "Depends",
        "recyclable": "Depends",
        "disposal_method":
            "Separate this item from general waste and check local waste-management guidelines. "
            "If possible, determine whether it belongs to organic, recyclable, hazardous or e-waste collection.",
        "environmental_impact":
            "Improper waste disposal can contribute to pollution and environmental problems. "
            "Correct segregation helps improve recycling and responsible waste management.",
        "reuse_or_recycling":
            "Check whether the item can be reused, repaired, donated or sent to an appropriate recycling facility.",
        "awareness_tip":
            "Identify and segregate waste correctly before disposal.",
        "source": "Local Waste Intelligence"
    }


# =========================================================
# GEMINI AI ANALYSIS
# =========================================================

def analyze_with_gemini(waste_text):

    if client is None:
        return None

    prompt = f"""
You are an AI Waste Management and Environmental Awareness Assistant.

Analyze the following waste item:

{waste_text}

Return ONLY valid JSON.

Use exactly these fields:

{{
    "waste_name": "",
    "category": "",
    "biodegradable": "",
    "recyclable": "",
    "disposal_method": "",
    "environmental_impact": "",
    "reuse_or_recycling": "",
    "awareness_tip": ""
}}

Allowed categories:

Organic
Paper
Plastic
Glass
Metal
E-Waste
Hazardous
Textile
Other

Biodegradable must be:

Yes
No
Depends

Recyclable must be:

Yes
No
Depends

Rules:

1. Identify the waste as accurately as possible.
2. Understand common product names and packaging names.
3. If the user enters a brand or product name, identify the likely waste material.
4. Give practical disposal instructions.
5. Explain environmental impact in simple language.
6. Explain reuse or recycling possibilities.
7. Give one useful awareness recommendation.
8. Do not use Markdown.
9. Return ONLY JSON.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        result_text = response.text.strip()

        # Remove Markdown code fences
        if result_text.startswith("```json"):
            result_text = result_text[7:]

        if result_text.startswith("```"):
            result_text = result_text[3:]

        if result_text.endswith("```"):
            result_text = result_text[:-3]

        result_text = result_text.strip()

        result = json.loads(result_text)

        result["source"] = "Gemini AI"

        return result

    except Exception:

        # Any Gemini error including 429
        # will activate local fallback
        return None


# =========================================================
# MAIN ANALYSIS FUNCTION
# =========================================================

def analyze_text_waste(waste_text):

    # Make sure input exists
    if not waste_text or not str(waste_text).strip():

        return {
            "waste_name": "Unknown",
            "category": "Other",
            "biodegradable": "Depends",
            "recyclable": "Depends",
            "disposal_method":
                "Please provide a waste item for analysis.",
            "environmental_impact":
                "No waste item was provided.",
            "reuse_or_recycling":
                "No analysis available.",
            "awareness_tip":
                "Enter a waste item such as plastic bottle, paper, food waste or battery.",
            "source": "Local Waste Intelligence"
        }

    # -----------------------------------------------------
    # FIRST: TRY GEMINI AI
    # -----------------------------------------------------

    ai_result = analyze_with_gemini(waste_text)

    if ai_result:

        return ai_result

    # -----------------------------------------------------
    # SECOND: LOCAL SMART ANALYZER
    # -----------------------------------------------------

    return local_waste_analysis(waste_text)
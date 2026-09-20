import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini client
client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception:
        client = None


# ---------------------------------------------------------
# LOCAL WASTE KNOWLEDGE BASE
# ---------------------------------------------------------

WASTE_DATABASE = {

    "plastic bottle": {
        "waste_name": "Plastic Bottle",
        "category": "Plastic",
        "biodegradable": "No",
        "recyclable": "Yes",
        "disposal_method": "Empty the bottle, rinse it if possible, and place it in a recyclable waste bin.",
        "environmental_impact": "Plastic bottles can remain in the environment for a very long time and may contribute to plastic pollution.",
        "reuse_or_recycling": "The bottle can be reused for suitable purposes or sent to a recycling facility.",
        "awareness_tip": "Prefer reusable bottles instead of single-use plastic bottles."
    },

    "plastic bag": {
        "waste_name": "Plastic Bag",
        "category": "Plastic",
        "biodegradable": "No",
        "recyclable": "Depends",
        "disposal_method": "Avoid burning it. Collect clean plastic bags and send them to an appropriate plastic recycling facility.",
        "environmental_impact": "Plastic bags can pollute land and water and may harm animals.",
        "reuse_or_recycling": "Clean plastic bags may sometimes be reused or accepted by plastic recycling programs.",
        "awareness_tip": "Carry a reusable cloth bag instead of using disposable plastic bags."
    },

    "paper": {
        "waste_name": "Paper Waste",
        "category": "Paper",
        "biodegradable": "Yes",
        "recyclable": "Yes",
        "disposal_method": "Keep paper dry and place it in the paper/recyclable waste collection.",
        "environmental_impact": "Paper waste is biodegradable, but excessive paper consumption increases demand for natural resources.",
        "reuse_or_recycling": "Clean paper can be reused for notes, crafts, or sent for recycling.",
        "awareness_tip": "Use both sides of paper whenever possible."
    },

    "cardboard": {
        "waste_name": "Cardboard",
        "category": "Paper",
        "biodegradable": "Yes",
        "recyclable": "Yes",
        "disposal_method": "Flatten the cardboard and place it with recyclable paper waste.",
        "environmental_impact": "Cardboard is generally biodegradable and recyclable, but large amounts of waste increase resource consumption.",
        "reuse_or_recycling": "Cardboard boxes can be reused for storage or recycled.",
        "awareness_tip": "Reuse cardboard boxes before sending them for recycling."
    },

    "glass": {
        "waste_name": "Glass Waste",
        "category": "Glass",
        "biodegradable": "No",
        "recyclable": "Yes",
        "disposal_method": "Handle broken glass carefully and place glass in the appropriate collection container.",
        "environmental_impact": "Glass does not biodegrade easily, but it can be recycled repeatedly.",
        "reuse_or_recycling": "Glass bottles and jars can often be reused or recycled.",
        "awareness_tip": "Reuse glass containers whenever practical."
    },

    "food": {
        "waste_name": "Food Waste",
        "category": "Organic",
        "biodegradable": "Yes",
        "recyclable": "No",
        "disposal_method": "Place food waste in an organic waste or composting collection.",
        "environmental_impact": "Food waste can produce greenhouse gases when it decomposes without proper management.",
        "reuse_or_recycling": "Suitable food scraps can be composted to produce useful organic matter.",
        "awareness_tip": "Avoid wasting edible food and compost suitable food scraps."
    },

    "vegetable": {
        "waste_name": "Vegetable Waste",
        "category": "Organic",
        "biodegradable": "Yes",
        "recyclable": "No",
        "disposal_method": "Place vegetable peels and scraps in an organic waste or composting bin.",
        "environmental_impact": "Organic waste can create environmental problems when disposed of improperly, but it can also be composted.",
        "reuse_or_recycling": "Vegetable waste can be composted into nutrient-rich organic material.",
        "awareness_tip": "Compost vegetable peels instead of sending them to landfill."
    },

    "metal": {
        "waste_name": "Metal Waste",
        "category": "Metal",
        "biodegradable": "No",
        "recyclable": "Yes",
        "disposal_method": "Separate metal items and send them to a suitable recycling collection.",
        "environmental_impact": "Mining and processing metals require significant energy and natural resources.",
        "reuse_or_recycling": "Metal can often be recycled and converted into new products.",
        "awareness_tip": "Separate metal waste from general household waste."
    },

    "battery": {
        "waste_name": "Battery",
        "category": "Hazardous",
        "biodegradable": "No",
        "recyclable": "Depends",
        "disposal_method": "Do not put batteries in regular household waste. Take them to an authorized battery or e-waste collection point.",
        "environmental_impact": "Batteries may contain chemicals and metals that can contaminate soil and water if improperly disposed.",
        "reuse_or_recycling": "Used batteries should be handled through authorized recycling or collection programs.",
        "awareness_tip": "Never throw used batteries into normal household garbage."
    },

    "electronic": {
        "waste_name": "Electronic Waste",
        "category": "E-Waste",
        "biodegradable": "No",
        "recyclable": "Depends",
        "disposal_method": "Take electronic devices to an authorized e-waste collection or recycling facility.",
        "environmental_impact": "Electronic waste can contain valuable materials as well as substances that require controlled handling.",
        "reuse_or_recycling": "Working devices can be reused or refurbished, while damaged devices should go to authorized e-waste recyclers.",
        "awareness_tip": "Repair or donate working electronics before replacing them."
    },

    "cloth": {
        "waste_name": "Textile Waste",
        "category": "Textile",
        "biodegradable": "Depends",
        "recyclable": "Depends",
        "disposal_method": "Donate usable clothing and send damaged textiles to an appropriate textile collection program.",
        "environmental_impact": "Textile waste contributes to landfill waste and uses resources during production.",
        "reuse_or_recycling": "Clothes can be donated, reused as cleaning material, or sent to textile recycling programs.",
        "awareness_tip": "Donate or repair usable clothes instead of throwing them away."
    }
}


# ---------------------------------------------------------
# LOCAL FALLBACK FUNCTION
# ---------------------------------------------------------

def local_waste_analysis(text):

    text_lower = text.lower()

    # Search known waste keywords
    for keyword, result in WASTE_DATABASE.items():

        if keyword in text_lower:
            return result.copy()

    # Generic fallback
    return {
        "waste_name": text.strip().title(),
        "category": "Other",
        "biodegradable": "Depends",
        "recyclable": "Depends",
        "disposal_method": "Separate the item from general waste and check the local waste collection rules.",
        "environmental_impact": "Improper disposal of waste can contribute to pollution and environmental damage.",
        "reuse_or_recycling": "Check whether the item can be reused, repaired, donated, or sent to a suitable recycling facility.",
        "awareness_tip": "Always separate waste before disposal and follow local waste-management guidelines."
    }


# ---------------------------------------------------------
# GEMINI AI ANALYSIS
# ---------------------------------------------------------

def analyze_with_gemini(waste_text):

    if client is None:
        return None

    prompt = f"""
You are an AI Waste Management and Environmental Awareness Assistant.

Analyze this waste item:

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

Category must be one of:

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
Yes, No, or Depends

Recyclable must be:
Yes, No, or Depends

Give practical and simple information.
Do not use Markdown.
Return ONLY JSON.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown JSON fences if Gemini returns them
        if text.startswith("```json"):
            text = text[7:]

        if text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        return json.loads(text)

    except Exception as e:

        error_text = str(e)

        # Important: 429 means quota/rate limit
        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            return None

        return None


# ---------------------------------------------------------
# MAIN ANALYSIS FUNCTION
# ---------------------------------------------------------

def analyze_text_waste(waste_text):

    # First try Gemini AI
    ai_result = analyze_with_gemini(waste_text)

    if ai_result:
        ai_result["source"] = "Gemini AI"
        return ai_result

    # If Gemini fails / quota exceeded
    # use local knowledge base
    local_result = local_waste_analysis(waste_text)

    local_result["source"] = "Local Waste Intelligence"

    return local_result
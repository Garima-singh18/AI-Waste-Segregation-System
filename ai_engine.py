import os
import json
from dotenv import load_dotenv
from google import genai

# Load .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file."
    )

# Create Gemini client
client = genai.Client(api_key=API_KEY)


def analyze_text_waste(waste_text):

    prompt = f"""
You are an AI Waste Management and Environmental Awareness Assistant.

Analyze this waste item:

{waste_text}

Return ONLY valid JSON using exactly these fields:

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

Rules:

1. Identify the waste item clearly.
2. Category must be one of:
   Organic, Paper, Plastic, Glass, Metal,
   E-Waste, Hazardous, Textile, Other.

3. Biodegradable must be:
   Yes or No.

4. Recyclable must be:
   Yes, No, or Depends.

5. Give practical disposal instructions.
6. Explain environmental impact in simple language.
7. Explain possible reuse or recycling.
8. Give one useful environmental awareness tip.
9. Do not use Markdown.
10. Return ONLY JSON.
"""

    try:

        # Current Gemini Interactions API
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        result_text = interaction.output_text.strip()

        # Remove accidental markdown formatting
        if result_text.startswith("```json"):
            result_text = result_text[7:]

        if result_text.startswith("```"):
            result_text = result_text[3:]

        if result_text.endswith("```"):
            result_text = result_text[:-3]

        result_text = result_text.strip()

        result = json.loads(result_text)

        return result

    except json.JSONDecodeError:

        return {
            "error": "AI returned an invalid JSON response."
        }

    except Exception as e:

        return {
            "error": str(e)
        }
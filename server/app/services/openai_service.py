import json
from app.utils.settings import OPENAI_API_KEY, API_VERSION, API_ENDPOINT, OPENAI_MODEL
from dotenv import load_dotenv
from openai import RateLimitError, OpenAIError, AzureOpenAI
from app.utils.logger import logger
from app.utils.retry import retry_on_rate_limit, retry_on_api_error

load_dotenv()

# Configure Azure OpenAI
client = AzureOpenAI(
    api_key=OPENAI_API_KEY,
    api_version=API_VERSION,
    azure_endpoint=API_ENDPOINT,
)


@retry_on_rate_limit
@retry_on_api_error
async def parse_user_input(message: str) -> dict:
    json_template = """{
        "water_intake_ml": 0,
        "food": [
            {
                "name": "",
                "nutrition_facts": {
                    "Calories": 0,
                    "Total Fat": {"amount_g": 0.0, "daily_value_percent": 0},
                    "Saturated Fat": {"amount_g": 0.0, "daily_value_percent": 0},
                    "Trans Fat": {"amount_g": 0.0},
                    "Cholesterol": {"amount_mg": 0, "daily_value_percent": 0},
                    "Sodium": {"amount_mg": 0.0, "daily_value_percent": 0},
                    "Total Carbohydrates": {"amount_g": 0.0, "daily_value_percent": 0},
                    "Dietary Fiber": {"amount_g": 0.0, "daily_value_percent": 0},
                    "Total Sugars": {"amount_g": 0.0},
                    "Added Sugars": {"amount_g": 0.0},
                    "Protein": {"amount_g": 0.0, "daily_value_percent": 0},
                    "Vitamin D": {"amount_mcg": 0, "daily_value_percent": 0},
                    "Calcium": {"amount_mg": 0.0, "daily_value_percent": 0},
                    "Iron": {"amount_mg": 0.0, "daily_value_percent": 0},
                    "Potassium": {"amount_mg": 0.0, "daily_value_percent": 0}
                }
            }
        ],
        "activities": [
            {
                "type": "",
                "category": "",  # e.g., "cardio", "strength", "flexibility", "sports"
                "duration_minutes": 0,
                "distance_km": 0,
                "intensity_level": "",  # "low", "moderate", "high"
                "calories_burned": 0,
                "heart_rate": {
                    "average": 0,
                    "peak": 0
                },
                "sets": [  # for strength training
                    {
                        "reps": 0,
                        "weight_kg": 0,
                        "rest_seconds": 0
                    }
                ],
                "notes": "",  # for additional details
                "location": "",  # "indoor", "outdoor", specific location
                "equipment_used": [],  # list of equipment
                "mood_after": "",  # how user felt after activity
                "progress_metrics": {  # activity-specific measurements
                    "flexibility_cm": 0,
                    "max_speed_kmh": 0,
                    "average_speed_kmh": 0
                }
            }
        ],
        "skincare": [
            {
                "product_name": "",
                "category": "",  # "cleanser", "toner", "serum", "moisturizer", "sunscreen", "mask"
                "brand": "",
                "time_of_day": "",  # "morning", "evening", "both"
                "ingredients": [],
                "concerns_targeted": [],  # "acne", "aging", "pigmentation", etc.
                "application_area": "",  # "face", "neck", "full_body"
                "quantity_used": "",
                "duration_minutes": 0,
                "steps_followed": [],
                "skin_reaction": "",  # immediate skin response
                "effectiveness_rating": 0,  # 1-5 scale
                "notes": ""
            }
        ],
        "haircare": [
            {
                "treatment_type": "",  # "wash", "mask", "oil", "styling", "treatment"
                "product_name": "",
                "brand": "",
                "ingredients": [],
                "hair_concerns": [],  # "dandruff", "hair_fall", "frizz", etc.
                "duration_minutes": 0,
                "technique_used": "",
                "tools_used": [],  # "hair_dryer", "straightener", etc.
                "water_temperature": "",  # "cold", "lukewarm", "hot"
                "scalp_condition": "",
                "hair_texture_after": "",
                "effectiveness_rating": 0,
                "notes": ""
            }
        ],
        "diy": [
            {
                "recipe_name": "",
                "category": "",  # "face_mask", "hair_mask", "scrub", "pack"
                "ingredients": [
                    {
                        "name": "",
                        "quantity": "",
                        "benefits": []
                    }
                ],
                "preparation_time_minutes": 0,
                "application_time_minutes": 0,
                "target_area": "",
                "preparation_steps": [],
                "storage_info": "",
                "shelf_life_hours": 0,
                "effectiveness_rating": 0,
                "side_effects_noticed": "",
                "notes": ""
            }
        ]
    }"""

    prompt = f"""
        You are a health and nutrition assistant.

        Given a user's input, extract and estimate structured daily health data including:
        - Water Intake (in ml)
        - Activities (type, duration, distance)
        - Skincare, Haircare, DIY routines
        - Food items (with name and full detailed nutrition facts)

        Each food item should have:
        - `name` (string)
        - `nutrition_facts` (object) with all standard nutrition label values

        Important Rules:
        - If multiple food items, skincare steps, activities, or DIY routines are mentioned, log each separately in their respective lists.
        - Standardize all units: 
        - Distance → kilometers
        - Weight → kilograms
        - Water intake → milliliters
        - If quantities are not provided, intelligently estimate (e.g., 1 glass = 250ml).
        - For food items, estimate nutrition facts using general knowledge.
        - If user mentions emotions after activities (e.g., "felt great after yoga"), capture that under `mood_after`.
        - DIY treatments like "haldi pack" or "ice pack" should be added under `diy`.
        - Skincare should note product names, categories (e.g., moisturizer, cleanser), time of day (morning/evening).
        - Haircare routines (e.g., oil massage, hair mask) should include products used and techniques.


        Return the full result in this JSON structure:
        {json_template}

        Only respond with valid JSON, no extra explanation.

        User input: {message}
        """

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content
        logger.info(f"Raw response: {content}")

        # Clean the response by removing markdown formatting
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]  # Remove ```json
        if content.startswith("```"):
            content = content[3:]  # Remove ```
        if content.endswith("```"):
            content = content[:-3]  # Remove closing ```
        content = content.strip()

        logger.info(f"Cleaned response: {content}")
        parsed_content = json.loads(content)
        return parsed_content
    except RateLimitError as e:
        logger.error(f"OpenAI API Rate Limit hit: {e}")
        raise
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise Exception(f"OpenAI API error: {str(e)}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding OpenAI JSON response: {e}")
        raise Exception("Failed to parse OpenAI response.")
    except Exception as e:
        logger.error(f"Unexpected error during OpenAI call: {e}")
        raise

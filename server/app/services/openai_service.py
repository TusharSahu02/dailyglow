import openai
import os
import json
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

# Configure Azure OpenAI
client = openai.AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("API_ENDPOINT"),
)


async def parse_user_input(message: str) -> dict:
    prompt = f"""
        You are a health tracker assistant. 
        Given a user's input, extract and return a JSON with EXACTLY these fields:
        {{
            "water_intake_ml": <integer>,
            "food": [
                {{
                    "name": <string>,
                    "calories": <integer>,
                    "macros": <object or null>
                }}
            ],
            "activities": [
                {{
                    "type": <string>,
                    "duration_min": <integer or null>,
                    "distance_km": <float or null>
                }}
            ],
            "skincare": [<strings>],
            "haircare": [<strings>],
            "diy": [<strings>]
        }}

        User input: {message}
        """
    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL"),
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
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        raise Exception("Failed to parse AI response into valid JSON")
    except Exception as e:
        logger.error(f"Error parsing user input: {e}")
        raise

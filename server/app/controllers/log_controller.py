from fastapi import APIRouter, HTTPException
from app.schemas.user_input import UserInput
from app.database.connection import db
from app.services.openai_service import parse_user_input
from app.utils.logger import logger
from datetime import datetime

router = APIRouter()


@router.post("/log")
async def log_user_input(user_input: UserInput):
    try:
        structured_data = await parse_user_input(user_input.message)
        structured_data["date"] = datetime.utcnow().date().isoformat()

        result = await db.daily_logs.insert_one(structured_data)

        # Convert ObjectId to string and update structured_data
        structured_data["_id"] = str(result.inserted_id)

        # Return only one response
        return {"status": "success", "data": structured_data}
    except Exception as e:
        logger.error(f"Failed to log input: {e}")
        raise HTTPException(status_code=500, detail=str(e))

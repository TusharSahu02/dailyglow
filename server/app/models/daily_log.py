from pydantic import BaseModel
from typing import List, Optional


class FoodItem(BaseModel):
    name: str
    calories: int
    macros: Optional[dict] = None


class Activity(BaseModel):
    type: str
    duration_min: Optional[int] = None
    distance_km: Optional[float] = None


class DailyLog(BaseModel):
    user_id: str
    date: str
    water_intake_ml: int = 0
    food: List[FoodItem] = []
    activities: List[Activity] = []
    skincare: List[str] = []
    haircare: List[str] = []
    diy: List[str] = []

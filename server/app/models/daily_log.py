from pydantic import BaseModel, Field
from typing import List, Optional, Dict


# --- Food Nutrition Facts ---
class NutritionFacts(BaseModel):
    Calories: int
    Total_Fat: Dict[str, float]  # {"amount_g": 0.0, "daily_value_percent": 0}
    Saturated_Fat: Dict[str, float]
    Trans_Fat: Dict[str, float]
    Cholesterol: Dict[str, float]
    Sodium: Dict[str, float]
    Total_Carbohydrates: Dict[str, float]
    Dietary_Fiber: Dict[str, float]
    Total_Sugars: Dict[str, float]
    Added_Sugars: Dict[str, float]
    Protein: Dict[str, float]
    Vitamin_D: Dict[str, float]
    Calcium: Dict[str, float]
    Iron: Dict[str, float]
    Potassium: Dict[str, float]


class FoodItem(BaseModel):
    name: str
    nutrition_facts: NutritionFacts


# --- Activities ---
class HeartRate(BaseModel):
    average: Optional[int] = 0
    peak: Optional[int] = 0


class SetDetails(BaseModel):
    reps: Optional[int] = 0
    weight_kg: Optional[float] = 0
    rest_seconds: Optional[int] = 0


class ProgressMetrics(BaseModel):
    flexibility_cm: Optional[float] = 0
    max_speed_kmh: Optional[float] = 0
    average_speed_kmh: Optional[float] = 0


class Activity(BaseModel):
    type: str
    category: Optional[str] = ""
    duration_minutes: Optional[int] = 0
    distance_km: Optional[float] = 0
    intensity_level: Optional[str] = ""
    calories_burned: Optional[int] = 0
    heart_rate: Optional[HeartRate] = HeartRate()
    sets: Optional[List[SetDetails]] = []
    notes: Optional[str] = ""
    location: Optional[str] = ""
    equipment_used: Optional[List[str]] = []
    mood_after: Optional[str] = ""
    progress_metrics: Optional[ProgressMetrics] = ProgressMetrics()


# --- Skincare ---
class SkincareStep(BaseModel):
    product_name: str
    category: str
    brand: Optional[str] = ""
    time_of_day: Optional[str] = ""
    ingredients: Optional[List[str]] = []
    concerns_targeted: Optional[List[str]] = []
    application_area: Optional[str] = ""
    quantity_used: Optional[str] = ""
    duration_minutes: Optional[int] = 0
    steps_followed: Optional[List[str]] = []
    skin_reaction: Optional[str] = ""
    effectiveness_rating: Optional[int] = 0
    notes: Optional[str] = ""


# --- Haircare (similar to skincare) ---
class HaircareStep(BaseModel):
    treatment_type: str
    product_name: str
    brand: Optional[str] = ""
    ingredients: Optional[List[str]] = []
    hair_concerns: Optional[List[str]] = []
    duration_minutes: Optional[int] = 0
    technique_used: Optional[str] = ""
    tools_used: Optional[List[str]] = []
    water_temperature: Optional[str] = ""
    scalp_condition: Optional[str] = ""
    hair_texture_after: Optional[str] = ""
    effectiveness_rating: Optional[int] = 0
    notes: Optional[str] = ""


# --- DIY Treatments ---
class DIYIngredient(BaseModel):
    name: str
    quantity: str
    benefits: Optional[List[str]] = []


class DIYStep(BaseModel):
    recipe_name: str
    category: str
    ingredients: List[DIYIngredient]
    preparation_time_minutes: Optional[int] = 0
    application_time_minutes: Optional[int] = 0
    target_area: Optional[str] = ""
    preparation_steps: Optional[List[str]] = []
    storage_info: Optional[str] = ""
    shelf_life_hours: Optional[int] = 0
    effectiveness_rating: Optional[int] = 0
    side_effects_noticed: Optional[str] = ""
    notes: Optional[str] = ""


# --- Main Daily Log Model ---
class DailyLog(BaseModel):
    water_intake_ml: int
    food: List[FoodItem]
    activities: List[Activity]
    skincare: List[SkincareStep]
    haircare: List[HaircareStep]
    diy: List[DIYStep]

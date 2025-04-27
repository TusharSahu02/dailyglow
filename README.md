# 🌿 AI Health & Wellness Tracker

An **AI-powered Health & Wellness Tracker** built using **FastAPI (Python)** for the backend and **ReactJS (TypeScript)** for the frontend, powered by **OpenAI GPT-4o** for intelligent parsing and tracking.

This system helps users effortlessly track:
- 💧 Water Intake
- 🥗 Food & Nutrition (Calories + Macros)
- 💊 Supplements & Probiotics
- 🧘 Yoga, Walks, and Physical Activities
- ✨ Skincare, Haircare, DIY Treatments

---

## 🚀 Features

- **User Input Parsing**: Chat-like natural logging powered by OpenAI.
- **Real-Time Live Tracking**: Automatically updates dashboard after every input.
- **Structured Storage**: Saves logs to MongoDB Atlas.
- **MVC Backend Architecture**: Clean separation of Controllers, Models, Services, and Utilities.
- **Production-grade Logging**: Full error handling and logging.
- **Extensible**: Future-ready for authentication, analytics, and reminders.

---

## 🛠 Tech Stack

| Layer | Technology |
|:-----|:------------|
| Frontend | ReactJS (TypeScript) + Vite + TailwindCSS v5 |
| Backend | FastAPI + Python 3.11 |
| AI | OpenAI GPT-4o |
| Database | MongoDB Atlas |
| Infra | .env configuration, production logging |

---

## 📁 Project Structure

```
backend/
  app/
    controllers/
      log_controller.py
    models/
      daily_log.py
    services/
      openai_service.py
    database/
      connection.py
    schemas/
      user_input.py
    utils/
      logger.py
  main.py
  .env
  requirements.txt

frontend/
  src/
    components/
      TrackerForm.tsx
      TrackerLog.tsx
    api/
      api.ts
    App.tsx
  tailwind.config.js
  index.css
  vite.config.ts
  .env
```

---

## 🧩 Setup Instructions

### Backend (FastAPI)

```bash
# Navigate to backend
cd backend

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\\Scripts\\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --reload
```

✅ Make sure you create a `.env` file:

```
MONGO_URL=your-mongodb-url
OPENAI_API_KEY=your-openai-key
MOCK_OPENAI=false  # (Optional, for local mocking)
```

---

### Frontend (React + Vite + Tailwind)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
yarn install

# Start dev server
yarn dev
```

✅ Make sure you have a `.env` file in `frontend/`:

```
VITE_API_URL=http://localhost:8000
```

---

## 🧪 How to Test API in Postman

1. Set method to `POST`
2. URL: `http://localhost:8000/log`
3. Headers:
   - Content-Type: application/json
4. Body (raw JSON):

```json
{
  "user_id": "user123",
  "message": "I drank 2L water, did yoga for 30 mins, ate oatmeal."
}
```

5. Click **Send** and see structured AI response with water intake, food, activities etc. logged into MongoDB!

---

## ⚡ Development Notes

- If you exceed OpenAI quota ➔ add billing or mock OpenAI responses.
- Full **error handling** for OpenAI rate limits, authentication errors, and JSON parsing.
- Future-proof **MVC structure** with scalability in mind.
- Live updates and streak tracking planned for next versions!

---

## 📈 Future Enhancements

- 🛡️ User Authentication (JWT)
- 📊 Graphical dashboards for progress
- 🔥 WebSocket live updates
- 🌱 Habit building & daily reminders
- 🧠 Smart wellness suggestions via AI

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

> Built with 💖 to make daily health tracking easier and smarter!

---

---

# ✨ Would you like me to also prepare:
- A **fancy GitHub badge section** (Tech badges, Made with FastAPI, etc.)?
- Or a **sample LICENSE file** to go with it?

🚀 Let’s polish it fully if you want!  
Want me to? 🎯
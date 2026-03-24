from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from agent import run_agent
from database import create_database, get_all_reservations
from tools import cancel_reservation

app = FastAPI()

# ✅ Create DB on startup
create_database()

# ✅ Fix template path (important for Render)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# ✅ Static files
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


# ✅ Request model
class Message(BaseModel):
    message: str


# ✅ Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request}
    )


# ✅ Chat endpoint (AI agent)
@app.post("/chat")
async def chat(msg: Message):
    response = run_agent(msg.message)
    return {"response": response}


# ✅ Admin dashboard
@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse(
        name="admin.html",
        context={"request": request}
    )


# ✅ Get all reservations
@app.get("/reservations")
async def reservations():
    return get_all_reservations()


# ✅ Cancel reservation
@app.get("/cancel/{reservation_id}")
async def cancel(reservation_id: int):
    cancel_reservation(reservation_id)
    return {"status": "ok"}


# ✅ For Render deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
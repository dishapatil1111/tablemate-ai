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

# ✅ Create database
create_database()

# ✅ Fix paths (important for Render)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)


# ✅ Request model
class Message(BaseModel):
    message: str


# ✅ Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# ✅ Chat endpoint
@app.post("/chat")
async def chat(msg: Message):
    response = run_agent(msg.message)
    return {"response": response}


# ✅ Admin page
@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse(
        "admin.html",
        {"request": request}
    )


# ✅ Get reservations
@app.get("/reservations")
async def reservations():
    return get_all_reservations()


# ✅ Cancel reservation
@app.get("/cancel/{reservation_id}")
async def cancel(reservation_id: int):
    cancel_reservation(reservation_id)
    return {"status": "ok"}


# ✅ Run app (Render compatible)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
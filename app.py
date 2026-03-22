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

create_database()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


class Message(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(msg: Message):
    response = run_agent(msg.message)
    return {"response": response}


@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


@app.get("/reservations")
async def reservations():
    return get_all_reservations()


@app.get("/cancel/{reservation_id}")
async def cancel(reservation_id: int):
    cancel_reservation(reservation_id)
    return {"status": "ok"}


# 👇 IMPORTANT FOR RENDER
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
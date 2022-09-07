#!/usr/bin/env python3

from pathlib import Path
from fastapi import FastAPI, Request, Depends, status
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import site

app = FastAPI()

ROOT = Path(__file__).parent

templates = Jinja2Templates(directory=str(ROOT / "templates"))

app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")

token_auth_scheme = HTTPBearer()


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/personal")
def private(request: Request, token: str = Depends(token_auth_scheme)):

    result = site.utils.VerifyToken(token.credentials).verify()

    if result.get("status"):

        request.status_code = status.HTTP_400_BAD_REQUEST

    return result


@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/meme")
async def meme(request: Request):
    return templates.TemplateResponse("meme.html", {"request": request})


@app.get("/meme/{meme_id}")
async def meme_id(request: Request, meme_id: int):
    return templates.TemplateResponse("meme.html", {"request": request, "meme_id": meme_id})


@app.get("/stock")
async def stock(request: Request):
    return templates.TemplateResponse("stock.html", {"request": request})


@app.get("/fact")
async def fact(request: Request):
    return templates.TemplateResponse("fact.html", {"request": request})


@app.get("/fact/{topic}", response_class=HTMLResponse)
async def fact_topic(request: Request, topic: str):
    return templates.TemplateResponse("fact.html", {"request": request, "topic": topic})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, use_colors=True, workers=2)

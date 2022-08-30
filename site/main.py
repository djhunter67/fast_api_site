from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

ROOT = Path(__file__).parent

templates = Jinja2Templates(directory=str(ROOT / "templates"))

app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

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

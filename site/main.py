from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="site/static"), name="static")

template = Jinja2Templates(directory="site/templates")


@app.get("/")
async def root():
    return HTMLResponse(content=template.render("index.html"))


@app.get("/about")
async def about():
    return HTMLResponse(content=template.render("about.html"))


@app.get("/meme")
async def meme():
    return HTMLResponse(content=template.render("meme.html"))


@app.get("/meme/{meme_id}")
async def meme_id(meme_id: int):
    return HTMLResponse(content=template.render("meme.html"))


@app.get("/stock")
async def stock():
    return HTMLResponse(content=template.render("stock.html"))


@app.get("/fact")
async def fact():
    return HTMLResponse(content=template.render("fact.html"))


@app.get("/fact/{topic}", response_class=HTMLResponse)
async def fact_topic(request: Request, topic: str):
    return template.TemplateResponse("fact.html", {"request": request, "topic": topic})

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from app.agents.pipeline import MisinformationPipeline
from app.models import AnalyzeRequest, AnalyzeResponse, KBAddRequest

app = FastAPI(title="Hybrid Misinformation Detection")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/static")
pipeline = MisinformationPipeline()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    return pipeline.analyze(req.text)


@app.post("/api/kb/add")
def add_kb(req: KBAddRequest):
    pipeline.retriever.add_document(req.title, req.source, req.content, req.tags)
    return {"status": "added"}

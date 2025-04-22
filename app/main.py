import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.services import load_resume_data

logger = logging.getLogger(__name__)


app = FastAPI(
    title="ResQ Resume Builder",
    description="An app to generate resumes from YAML data.",
    version="0.1.0",
)

BASE_DIR = Path(__file__).resolve().parent.parent  # project root


# Handle Static Files
STATIC_DIR = BASE_DIR / "static"
if not STATIC_DIR.is_dir():
   logger.warning(f"Static directory not found at: {STATIC_DIR}.")
   raise FileNotFoundError(f"Templates directory not found: {STATIC_DIR}")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
logger.info(f"Static files mounted from: {STATIC_DIR}")

TEMPLATES_DIR = BASE_DIR / "templates"
if not TEMPLATES_DIR.is_dir():
    logger.error(f"Templates directory not found: {TEMPLATES_DIR}")
    raise FileNotFoundError(f"Templates directory not found: {TEMPLATES_DIR}")

templates = Jinja2Templates(directory=TEMPLATES_DIR)


# Routs
@app.get("/", name="view_resume")
async def get_resume(request: Request):
    logger.info("Request reived for root path ('/')")
    resume_data = load_resume_data()

    if resume_data is None:
        logger.error("Failed to load resume data")
        raise HTTPException(status_code=500, detail="Failed to load resume data")

    logger.info(f"Successfully loaded resume data: {list(resume_data.keys())}")
    return templates.TemplateResponse(
        "resume_template.html",
        {
            "request": request,
            "resume": resume_data,
        },
    )


@app.get("/health", name="health_check")
async def health_check():
    return {"status": "ok"}

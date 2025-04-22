import shutil
import logging
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from services import load_resume_data

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = PROJECT_ROOT / "templates"
STATIC_CSS_FILE = PROJECT_ROOT / "static" / "css" / "style.css"
OUTPUT_DIR = PROJECT_ROOT / "docs"
OUTPUT_FILE = OUTPUT_DIR / "index.html"
OUTPUT_CSS_DIR = OUTPUT_DIR / "css"
OUTPUT_CSS_FILE = OUTPUT_CSS_DIR / "style.css"

def save_static_resume():
    logger.info("Starting static resume export")

    logger.info("Loading resume data")
    resume_data = load_resume_data()
    if not resume_data:
        logger.error("Failed to load resume data")
        return

    try:
        logger.info(f"Ensuring output dir exists: {OUTPUT_DIR}")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensuring output css dir exists: {OUTPUT_CSS_DIR}")
        OUTPUT_CSS_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logger.error(f"Failed to create output dirs: {e}")
        return
    
    if not TEMPLATE_DIR.is_dir():
        logger.error(f"Template dir not found: {TEMPLATE_DIR}")
        return
    
    jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)
    try:
        template = jinja_env.get_template("resume_template.html")
        rendered_html = template.render(resume=resume_data, static_export=True)
    except Exception as e:
        logger.error(f"Failed to render template: {e}")
        return
    
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(rendered_html)
    except IOError as e:
        logger.error(f"Failed to write output file: {e}")
        return
    
    if not STATIC_CSS_FILE.is_file():
        logger.error(f"Static CSS file not found: {STATIC_CSS_FILE}")
        return

    try:
        shutil.copy(STATIC_CSS_FILE, OUTPUT_CSS_FILE)
    except IOError as e:
        logger.error(f"Failed to copy static CSS file: {e}")
        return
    
if __name__ == "__main__":
    save_static_resume()

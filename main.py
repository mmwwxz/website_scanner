from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from scanner import scanner, clean_url

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

FILE_DIRECTORY = "document"

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/scan")
async def perform_scan(request: Request, url: str = Form(...)):
    cleaned_url = clean_url(url)

    try:
        results, filename = scanner(cleaned_url)
        return templates.TemplateResponse("results.html", {
            "request": request,
            "results": results,
            "filename": filename
        })
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": str(e)
        })

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = filename

    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename,
                             media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    return {"error": "File not found"}

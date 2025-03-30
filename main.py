from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from router import binary, multi, segment, chatbot

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(binary.router, prefix="/binary", tags=["Binary Classification"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(multi.router, prefix="/multi", tags=["Multiclass Classification"])
app.include_router(segment.router, prefix="/segment", tags=["Image Segmentation"])


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Debugging: List all registered routes
@app.on_event("startup")
async def list_routes():
    routes = [route.path for route in app.routes]
    print("\nRegistered Routes:")
    for route in routes:
        print(route)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

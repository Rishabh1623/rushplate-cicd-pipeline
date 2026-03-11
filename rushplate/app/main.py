from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import health, restaurants, orders

app = FastAPI(title="RushPlate API", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(restaurants.router, tags=["Restaurants"])
app.include_router(orders.router, tags=["Orders"])

@app.get("/")
def serve_frontend():
    return FileResponse("app/static/index.html")

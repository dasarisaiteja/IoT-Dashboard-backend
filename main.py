from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# Import my other files
from database import create_tables
from mqtt_client import start_mqtt_client
from routers import sensor_data, alerts

# Create the app object
app = FastAPI(
    title="IoT Sensor Dashboard API",
    description="This API receives sensor data via MQTT and serves it to the frontend",
    version="1.0.0"
)

# Set up CORS so the frontend can connect
# I'm using a list for the origins
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This runs when the server starts
@app.on_event("startup")
async def startup_event():
    print("Starting up the application...")
    # Create the tables in the database
    create_tables()
    
    # Start the mqtt background task
    asyncio.create_task(start_mqtt_client())

# This runs when the server stops
@app.on_event("shutdown")
def shutdown_event():
    print("Shutting down the application...")

# Adding the routers from the other files
app.include_router(sensor_data.router, prefix="/api/sensor-data", tags=["Sensor Data"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])

# Home route
@app.get("/")
def read_root():
    # Just a simple message
    return {"message": "IoT Dashboard API is running!", "status": "ok"}
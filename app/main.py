from fastapi import FastAPI
from app.routes import client
from app.routes.ops import router as ops_router
from app.database import engine
from app.models import Base

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

# Include routers
app.include_router(client.router, prefix="/client", tags=["Client"])
app.include_router(ops_router, prefix="/ops", tags=["Ops"])  # ✅ Only this for ops

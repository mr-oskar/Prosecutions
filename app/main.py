from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import subscription_router, scan_router

app = FastAPI(
    title="System Guardian API",
    description="Professional PC Diagnostic System with Subscription Management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subscription_router)
app.include_router(scan_router)


@app.get("/")
async def root():
    return {
        "message": "System Guardian API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from neuralnexus.schemas.query_schema import QueryRequest, QueryResponse
from neuralnexus.orchestrator.router import orchestrator
from neuralnexus.config.settings import settings
from neuralnexus.utils.logger import setup_logger
from neuralnexus.event.event_bus import event_bus
from neuralnexus.memory.memory_manager import memory_manager

logger = setup_logger(__name__)

app = FastAPI(
    title="NeuralNexus",
    description="Multi-agent AI orchestration framework",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try:
        settings.validate()
        logger.info("NeuralNexus API started successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise

@app.get("/")
async def root():
    return {
        "service": "NeuralNexus",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        logger.info(f"Received query: {request.query[:50]}...")
        result = orchestrator.process_query(request.query)
        return QueryResponse(**result)
    except Exception as e:
        logger.error(f"Query processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events")
async def get_events(limit: int = 100):
    """Get event timeline"""
    try:
        events = event_bus.get_events(limit)
        return {
            "total": len(events),
            "events": events
        }
    except Exception as e:
        logger.error(f"Failed to get events: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history(limit: int = 10):
    """Get query history with tasks and results"""
    try:
        history = memory_manager.get_query_history(limit)
        return {
            "total": len(history),
            "history": history
        }
    except Exception as e:
        logger.error(f"Failed to get history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

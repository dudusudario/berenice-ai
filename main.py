"""
Main FastAPI application for Berenice AI SDR Agent.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.webhooks import router as webhooks_router
from api.dashboard import router as dashboard_router
from services.graphiti_service import graphiti_service
from config.settings import settings, validate_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting Berenice AI SDR Agent...")

    try:
        # Validate configuration
        validate_settings()
        logger.info("✅ Configuration validated")

        # Initialize Graphiti
        await graphiti_service.initialize()
        logger.info("✅ Graphiti initialized")

        logger.info(f"🚀 Application ready on http://{settings.host}:{settings.port}")
        logger.info(f"📱 Clinic: {settings.clinic_name}")
        logger.info(f"📍 Webhook URL: http://{settings.host}:{settings.port}/webhook/message")
        logger.info(f"📊 Dashboard URL: http://{settings.host}:{settings.port}/dashboard/ws")
        logger.info(f"🌐 Frontend: Open frontend/index.html or run npm start in frontend/")

    except Exception as e:
        logger.error(f"❌ Startup failed: {e}", exc_info=True)
        raise

    yield

    # Shutdown
    logger.info("Shutting down Berenice AI SDR Agent...")
    await graphiti_service.close()
    logger.info("✅ Graphiti connection closed")


# Create FastAPI application
app = FastAPI(
    title="Berenice AI - SDR Agent",
    description="AI-powered SDR agent for dental clinic using WhatsApp",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(webhooks_router)
app.include_router(dashboard_router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Berenice AI - SDR Agent",
        "version": "1.0.0",
        "clinic": settings.clinic_name,
        "status": "running",
        "endpoints": {
            "webhook": "/webhook/message",
            "health": "/webhook/health",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "berenice-ai-sdr",
        "graphiti": "connected" if graphiti_service.graphiti else "disconnected",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )

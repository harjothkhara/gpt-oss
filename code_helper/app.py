"""
Interactive Code Helper - FastAPI Web Application

A web-based interface for the Interactive Code Helper using gpt-oss-20b.
"""

import argparse
import asyncio
import logging
import os
from pathlib import Path
from typing import Dict, List

import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from code_analyzer import CodeAnalyzer, CodeAnalysisRequest, AnalysisType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Interactive Code Helper",
    description="AI-powered code learning assistant using gpt-oss-20b",
    version="1.0.0"
)

# Global analyzer instance
analyzer: CodeAnalyzer = None

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    """Initialize the code analyzer on startup."""
    global analyzer

    # Get model path from environment or command line
    model_path = os.getenv("MODEL_PATH", "gpt-oss-20b/metal/model.bin")

    if not os.path.exists(model_path):
        logger.error(f"Model file not found: {model_path}")
        raise FileNotFoundError(f"Model file not found: {model_path}")

    try:
        analyzer = CodeAnalyzer(model_path)
        logger.info("Code analyzer initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize analyzer: {e}")
        raise


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "supported_languages": analyzer.get_supported_languages() if analyzer else [],
        "analysis_types": analyzer.get_analysis_types() if analyzer else []
    })


@app.post("/analyze")
async def analyze_code(
    request: Request,
    code: str = Form(...),
    language: str = Form(...),
    analysis_type: str = Form(...),
    user_level: str = Form(default="beginner"),
    specific_question: str = Form(default="")
):
    """Analyze code and return results."""
    try:
        if not analyzer:
            raise HTTPException(status_code=500, detail="Analyzer not initialized")

        # Validate inputs
        if not code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty")

        if language not in analyzer.get_supported_languages():
            raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")

        if analysis_type not in analyzer.get_analysis_types():
            raise HTTPException(status_code=400, detail=f"Invalid analysis type: {analysis_type}")

        # Create analysis request
        analysis_request = CodeAnalysisRequest(
            code=code,
            language=language,
            analysis_type=AnalysisType(analysis_type),
            user_level=user_level,
            specific_question=specific_question if specific_question.strip() else None
        )

        # Perform analysis
        logger.info(f"Analyzing {language} code with {analysis_type} analysis")
        result = await analyzer.analyze_code(analysis_request)

        # Return JSON response for AJAX requests
        if request.headers.get("accept") == "application/json":
            return JSONResponse({
                "analysis": result.analysis,
                "suggestions": result.suggestions,
                "examples": result.examples,
                "execution_result": result.execution_result,
                "error": result.error
            })

        # Return HTML response for form submissions
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": result,
            "code": code,
            "language": language,
            "analysis_type": analysis_type,
            "user_level": user_level,
            "specific_question": specific_question,
            "supported_languages": analyzer.get_supported_languages(),
            "analysis_types": analyzer.get_analysis_types()
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "analyzer_ready": analyzer is not None,
        "model_loaded": analyzer.model is not None if analyzer else False
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Interactive Code Helper")
    parser.add_argument(
        "--model-path",
        type=str,
        default="gpt-oss-20b/metal/model.bin",
        help="Path to the gpt-oss-20b Metal model file"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind the server to"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the server to"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )

    args = parser.parse_args()

    # Set model path in environment for startup event
    os.environ["MODEL_PATH"] = args.model_path

    # Run the server
    uvicorn.run(
        "app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()

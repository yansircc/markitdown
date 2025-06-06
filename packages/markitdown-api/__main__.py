"""Main entry point for the API server."""
import uvicorn

from markitdown_api.api import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
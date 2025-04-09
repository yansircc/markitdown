from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
import requests
import io
import tempfile
import os
from markitdown import MarkItDown

app = FastAPI(title="MarkItDown API", description="Convert documents to Markdown")
md = MarkItDown(enable_plugins=True)

@app.post("/convert", response_class=PlainTextResponse)
async def convert_url(request_data: dict):
    url = request_data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    try:
        # Download file
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Save content to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name
        
        try:
            # Convert to Markdown using the file path
            result = md.convert(temp_path)
            return result.text_content
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 
from pathlib import Path
from unittest import result
from uuid import uuid4


from fastapi import FastAPI, UploadFile, File, HTTPException
from app.services.document_processor import process_document
from pydantic import BaseModel

class DocumentCreate(BaseModel):
    title: str
    description: str

app = FastAPI(
    title="DocuMind AI",
    description="A document processing API using FastAPI and DocuMind AI",
    version="0.1.0"
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def home():
    return {
        "message": "Welcome to DocuMind AI! Use the /process endpoint to process your documents.",
        "status" : "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.get("/documents")
def get_documents():
    return{
        "documents" : [
            {
                "id":1,
                "filename":"sample.txt",
                "status":"processed"
            },
            {
                "id":2,
                "filename":"report.pdf",
                "status":"pending"
            }
        ]
    }

@app.get("/documents/{document_id}")
def create_document(document_id: int):
    return {
        "document_id": document_id,
        "filename": "sample.txt"
    }

@app.get("/search")
def search_documents(limit: int=10, status: str="all"):
    return {
        "limit:": limit,
        "status": status
    }

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    extension = Path(file.filename or "").suffix.lower()

    if extension != ".txt":
        raise HTTPException(status_code=400, detail="Only .txt files are allowed.")

    content = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="The uploaded file is empty")

    stored_filename = f"{uuid4()}{extension}"

    file_path = UPLOAD_DIR / stored_filename

    try:
        file_path.write_bytes(content)

        result = process_document(str(file_path))

        return {
            "message": "File uploaded successfully",
            "original_filename": file.filename,
            "stored_filename": stored_filename,
            "size_bytes": len(content),
            "document": result
        }

    except (OSError, UnicodeDecodeError, ValueError) as error:
        file_path.unlink(missing_ok=True)

        raise HTTPException(status_code=500, detail=str(error)) from error

    finally:
        await file.close()

    

    

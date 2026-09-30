from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=1)
    parties: str = Field(..., min_length=1)
    terms: str = Field(..., min_length=1)
    dates: str = Field(..., min_length=1)


@router.post("/generate", status_code=status.HTTP_200_OK, tags=["Generation"])
def generate_document_endpoint(payload: DocumentRequest):
    if not payload.document_type.strip():
        raise HTTPException(status_code=400, detail="Document type cannot be empty.")
    if not payload.parties.strip():
        raise HTTPException(status_code=400, detail="Parties information cannot be empty.")
    if not payload.terms.strip():
        raise HTTPException(status_code=400, detail="Terms and conditions cannot be empty.")
    if not payload.dates.strip():
        raise HTTPException(status_code=400, detail="Effective date cannot be empty.")

    try:
        document_text = generator.generate_document(
            document_type=payload.document_type.strip(),
            parties=payload.parties.strip(),
            terms=payload.terms.strip(),
            dates=payload.dates.strip()
        )
        return {
            "success": True,
            "document": document_text
        }
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating document: {str(e)}")
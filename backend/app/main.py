import os
import io

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import settings

# LangSmith configuration
os.environ["LANGSMITH_TRACING"] = str(settings.langsmith_tracing).lower()
os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
os.environ["LANGSMITH_ENDPOINT"] = settings.langsmith_endpoint
os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project

from app.graph import app_graph
from app.agents.scam_agent import run_scam_agent


app = FastAPI(title="RemitGuard")


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str

def extract_text_from_image(contents: bytes) -> str:
    """
    Runs OCR on raw image bytes and returns the extracted text.

    Tesseract's location is picked up from the TESSERACT_CMD setting
    (from .env) when set — useful on Windows, or any machine where
    tesseract isn't on PATH. If it's empty, pytesseract falls back to
    whatever `tesseract` resolves to on PATH, which is the normal case
    on Linux/Mac after `apt install tesseract-ocr` / `brew install tesseract`.
    """
    from PIL import Image
    import pytesseract

    if settings.tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

    image = Image.open(io.BytesIO(contents))
    return pytesseract.image_to_string(image).strip()


def _validate_image(file: UploadFile) -> None:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file.",
        )


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "env": settings.app_env,
    }


@app.post("/chat")
def chat(request: ChatRequest):
    result = app_graph.invoke({
        "user_query": request.message,
    })

    return {
        "route": result["route"],
        "response": result["final_response"],
    }


@app.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    """
    Plain OCR utility endpoint — returns extracted text only, with no
    analysis. Kept for cases where the raw text itself is useful.
    """
    _validate_image(file)
    contents = await file.read()

    try:
        text = extract_text_from_image(contents)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")


@app.post("/analyze-screenshot")
async def analyze_screenshot(file: UploadFile = File(...)):
    """
    OCR + Scam Detector Agent, chained together.

    This is where OCR is actually wired into the multi-agent workflow:
    a user uploads a screenshot of a suspicious message or offer, we
    extract the text, and pass it straight into the Scam Detector Agent
    (which runs it against the RAG knowledge base) instead of just
    handing raw OCR text back to the user.
    """
    _validate_image(file)
    contents = await file.read()

    try:
        extracted_text = extract_text_from_image(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")

    if not extracted_text:
        raise HTTPException(
            status_code=400,
            detail="No readable text was found in that image.",
        )

    analysis = run_scam_agent(
        "The following text was extracted from a screenshot the user is "
        "unsure about (e.g. a message, offer, or advertisement). Assess "
        "whether it shows signs of being a remittance scam or an illegal "
        "channel (hundi/hawala), and explain why.\n\n"
        f"Extracted text:\n{extracted_text}"
    )

    return {
        "route": "scam",
        "extracted_text": extracted_text,
        "response": {
            "summary": analysis,
            "recommendation": "",
            "safety_warnings": [],
            "what_to_verify": [],
            "sources": [],
        },
    }

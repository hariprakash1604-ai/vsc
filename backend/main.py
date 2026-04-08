import io
import pandas as pd
from typing import Dict, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.data_processing import clean_data, generate_eda_stats
from services.ml_models import detect_anomalies, calculate_trend, forecast_neural_network
from services.nlp_engine import process_chat_query, generate_natural_language_insight
from services.reporting import generate_pdf_report
from services.database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    yield

app = FastAPI(title="Advanced Intelligent Business Analytics Platform API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Intelligent Business Analytics API (Phase 2 Component Active)"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Ingests data."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files supported.")
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        df_clean = clean_data(df)
        return {
            "status": "success",
            "columns": df_clean.columns.tolist(),
            "preview": df_clean.head(5).to_dict(orient="records"),
            "shape": df_clean.shape
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/eda")
async def get_eda(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(io.BytesIO(await file.read()))
        df_clean = clean_data(df)
        stats = generate_eda_stats(df_clean)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/anomalies/{column_name}")
async def get_anomalies(column_name: str, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(io.BytesIO(await file.read()))
        df_clean = clean_data(df)
        
        res = detect_anomalies(df_clean, column_name)
        if "error" in res:
             raise HTTPException(status_code=400, detail=res["error"])
        
        trend = calculate_trend(df_clean, column_name)
        
        # Phase 2 additions: NLG & DB Save
        nlg_insight = generate_natural_language_insight(
             column_name, 
             trend["moving_average"], 
             res["total_anomalies"]
        )
        db.save_analysis("demo", res)
        
        return {
            "anomalies": res,
            "trend": trend,
            "values": df_clean[column_name].tolist(),
            "insight": nlg_insight
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chatbot_query(req: ChatRequest):
    """Answers Natural Language Queries."""
    ans = process_chat_query(req.query)
    return {"reply": ans}

@app.post("/report/download")
async def extract_pdf_report(insights: list[str] = Form(...)): # simplified for prototype mapping
    """Generates a PDF report summary."""
    try:
        report = generate_pdf_report(insights)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

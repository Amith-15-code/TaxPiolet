from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Depends  # Add this import
from database import engine
from models import Base
from typing import Dict, List, Literal, Optional
import os
from dotenv import load_dotenv
from services import analyze_text, generate_financial_advice, generate_budget_summary, generate_spending_insights
from auth import get_current_user
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))  # Add backend directory to Python path
load_dotenv()

app = FastAPI(
    title="Personal Finance Chatbot API",
    description="API for financial guidance and analysis",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NLURequest(BaseModel):
    text: str

class GenerateRequest(BaseModel):
    question: str
    persona: Literal["student", "professional"]

class BudgetSummaryRequest(BaseModel):
    income: float
    expenses: Dict[str, float]
    savings_goal: float
    currency_symbol: str
    user_type: Literal["student", "professional"]

class Goal(BaseModel):
    name: str
    amount: float
    timeframe_months: int

class SpendingInsightsRequest(BaseModel):
    income: float
    expenses: Dict[str, float]
    savings_goal: float
    currency_symbol: str
    user_type: Literal["student", "professional"]
    goals: List[Goal]

@app.post("/nlu")
async def nlu_analysis(request: NLURequest):
    try:
        analysis = analyze_text(request.text)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
async def generate_response(request: GenerateRequest):
    try:
        response = generate_financial_advice(request.question, request.persona)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/budget-summary")
async def budget_summary(
    request: BudgetSummaryRequest, 
    user: dict = Depends(get_current_user)
):
    # Existing logic + add:
    track_feature_usage(user["sub"], "budget_summary")
@app.post("/spending-insights")
async def spending_insights(request: SpendingInsightsRequest):
    try:
        insights = generate_spending_insights(
            income=request.income,
            expenses=request.expenses,
            savings_goal=request.savings_goal,
            currency_symbol=request.currency_symbol,
            user_type=request.user_type,
            goals=[goal.dict() for goal in request.goals]
        )
        return {"insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "success": False}
    )
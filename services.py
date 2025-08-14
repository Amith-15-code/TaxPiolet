from transformers import pipeline
import os
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from typing import Dict, Any, List
import json
from database import SessionLocal
from models import UserFinancialProfile

# Initialize Hugging Face model for NLU
nlp = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Replace the current analyze_text() function with:
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load financial-specific model (add to top of file)
finbert_tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
finbert_model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
def save_user_profile(user_id: str, financial_data: dict):
    db = SessionLocal()
    try:
        profile = UserFinancialProfile(
            user_id=user_id,
            income=financial_data.get("income"),
            expenses=json.dumps(financial_data.get("expenses", {})),
            savings_goals=json.dumps(financial_data.get("goals", []))
        )
        db.add(profile)
        db.commit()
    finally:
        db.close()
def analyze_text(text: str) -> Dict[str, Any]:
    """Analyze financial text with FinBERT"""
    inputs = finbert_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = finbert_model(**inputs)
    
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return {
        "sentiment": finbert_model.config.id2label[torch.argmax(probs).item()],  # "Positive"/"Negative"/"Neutral"
        "confidence": torch.max(probs).item(),
        "financial_keywords": extract_financial_terms(text)  # New helper function
    }

def generate_financial_advice(question: str, persona: str) -> str:
    """Generate financial advice using IBM Granite model"""
    if not os.getenv("IBM_CLOUD_API_KEY"):
        return "Mock response: Consider setting aside 20% of your income for savings."
    
    model = Model(
        model_id="ibm/granite-3b-instruct",
        credentials={
            "apikey": os.getenv("IBM_CLOUD_API_KEY"),
            "url": "https://us-south.ml.cloud.ibm.com"
        },
        project_id=os.getenv("IBM_PROJECT_ID")
    )
    
    prompt = f"""
    You are a financial advisor helping a {persona}. 
    The user asks: "{question}"
    
    Provide clear, actionable advice in 3-5 bullet points.
    """
    
    response = model.generate_text(
        prompt,
        params={
            GenParams.DECODING_METHOD: "greedy",
            GenParams.MAX_NEW_TOKENS: 300,
            GenParams.MIN_NEW_TOKENS: 50,
            GenParams.TEMPERATURE: 0.7
        }
    )
    return response

def generate_budget_summary(
    income: float,
    expenses: Dict[str, float],
    savings_goal: float,
    currency_symbol: str,
    user_type: str
) -> str:
    """Generate budget summary using IBM Granite model"""
    if not os.getenv("IBM_CLOUD_API_KEY"):
        return "Mock budget summary response"
    
    model = Model(
        model_id="ibm/granite-3b-instruct",
        credentials={
            "apikey": os.getenv("IBM_CLOUD_API_KEY"),
            "url": "https://us-south.ml.cloud.ibm.com"
        },
        project_id=os.getenv("IBM_PROJECT_ID")
    )
    
    expense_items = "\n".join([f"- {category}: {currency_symbol}{amount}" for category, amount in expenses.items()])
    
    prompt = f"""
    Create a budget summary for a {user_type} with:
    - Monthly income: {currency_symbol}{income}
    - Monthly expenses:
    {expense_items}
    - Monthly savings goal: {currency_symbol}{savings_goal}
    
    Provide:
    1. Total expenses
    2. Disposable income
    3. Savings progress
    4. Top 3 expense categories
    5. 2-3 recommendations for improvement
    """
    
    response = model.generate_text(prompt)
    return response

def generate_spending_insights(
    income: float,
    expenses: Dict[str, float],
    savings_goal: float,
    currency_symbol: str,
    user_type: str,
    goals: List[Dict[str, Any]]
) -> str:
    """Generate spending insights using IBM Granite model"""
    if not os.getenv("IBM_CLOUD_API_KEY"):
        return "Mock spending insights response"
    
    model = Model(
        model_id="ibm/granite-3b-instruct",
        credentials={
            "apikey": os.getenv("IBM_CLOUD_API_KEY"),
            "url": "https://us-south.ml.cloud.ibm.com"
        },
        project_id=os.getenv("IBM_PROJECT_ID")
    )
    
    goals_text = "\n".join([f"- {goal['name']}: {currency_symbol}{goal['amount']} in {goal['timeframe_months']} months" for goal in goals])
    
    prompt = f"""
    Analyze spending patterns for a {user_type} with:
    - Monthly income: {currency_symbol}{income}
    - Monthly expenses totaling: {currency_symbol}{sum(expenses.values())}
    - Monthly savings goal: {currency_symbol}{savings_goal}
    - Financial goals:
    {goals_text}
    
    Provide:
    1. Current spending analysis
    2. Goal feasibility assessment
    3. Potential budget optimizations
    4. Timeline projections for goals
    5. Risk factors to watch
    """
    
    response = model.generate_text(prompt)
    return response
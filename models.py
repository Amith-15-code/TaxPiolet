from sqlalchemy import Column, Integer, String, Float, JSON
from database import Base  # Make sure this imports your Base from database.py

class UserFinancialProfile(Base):
    __tablename__ = "user_financial_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    income = Column(Float)
    expenses = Column(JSON)  # Stores as {category: amount}
    savings_goals = Column(JSON)
    risk_tolerance = Column(String)
from typing import Dict, Any
import json

def format_expenses(expenses: Dict[str, float], currency_symbol: str) -> str:
    """Format expenses dictionary into a readable string"""
    return "\n".join([f"- {category}: {currency_symbol}{amount:.2f}" for category, amount in expenses.items()])

def calculate_percentages(expenses: Dict[str, float], total: float) -> Dict[str, float]:
    """Calculate percentage of each expense category"""
    return {category: (amount / total) * 100 for category, amount in expenses.items()}
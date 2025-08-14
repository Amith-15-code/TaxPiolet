import streamlit as st
import requests
import json
from utils import set_background, glass_style
from visualizations import create_spending_pie_chart

# Page configuration
st.set_page_config(
    page_title="Personal Finance Chatbot",
    page_icon="💰",
    layout="wide"
)

# Set background and apply glass style
set_background("frontend/assets/background.jpg")
glass_style()

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Navigation
def navigate_to(page):
    st.session_state.page = page

# Home page
def home_page():
    st.title("Personal Finance Chatbot")
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        Get intelligent guidance for your savings, taxes, and investments
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("NLU Analysis", on_click=navigate_to, args=("nlu",), use_container_width=True)
        st.button("Q&A with Financial Advisor", on_click=navigate_to, args=("qa",), use_container_width=True)
    
    with col2:
        st.button("Budget Summary", on_click=navigate_to, args=("budget",), use_container_width=True)
        st.button("Spending Insights", on_click=navigate_to, args=("spending",), use_container_width=True)

# NLU Analysis Page
def nlu_page():
    st.title("NLU Analysis")
    st.write("Analyze the sentiment and key aspects of your financial text")
    
    example_input = {
        "text": "I'm struggling to save money each month because my rent is too high"
    }
    
    input_text = st.text_area(
        "Enter your financial text to analyze:",
        value=json.dumps(example_input, indent=2),
        height=150
    )
    
    if st.button("Analyze"):
        try:
            payload = json.loads(input_text)
            response = requests.post("http://localhost:8000/nlu", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                st.subheader("Analysis Results")
                st.json(result)
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")
    
    st.button("Back to Home", on_click=navigate_to, args=("home",))

# Q&A Page
def qa_page():
    st.title("Q&A with Financial Advisor")
    st.write("Get personalized financial advice based on your situation")
    
    example_input = {
        "question": "How can I save money while paying off student loans?",
        "persona": "student"
    }
    
    input_data = st.text_area(
        "Enter your question and persona:",
        value=json.dumps(example_input, indent=2),
        height=150
    )
    
    if st.button("Get Advice"):
        try:
            payload = json.loads(input_data)
            response = requests.post("http://localhost:8000/generate", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                st.subheader("Financial Advice")
                st.write(result["response"])
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")
    
    st.button("Back to Home", on_click=navigate_to, args=("home",))

# Budget Summary Page
def budget_page():
    st.title("Budget Summary")
    st.write("Get a detailed analysis of your income and expenses")
    
    example_input = {
        "income": 3500,
        "expenses": {
            "rent": 1200,
            "groceries": 400,
            "transportation": 200,
            "entertainment": 150,
            "utilities": 100,
            "other": 200
        },
        "savings_goal": 500,
        "currency_symbol": "$",
        "user_type": "student"
    }
    
    input_data = st.text_area(
        "Enter your budget details:",
        value=json.dumps(example_input, indent=2),
        height=300
    )
    if response.status_code == 200:
    result = response.json()
    st.subheader("Budget Summary")
    
    # Add visualization
    expenses = json.loads(input_data)["expenses"]
    st.plotly_chart(create_spending_pie_chart(expenses))
    
    st.write(result["summary"])
    if st.button("Generate Summary"):
        try:
            payload = json.loads(input_data)
            response = requests.post("http://localhost:8000/budget-summary", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                st.subheader("Budget Summary")
                st.write(result["summary"])
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")
    
    st.button("Back to Home", on_click=navigate_to, args=("home",))

# Spending Insights Page
def spending_page():
    st.title("Spending Insights")
    st.write("Get personalized insights and recommendations for your spending")
    
    example_input = {
        "income": 3500,
        "expenses": {
            "rent": 1200,
            "groceries": 400,
            "transportation": 200,
            "entertainment": 150,
            "utilities": 100,
            "other": 200
        },
        "savings_goal": 500,
        "currency_symbol": "$",
        "user_type": "student",
        "goals": [
            {
                "name": "Emergency fund",
                "amount": 5000,
                "timeframe_months": 10
            },
            {
                "name": "New laptop",
                "amount": 1200,
                "timeframe_months": 6
            }
        ]
    }
    
    input_data = st.text_area(
        "Enter your financial details and goals:",
        value=json.dumps(example_input, indent=2),
        height=350
    )
    
    if st.button("Generate Insights"):
        try:
            payload = json.loads(input_data)
            response = requests.post("http://localhost:8000/spending-insights", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                st.subheader("Spending Insights")
                st.write(result["insights"])
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")
    
    st.button("Back to Home", on_click=navigate_to, args=("home",))

# Main app router
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "nlu":
    nlu_page()
elif st.session_state.page == "qa":
    qa_page()
elif st.session_state.page == "budget":
    budget_page()
elif st.session_state.page == "spending":
    spending_page()
import streamlit as st
import requests
import datetime

# from exception.exceptions import TradingBotException
import sys

BASE_URL = "http://localhost:8000"  # Backend endpoint

st.set_page_config(
    page_title="🌍 Travel Planner Agentic Application",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("🌍 Travel Planner Agentic Application")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.header("How can I help you in planning a trip? Let me know where do you want to visit.")

# Chat input box at bottom
with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input("User Input", placeholder="e.g. Plan a trip to Goa for 5 days")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input.strip():
    try:
        # # Show user message
        # Show thinking spinner while backend processes
        with st.spinner("Bot is thinking..."):
            payload = {"query": user_input}
            response = requests.post(f"{BASE_URL}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            st.success("Trip plan generated!")

            st.markdown("## 🌍 Your AI Travel Plan")

            st.caption(
                f"Generated on {datetime.datetime.now().strftime('%d %b %Y, %H:%M')}"
            )

            st.divider()

            st.markdown(answer)

            st.divider()

            st.caption(
                "⚠️ AI-generated plan. Please verify prices, operating hours, "
                "availability, and travel requirements before your trip."
            )
        else:
            st.error(" Bot failed to respond: " + response.text)

    except Exception as e:
        raise f"The response failed due to {e}"
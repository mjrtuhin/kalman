"""
Streamlit Chat Interface for KALMAN.
"""

import streamlit as st
import requests
import json

st.set_page_config(
    page_title="KALMAN - AI Property Valuation",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 KALMAN - AI Property Valuation")
st.markdown("Ask me anything about UK property prices!")

API_URL = "http://localhost:8000/api/chat"

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("prediction"):
            st.metric(
                "Estimated Value",
                f"£{message['prediction']:,.0f}",
                delta=f"Range: £{message['confidence_low']:,.0f} - £{message['confidence_high']:,.0f}"
            )

if prompt := st.chat_input("Ask about property prices..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {"message": prompt}
                if st.session_state.conversation_id:
                    payload["conversation_id"] = st.session_state.conversation_id
                
                response = requests.post(API_URL, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if data.get("conversation_id"):
                    st.session_state.conversation_id = data["conversation_id"]
                
                st.markdown(data["message"])
                
                if data.get("prediction"):
                    st.metric(
                        "Estimated Value",
                        f"£{data['prediction']:,.0f}",
                        delta=f"Range: £{data['confidence_low']:,.0f} - £{data['confidence_high']:,.0f}"
                    )
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data["message"],
                    "prediction": data.get("prediction"),
                    "confidence_low": data.get("confidence_low"),
                    "confidence_high": data.get("confidence_high")
                })
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Make sure the backend is running: uvicorn backend.main:app --port 8000")

with st.sidebar:
    st.header("About KALMAN")
    st.markdown("""
    **Features:**
    - 🤖 AI-powered predictions
    - 💬 Natural language interface
    - 🧠 Conversation memory
    - 📊 866K training samples
    - 🎯 R² Score: 0.59
    
    **Example questions:**
    - "How much is a 3 bed house in Manchester?"
    - "What's the value of a flat in SW1?"
    - "What if I renovate the kitchen?"
    """)
    
    if st.button("Clear Conversation"):
        st.session_state.conversation_id = None
        st.session_state.messages = []
        st.rerun()

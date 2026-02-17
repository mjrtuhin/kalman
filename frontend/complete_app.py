"""
KALMAN - Complete Interface with Form AND Chat
"""

import streamlit as st
import requests

st.set_page_config(
    page_title="KALMAN - AI Property Valuation",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 KALMAN - AI Property Valuation")

API_URL = "http://localhost:8000"

tab1, tab2 = st.tabs(["📋 Simple Form", "💬 AI Chat"])

with tab1:
    st.header("Simple Property Valuation Form")
    st.markdown("Fill in the details below for an instant prediction.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        postcode = st.text_input(
            "Postcode",
            placeholder="e.g., SW1A 1AA, M1 2AB",
            help="Enter UK postcode"
        )
        
        property_type = st.selectbox(
            "Property Type",
            ["Semi-Detached", "Detached", "Terraced", "Flat"],
            help="Select property type"
        )
    
    with col2:
        tenure = st.selectbox(
            "Tenure",
            ["Freehold", "Leasehold"],
            help="Ownership type"
        )
        
        bedrooms = st.number_input(
            "Bedrooms (optional)",
            min_value=1,
            max_value=10,
            value=3,
            help="Number of bedrooms"
        )
    
    if st.button("💰 Get Valuation", type="primary", use_container_width=True):
        if not postcode:
            st.error("Please enter a postcode!")
        else:
            with st.spinner("Analyzing property..."):
                try:
                    payload = {
                        "category": "house_price",
                        "input_data": {
                            "postcode": postcode,
                            "property_type": property_type,
                            "tenure": tenure,
                            "bedrooms": bedrooms
                        }
                    }
                    
                    response = requests.post(f"{API_URL}/api/predict", json=payload, timeout=30)
                    response.raise_for_status()
                    data = response.json()
                    
                    st.success("Valuation Complete!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Low Estimate", f"£{data['confidence_low']:,.0f}")
                    with col2:
                        st.metric("Predicted Value", f"£{data['prediction']:,.0f}", delta="Best Estimate")
                    with col3:
                        st.metric("High Estimate", f"£{data['confidence_high']:,.0f}")
                    
                    st.divider()
                    st.markdown("### 🤖 AI Explanation")
                    st.info(data['explanation'])
                    
                    if data.get('metadata', {}).get('top_factors'):
                        st.markdown("### 📊 Top Value Factors")
                        for i, factor in enumerate(data['metadata']['top_factors'][:3], 1):
                            st.markdown(f"**{i}.** {factor['feature'].replace('_', ' ').title()}: {factor['importance']:.1f}% importance")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info("Make sure backend is running: uvicorn backend.main:app --port 8000")

with tab2:
    st.header("AI Chat Interface")
    st.markdown("Ask me anything about UK property prices!")
    
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("prediction"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Low", f"£{message['confidence_low']:,.0f}")
                with col2:
                    st.metric("Value", f"£{message['prediction']:,.0f}")
                with col3:
                    st.metric("High", f"£{message['confidence_high']:,.0f}")
    
    if prompt := st.chat_input("Try: 'How much is a 3 bed semi in SW1?'"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    payload = {"message": prompt}
                    if st.session_state.conversation_id:
                        payload["conversation_id"] = st.session_state.conversation_id
                    
                    response = requests.post(f"{API_URL}/api/chat", json=payload, timeout=30)
                    response.raise_for_status()
                    data = response.json()
                    
                    if data.get("conversation_id"):
                        st.session_state.conversation_id = data["conversation_id"]
                    
                    st.markdown(data["message"])
                    
                    if data.get("prediction"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Low", f"£{data['confidence_low']:,.0f}")
                        with col2:
                            st.metric("Value", f"£{data['prediction']:,.0f}")
                        with col3:
                            st.metric("High", f"£{data['confidence_high']:,.0f}")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["message"],
                        "prediction": data.get("prediction"),
                        "confidence_low": data.get("confidence_low"),
                        "confidence_high": data.get("confidence_high")
                    })
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    if st.button("🔄 Clear Chat"):
        st.session_state.conversation_id = None
        st.session_state.messages = []
        st.rerun()

with st.sidebar:
    st.header("📊 About KALMAN")
    st.markdown("""
    **Current Features:**
    - 🏠 House Price Prediction
    - 🤖 AI-powered explanations
    - 💬 Natural language chat
    - 📋 Simple form interface
    
    **Statistics:**
    - 866K training samples
    - R² Score: 0.59
    - MAE: £97K
    
    **Coming Soon:**
    - 🏢 Business viability
    - 📦 Product launch prediction
    """)
    
    st.divider()
    st.caption("Built with CatBoost + Llama 3")

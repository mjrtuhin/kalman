"""
KALMAN - Complete House Price Prediction Interface
All features, no chat complications
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="KALMAN - House Price Prediction",
    page_icon="🏠",
    layout="wide"
)

API_URL = "http://localhost:8000"

st.title("🏠 KALMAN - AI House Price Prediction")
st.markdown("**Predict UK property values using AI trained on 866,000 transactions**")

with st.sidebar:
    st.header("📊 Model Information")
    st.metric("Training Samples", "866,199")
    st.metric("R² Score", "0.59")
    st.metric("Average Error", "£97K")
    st.divider()
    st.markdown("""
    **Powered by:**
    - CatBoost ML
    - Llama 3 AI
    - 866K UK transactions
    - Real-time predictions
    """)

tab1, tab2, tab3 = st.tabs(["🔮 Predict", "📊 Model Info", "❓ Help"])

with tab1:
    st.header("Property Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Location")
        postcode = st.text_input(
            "Postcode *",
            placeholder="e.g., SW1A 1AA",
            help="UK postcode (required)"
        )
        
        town = st.text_input(
            "Town/City",
            placeholder="e.g., London",
            help="Optional - auto-detected from postcode"
        )
    
    with col2:
        st.subheader("Property Type")
        property_type = st.selectbox(
            "Type *",
            ["Semi-Detached", "Detached", "Terraced", "Flat", "Bungalow"],
            help="Property type"
        )
        
        tenure = st.selectbox(
            "Tenure *",
            ["Freehold", "Leasehold"],
            help="Ownership type"
        )
    
    with col3:
        st.subheader("Features")
        bedrooms = st.number_input(
            "Bedrooms",
            min_value=1,
            max_value=10,
            value=3,
            help="Number of bedrooms"
        )
        
        floor_area = st.number_input(
            "Floor Area (m²)",
            min_value=10,
            max_value=500,
            value=100,
            help="Total floor area"
        )
    
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        predict_btn = st.button(
            "🔮 Get AI Prediction",
            type="primary",
            use_container_width=True
        )
    
    if predict_btn:
        if not postcode:
            st.error("⚠️ Please enter a postcode!")
        else:
            with st.spinner("🤖 AI analyzing property..."):
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
                    
                    response = requests.post(
                        f"{API_URL}/api/predict",
                        json=payload,
                        timeout=30
                    )
                    response.raise_for_status()
                    data = response.json()
                    
                    st.success("✅ Prediction Complete!")
                    
                    st.divider()
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Low Estimate",
                            f"£{data['confidence_low']:,.0f}",
                            help="Lower bound of prediction"
                        )
                    
                    with col2:
                        st.metric(
                            "Predicted Value",
                            f"£{data['prediction']:,.0f}",
                            delta="Best Estimate",
                            help="Most likely value"
                        )
                    
                    with col3:
                        st.metric(
                            "High Estimate",
                            f"£{data['confidence_high']:,.0f}",
                            help="Upper bound of prediction"
                        )
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Indicator(
                        mode="gauge+number",
                        value=data['prediction'],
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Predicted Value"},
                        number={'prefix': "£", 'valueformat': ",.0f"},
                        gauge={
                            'axis': {
                                'range': [data['confidence_low'], data['confidence_high']],
                                'tickformat': ',.0f'
                            },
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [data['confidence_low'], data['prediction']], 'color': "lightgray"},
                                {'range': [data['prediction'], data['confidence_high']], 'color': "gray"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': data['prediction']
                            }
                        }
                    ))
                    
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.divider()
                    
                    st.subheader("🤖 AI Explanation")
                    st.info(data['explanation'])
                    
                    if data.get('metadata', {}).get('top_factors'):
                        st.subheader("📊 Top Value Factors")
                        
                        factors = data['metadata']['top_factors'][:5]
                        
                        df_factors = pd.DataFrame([
                            {
                                'Factor': f['feature'].replace('_', ' ').title(),
                                'Importance': f['importance']
                            }
                            for f in factors
                        ])
                        
                        fig2 = go.Figure(go.Bar(
                            x=df_factors['Importance'],
                            y=df_factors['Factor'],
                            orientation='h',
                            marker=dict(color='rgb(26, 118, 255)')
                        ))
                        
                        fig2.update_layout(
                            title="Feature Importance",
                            xaxis_title="Importance Score",
                            yaxis_title="Factor",
                            height=300
                        )
                        
                        st.plotly_chart(fig2, use_container_width=True)
                    
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend API")
                    st.info("Start backend: `uvicorn backend.main:app --port 8000`")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

with tab2:
    st.header("📊 Model Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("R² Score", "0.5855", help="Explains 58.5% of price variance")
        st.metric("Mean Absolute Error", "£97,173")
        st.metric("Training Samples", "866,199")
    
    with col2:
        st.metric("Model Type", "CatBoost")
        st.metric("Features", "12")
        st.metric("LLM", "Llama 3.2 3B")
    
    st.divider()
    
    st.subheader("Features Used")
    features = [
        "Property Type", "Postcode Sector", "Town/City",
        "County", "Tenure", "Month", "Quarter",
        "New Build Status", "Freehold Status",
        "Sector Median Price", "Town Median Price", "Property Type Median"
    ]
    
    st.write(", ".join(features))

with tab3:
    st.header("❓ How to Use")
    
    st.markdown("""
    ### Quick Start
    
    1. **Enter Postcode** (Required)
       - Format: SW1A 1AA, M1 2AB, etc.
    
    2. **Select Property Type** (Required)
       - Detached, Semi-Detached, Terraced, Flat, Bungalow
    
    3. **Choose Tenure** (Required)
       - Freehold or Leasehold
    
    4. **Add Details** (Optional)
       - Bedrooms, floor area
    
    5. **Click Predict**
       - Get instant AI prediction!
    
    ### Understanding Results
    
    - **Low/High Estimates**: ±15% confidence range
    - **AI Explanation**: Why the price is predicted
    - **Top Factors**: What affects the value most
    
    ### Example
```
    Postcode: SW1A 1AA
    Type: Semi-Detached
    Tenure: Freehold
    Bedrooms: 3
    → Prediction: £870,789
```
    """)

st.divider()
st.caption("KALMAN v1.0 | Powered by CatBoost + Llama 3 | 866K UK Property Transactions")

"""
KALMAN - House Price Prediction
Matches actual model capabilities (location + type only)
"""

import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(
    page_title="KALMAN - House Price Prediction",
    page_icon="🏠",
    layout="wide"
)

API_URL = "http://localhost:8000"

st.title("🏠 KALMAN - AI House Price Prediction")
st.markdown("**Predict UK property values using AI trained on 866,000 transactions**")

st.warning("""
⚠️ **Model Limitations**: This model predicts based on **location** and **property type** only.
It does NOT use bedrooms, floor area, or other features (not available in training data).
""")

with st.sidebar:
    st.header("📊 Model Information")
    st.metric("Training Samples", "866,199")
    st.metric("R² Score", "0.59")
    st.metric("Average Error", "£97K")
    
    st.divider()
    
    st.markdown("### Model Features")
    st.markdown("""
    **Uses:**
    - ✅ Postcode sector
    - ✅ Property type
    - ✅ Tenure
    - ✅ Location medians
    
    **Does NOT use:**
    - ❌ Bedrooms
    - ❌ Floor area
    - ❌ Bathrooms
    - ❌ Garden/parking
    """)
    
    st.divider()
    st.caption("Powered by CatBoost + Llama 3")

st.header("Property Details")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Location")
    postcode = st.text_input(
        "Postcode *",
        placeholder="e.g., SW1A 1AA, M1 2AB, B1 1AA",
        help="Required: Full UK postcode"
    )

with col2:
    st.subheader("🏠 Property Type")
    property_type = st.selectbox(
        "Type *",
        ["Semi-Detached", "Detached", "Terraced", "Flat"],
        help="Property type affects value significantly"
    )

st.subheader("📋 Ownership")
tenure = st.selectbox(
    "Tenure *",
    ["Freehold", "Leasehold"],
    help="Freehold = own land, Leasehold = rent land"
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
                        "tenure": tenure
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
                        help="Lower bound (15% below prediction)"
                    )
                
                with col2:
                    st.metric(
                        "Predicted Value",
                        f"£{data['prediction']:,.0f}",
                        delta="Best Estimate",
                        help="Most likely value based on location + type"
                    )
                
                with col3:
                    st.metric(
                        "High Estimate",
                        f"£{data['confidence_high']:,.0f}",
                        help="Upper bound (15% above prediction)"
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
                    
                    fig2 = go.Figure(go.Bar(
                        y=[f['feature'].replace('_', ' ').title() for f in factors],
                        x=[f['importance'] for f in factors],
                        orientation='h',
                        marker=dict(color='rgb(26, 118, 255)')
                    ))
                    
                    fig2.update_layout(
                        title="What Drives This Price?",
                        xaxis_title="Importance Score",
                        yaxis_title="Factor",
                        height=300
                    )
                    
                    st.plotly_chart(fig2, use_container_width=True)
                
                st.info(f"📍 Prediction based on: {postcode.upper()} + {property_type} + {tenure}")
                
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend API")
                st.code("uvicorn backend.main:app --port 8000", language="bash")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.divider()

with st.expander("ℹ️ How This Works"):
    st.markdown("""
    ### Model Capabilities
    
    This AI model predicts house prices based on:
    
    1. **Postcode Sector** (e.g., SW1, M1, B1)
       - Area median prices
       - Location desirability
       - Regional trends
    
    2. **Property Type**
       - Detached, Semi-Detached, Terraced, Flat
       - Type-specific pricing patterns
    
    3. **Tenure**
       - Freehold vs Leasehold
       - Ownership structure impact
    
    ### What It Does NOT Know
    
    - Number of bedrooms ❌
    - Floor area ❌
    - Bathrooms ❌
    - Garden/parking ❌
    - Condition ❌
    
    **Why?** The training data (Land Registry) doesn't include these features.
    
    ### Accuracy
    
    - R² Score: 0.59 (explains 59% of variance)
    - Average Error: £97K
    - Best for: Area-level estimates
    - Not for: Precise individual valuations
    
    ### Example Predictions
```
    SW1A 1AA + Semi-Detached + Freehold = £870K
    M1 2AB + Terraced + Freehold = £325K
    B1 1AA + Flat + Leasehold = £243K
```
    
    The model gives you a **location-based estimate**, similar to what you'd get
    from looking at recent sales in the area.
    """)

st.caption("KALMAN v1.0 | CatBoost ML + Llama 3 LLM | 866K UK Transactions")

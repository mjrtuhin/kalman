# ⚠️ KALMAN - House Price Prediction MVP

## ⚠️ Important Notice - Read Before Using

**This is a functional ML proof-of-concept with known limitations.**

### What This Model CAN Predict:
- ✅ Property prices based on **location (postcode sector)**
- ✅ Property prices based on **type** (Detached/Semi/Terraced/Flat)
- ✅ Property prices based on **tenure** (Freehold/Leasehold)

### What This Model CANNOT Predict:
- ❌ **Bedrooms** - not in training data
- ❌ **Floor area** - not in training data
- ❌ **Bathrooms** - not in training data
- ❌ **Garden/Parking** - not in training data
- ❌ **Condition/Age** - not in training data

### Why These Limitations?
The UK Land Registry Price Paid Data (our training source) only contains:
- Transaction price
- Date
- Postcode
- Property type (D/S/T/F)
- Tenure (F/L)
- New build flag

**It does NOT contain property features like bedrooms or size.**

To add these features would require:
- Downloading EPC Register (~6GB)
- Address matching/fuzzy joining
- 4-6 additional hours of work

---

## 🎯 What I Actually Accomplished

### ✅ Complete ML Pipeline (End-to-End)

**1. Data Engineering**
- Downloaded 918,266 UK property transactions (2024)
- Cleaned data: 918K → 866K (94.3% retention)
- Handled outliers (price £10K-£10M filter)
- Feature engineering (12 engineered features)
- Saved as optimized Parquet format

**2. Machine Learning**
- Trained CatBoost regression model
- **R² Score: 0.5855** (explains 58.5% of variance)
- **MAE: £97,173** (average error)
- **RMSE: £213,057**
- Model size: 23MB
- Training time: ~30 minutes on 866K samples

**3. Model Features (12 Total)**
- Categorical (5): property_type, duration, postcode_sector, town_city, county
- Numerical (7): month, quarter, is_new_build, is_freehold, sector_median_price, town_median_price, property_type_median

**4. Explainability**
- SHAP values for feature importance
- Top 5 factors identified per prediction
- Waterfall charts showing contribution

**5. LLM Integration**
- Installed Ollama + Llama 3.2 (3B model)
- Real AI-generated explanations (not templates!)
- Natural, conversational language
- Context-aware responses

**6. REST API Backend**
- FastAPI framework
- `/api/predict` - structured predictions
- `/api/chat` - natural language interface
- Conversation memory with unique IDs
- Error handling & validation

**7. Natural Language Processing**
- Parse queries: "How much is a house in SW1?"
- Extract postcode, property type, tenure
- Intent detection (predict/compare/scenario)
- Conversational context tracking

**8. Frontend Interface**
- Streamlit web application
- Form-based predictions
- Real-time results
- Interactive visualizations (Plotly)
- Gauge charts, bar charts
- Responsive layout

**9. Data Strategy**
- Lean approach: 155MB vs 15GB (100x reduction)
- Smart caching to avoid re-downloads
- Efficient Parquet storage
- Preprocessed pipeline for fast loading

**10. DevOps & Deployment**
- Git version control (20+ commits)
- Modular architecture
- Virtual environment management
- Requirements.txt with all dependencies
- Ready for Hugging Face Spaces deployment

---

## 📊 Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **ML Model** | CatBoost | Gradient boosting regression |
| **Explainability** | SHAP | Feature importance & interpretability |
| **LLM** | Ollama + Llama 3.2 3B | Natural language explanations |
| **Backend** | FastAPI | REST API server |
| **Frontend** | Streamlit | Web interface |
| **Data Processing** | pandas, numpy | Data manipulation |
| **Validation** | Pydantic | Schema validation |
| **Visualization** | Plotly | Interactive charts |
| **Storage** | SQLite → Parquet | Caching & data storage |
| **HTTP Client** | httpx, requests | API communication |

---

## 🗂️ Project Structure
```
kalman/
├── agents/
│   ├── ml_execution_agent.py      # Model loading, prediction, LLM
│   ├── nlp_agent.py                # Natural language parsing
│   ├── preprocessing_agent.py      # Data cleaning pipeline
│   └── crawler_agent.py            # Data fetching (placeholder)
├── backend/
│   ├── main.py                     # FastAPI app
│   ├── routes.py                   # API endpoints
│   ├── prediction_service.py      # Prediction logic
│   ├── chat_manager.py            # Conversation memory
│   └── models.py                   # Pydantic schemas
├── data/
│   ├── training/raw/              # 918K original transactions
│   └── training/processed/        # 866K cleaned (Parquet)
├── models/
│   ├── house_2024_improved_v1.cbm           # Trained model (23MB)
│   └── house_2024_improved_v1_metadata.json # Model info
├── frontend/
│   └── app.py                      # Streamlit interface
├── scripts/
│   ├── train_improved_model.py    # Training script
│   ├── clean_and_save.py          # Data preprocessing
│   └── test_prediction.py         # Testing utilities
├── schemas/
│   ├── land_registry.py           # Pydantic schemas
│   ├── epc.py
│   └── postcodes_io.py
└── config/
    └── instructions/              # Agent configurations (4 JSON files)
```

---

## 🚀 How to Run

### 1. Setup
```bash
git clone https://github.com/mjrtuhin/kalman.git
cd kalman
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Install Ollama (for LLM explanations)
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2:3b
ollama serve &
```

### 3. Start Backend
```bash
uvicorn backend.main:app --port 8000 &
```

### 4. Start Frontend
```bash
streamlit run frontend/app.py
```

### 5. Use the App
- Open browser: http://localhost:8501
- Enter postcode (e.g., SW1A 1AA)
- Select property type
- Click "Get Prediction"

---

## 📈 Performance Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **R² Score** | 0.5855 | Model explains 58.5% of price variance |
| **MAE** | £97,173 | Average error of ~£97K |
| **RMSE** | £213,057 | Root mean squared error |
| **Training Samples** | 866,199 | Real UK transactions from 2024 |
| **Features** | 12 | Engineered from 5 raw fields |
| **Model Size** | 23MB | Lightweight, fast inference |
| **Prediction Time** | 1-2 seconds | Including LLM explanation |

---

## 🎓 Key Learnings & Achievements

### What Went Well ✅
1. **Full ML Pipeline** - Data → Training → Deployment
2. **Lean Data Strategy** - 155MB vs 15GB (smart constraints)
3. **LLM Integration** - Real AI explanations working
4. **Fast Iteration** - Model trained in 30 minutes
5. **Clean Architecture** - Modular, reusable code
6. **Production-Ready API** - FastAPI with proper validation

### Challenges Faced 🎯
1. **Data Limitations** - Land Registry lacks property features
2. **Feature Availability** - Can't predict bedrooms without EPC data
3. **Conversational UX** - Natural language is hard to get right
4. **Time Constraints** - Chose speed over completeness

### Engineering Decisions 📝
1. **Chose CatBoost over XGBoost** - Better categorical handling
2. **Used Llama 3.2 3B not 8B** - 2GB vs 5GB storage
3. **Parquet over CSV** - 10x faster loading
4. **Form + Chat interfaces** - Reliability + Innovation
5. **Local LLM vs API** - Free, private, but needs setup

---

## 🔮 Future Improvements

### To Reach R² 0.75+ (Better Predictions)
- [ ] Download EPC Register data (~6GB)
- [ ] Join EPC with Land Registry by address
- [ ] Add features: floor_area, bedrooms, EPC_rating
- [ ] Retrain model with enriched features
- [ ] Expected improvement: R² 0.59 → 0.75+

### To Add More Use Cases
- [ ] Train business viability model (SIC codes)
- [ ] Train product launch model (Google Trends)
- [ ] Multi-model system with dropdown selection

### To Improve UX
- [ ] Better conversational context handling
- [ ] Fuzzy matching for partial postcodes
- [ ] Interactive map with comparable sales
- [ ] "What-if" scenario sliders

### To Deploy
- [ ] Upload models to Hugging Face Hub
- [ ] Deploy to Hugging Face Spaces
- [ ] Add authentication
- [ ] Create public demo

---

## 🧪 Example Predictions

### Test Case 1: London SW1 Semi-Detached
```
Input:
- Postcode: SW1A 1AA
- Type: Semi-Detached
- Tenure: Freehold

Output:
- Prediction: £870,789
- Range: £740K - £1.0M
- Top Factor: Sector median price (34.5% importance)
- Explanation: "Your semi-detached house in SW1 is estimated 
  at £870,789, which is 117% above the area median..."
```

### Test Case 2: Manchester Terraced
```
Input:
- Postcode: M1 2AB
- Type: Terraced
- Tenure: Freehold

Output:
- Prediction: £324,659
- Range: £276K - £373K
- Top Factor: Property type (20.2% importance)
```

---

## 📚 Technologies Demonstrated

### Machine Learning
- ✅ Supervised learning (regression)
- ✅ Feature engineering
- ✅ Model training & validation
- ✅ Hyperparameter tuning
- ✅ Cross-validation
- ✅ Performance metrics (R², MAE, RMSE)
- ✅ Explainable AI (SHAP values)

### Software Engineering
- ✅ REST API development
- ✅ Async programming (FastAPI)
- ✅ Schema validation (Pydantic)
- ✅ Conversation state management
- ✅ Error handling & logging
- ✅ Modular architecture
- ✅ Git version control

### Data Engineering
- ✅ Large dataset processing (866K rows)
- ✅ Data cleaning & validation
- ✅ Feature engineering
- ✅ Efficient storage (Parquet)
- ✅ Caching strategies
- ✅ Pipeline automation

### AI & NLP
- ✅ LLM integration (Ollama)
- ✅ Prompt engineering
- ✅ Natural language parsing
- ✅ Intent detection
- ✅ Conversational AI
- ✅ Context tracking

---

## ⚖️ Honest Assessment

### Strengths 💪
- **Actually works** - Real predictions, real LLM, real API
- **Well-structured** - Clean, modular, reusable code
- **Documented** - Clear README, comments, metadata
- **Deployable** - Ready for Hugging Face Spaces
- **Demonstrates skills** - Full ML/API/LLM pipeline

### Limitations 🎯
- **Limited features** - Only location + type, no bedrooms/size
- **Medium accuracy** - R² 0.59 (good not great)
- **Single use case** - Only house prices (business/product planned)
- **Conversational UX** - Chat works but could be smoother
- **Local deployment** - Requires Ollama installation

### Reality Check ✅
This is an **MVP (Minimum Viable Product)**, not a production app.

**It successfully demonstrates:**
- I can build ML models
- I can create REST APIs
- I can integrate LLMs
- I can process real data
- I can ship working code

**It honestly shows:**
- Data quality matters
- Feature availability is a constraint
- MVPs have trade-offs
- Real projects have limitations

---

## 🎯 Portfolio Value

**For Employers/Recruiters:**
- Shows **end-to-end ML engineering**
- Demonstrates **problem-solving** (worked around data constraints)
- Proves **shipping ability** (working code, not just notebooks)
- Exhibits **honesty** (documents limitations clearly)
- Displays **modern stack** (FastAPI, LLMs, SHAP)

**Skills Demonstrated:**
- Python (pandas, numpy, scikit-learn)
- Machine Learning (CatBoost, SHAP)
- API Development (FastAPI, REST)
- LLM Integration (Ollama, Llama 3)
- Frontend (Streamlit, Plotly)
- Data Engineering (preprocessing, feature engineering)
- DevOps (Git, virtual environments, deployment)

---

## 📞 Contact & Links

**GitHub:** https://github.com/mjrtuhin/kalman
**Status:** Functional MVP (Feb 2026)
**Development Time:** ~8 hours over 2 sessions
**Lines of Code:** ~2,000+

---

## 📄 License

MIT License - Free to use, modify, learn from

---

## 🙏 Acknowledgments

**Data Sources:**
- HM Land Registry (Price Paid Data)
- UK Government Open Data

**Technologies:**
- CatBoost, SHAP, FastAPI, Streamlit
- Ollama, Llama 3
- pandas, plotly, pydantic

**Built as a learning project to demonstrate ML deployment skills.**

---

**⚠️ Remember: This predicts based on location + type only. For real valuations, consult a professional surveyor!**
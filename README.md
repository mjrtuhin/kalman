# KALMAN - Knowledge Agents for Launch, Market & Asset Navigation

[![Status](https://img.shields.io/badge/status-under%20development-yellow)](https://github.com/mjrtuhin/kalman)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> Multi-purpose AI prediction platform for the UK market: House Prices, Business Viability, and Product Launch Success

---

## 🎯 What is KALMAN?

KALMAN is a **free, AI-powered prediction platform** designed specifically for the UK market. It uses machine learning models trained on government data to provide three types of predictions:

1. **🏠 House Price Prediction** - Estimate property values (Target: R² 0.80-0.85)
2. **💼 Business Viability Assessment** - Predict business success probability (Target: 65-75% accuracy)
3. **🚀 Product Launch Success** - Forecast market reception (Target: 60-70% accuracy)

**Key Features:**
- ✅ 100% free UK government data sources (Land Registry, Companies House, ONS, Police.uk)
- ✅ CatBoost models with SHAP explainability (GDPR Article 22 compliant)
- ✅ LLM interpretation via Ollama + Llama 3 (plain-English explanations)
- ✅ Comprehensive feature set (95+ features across all categories)
- ✅ Deployed on Hugging Face Spaces + Google Colab

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- 16GB RAM (for training models)
- 50GB disk space (for training data)

### Installation
```bash
# Clone repository
git clone https://github.com/mjrtuhin/kalman.git
cd kalman

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend API
uvicorn backend.main:app --reload --port 8000

# Run frontend (in another terminal)
streamlit run frontend/streamlit_app.py
```

Access the app at: **http://localhost:8501**

---

## 📊 Feature Overview

### 🏠 House Price Prediction (~40 Features)
- **Basic Details**: Postcode, property type, year built, tenure, lease years
- **Space**: Bedrooms, bathrooms, en-suites, reception rooms, floor area, loft, basement
- **Outdoor**: Garden (size/south-facing), parking (driveway/garage), porch, conservatory
- **Energy**: EPC rating, heating system, solar panels, insulation, double glazing
- **Condition**: Recent renovations, broadband speed, mobile signal
- **Auto-fetched**: Crime rate, school quality, flood risk, transport links

### 💼 Business Viability (~25 Features)
**15 Business Types:** Restaurants (Pakistani/Indian/Chinese), Fast Food (Chicken/Fish), Halal Butcher, Asian Grocery, Convenience Store, Clothing (Pakistani/Islamic/General), Phone Shop, Pharmacy, Barber, Hair Salon, Beauty Salon

- **Financial**: Startup budget, rent, investment, operating costs
- **Premises**: Size, visibility, parking, delivery access, opening hours
- **Experience**: Years in industry, qualifications, team size
- **Target Market**: Demographics, footfall, average spend
- **Auto-fetched**: Competitor density, sector survival rates, population data

### 🚀 Product Launch (~30 Features)
**15 Product Types:** Energy Drink, Electrolyte Drink, Protein Shake, Sparkling Water, Fruit Juice, Protein Bars, Plant-Based Meat, Ready Meals, Halal Meals, Wireless Earbuds, Bluetooth Speakers, Phone Cases, Skincare, Hair Care, Beard Care

- **Pricing**: Retail price, cost, margins, positioning (budget/premium)
- **Market**: Launch channel, geographic area, distribution partners
- **Audience**: Age groups, gender, income level, lifestyle
- **Marketing**: Budget, social media, influencers, competitors, USP
- **Attributes**: Packaging, certifications (Halal/Vegan/Organic), Made in UK
- **Auto-fetched**: Google Trends, competitor analysis, market size, seasonal patterns

---

## 🏗️ Architecture

### 5-Agent System
```
┌─────────────────────────────────────────────────────────┐
│              STREAMLIT FRONTEND                         │
│  Dropdown → Dynamic Forms → Results Display             │
└─────────────────┬───────────────────────────────────────┘
                  │ HTTP POST /api/predict
┌─────────────────▼───────────────────────────────────────┐
│              FASTAPI ORCHESTRATOR                       │
│  Loads JSON instructions → Dispatches agents           │
└──┬────────────────┬────────────────┬───────────────────┘
   │                │                │
┌──▼──────┐  ┌──────▼──────┐  ┌─────▼────────┐
│Crawler 1│  │  Crawler 2  │  │  Crawler 3   │
│(Primary)│  │ (Location)  │  │  (Market)    │
└──┬──────┘  └──────┬──────┘  └─────┬────────┘
   │                │                │
   └────────────────┼────────────────┘
                    ▼
        ┌───────────────────────┐
        │ PREPROCESSING AGENT   │
        │ Clean → Engineer      │
        └───────────┬───────────┘
                    ▼
        ┌───────────────────────┐
        │ ML EXECUTION AGENT    │
        │ Predict → SHAP → LLM  │
        └───────────────────────┘
```

**Key Design:** 3 crawlers use **identical code** with **different JSON instructions** loaded via dropdown selection.

---

## 📚 Documentation

- [**FEATURES_COMPREHENSIVE.md**](FEATURES_COMPREHENSIVE.md) - Complete feature list with data sources
- [**PROJECT_STATUS.md**](PROJECT_STATUS.md) - Current progress and next steps
- [**KALMAN_ARCHITECTURE.md**](/mnt/project/KALMAN_ARCHITECTURE.md) - Detailed system design (in project files)

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| ML Framework | CatBoost 1.2+ | Gradient boosting models |
| Explainability | SHAP 0.44+ | Feature importance |
| LLM | Ollama + Llama 3 | Plain-English interpretation |
| Backend | FastAPI 0.109+ | REST API |
| Frontend | Streamlit 1.30+ | Web interface |
| Data Processing | pandas, NumPy, scikit-learn | Data manipulation |
| Validation | Pydantic 2.5+ | Schema validation |
| Database | SQLite → PostgreSQL | Caching & storage |
| Visualization | Plotly 5.18+ | Interactive charts |

---

## 📂 Project Structure
```
kalman/
├── agents/               # 5-agent system
│   ├── crawler_agent.py       # Generic crawler
│   ├── preprocessing_agent.py # Data cleaning & features
│   └── ml_execution_agent.py  # Prediction & explanation
├── backend/              # FastAPI API
│   ├── main.py               # App entry point
│   ├── routes.py             # Endpoints
│   └── orchestrator.py       # Agent coordination
├── frontend/             # Streamlit UI
│   └── streamlit_app.py      # Complete web app
├── config/
│   ├── instructions/         # JSON configs for crawlers
│   └── features/             # Feature engineering configs
├── data/
│   ├── training/raw/         # Downloaded bulk data
│   ├── training/processed/   # Preprocessed datasets
│   └── cache/                # SQLite cache
├── models/               # Trained .cbm files
├── schemas/              # Pydantic validation
├── utils/                # Helper modules
├── scripts/              # Data download & training
├── tests/                # Unit tests
└── deployment/           # HF Spaces & Colab configs
```

---

## 🎯 Roadmap

- [x] **Week 1-2:** Setup & Data Collection ✅
  - [x] Project structure
  - [x] Backend API
  - [x] Frontend UI with 95+ features
  - [x] Utility modules
  - [x] GitHub repository
  
- [ ] **Week 2-3:** Model Training ⏳
  - [ ] Data download scripts
  - [ ] Preprocessing pipeline
  - [ ] Train CatBoost models (house, restaurant, convenience, energy drink)
  - [ ] Upload to Hugging Face Hub
  
- [ ] **Week 4:** Agent Integration
  - [ ] Instruction JSON files
  - [ ] Complete preprocessing agent
  - [ ] Complete ML execution agent
  - [ ] SHAP integration
  
- [ ] **Week 5:** LLM & Backend
  - [ ] Ollama + Llama 3 setup
  - [ ] Prompt engineering
  - [ ] Frontend-backend integration
  
- [ ] **Week 6-7:** Additional Models
  - [ ] Train remaining business models
  - [ ] Train remaining product models
  - [ ] Model evaluation & tuning
  
- [ ] **Week 8:** Deployment
  - [ ] Hugging Face Spaces deployment
  - [ ] Google Colab notebook
  - [ ] Documentation & demo video

---

## 🔬 Data Sources (100% Free)

### Houses
- HM Land Registry Price Paid Data (28M+ transactions)
- EPC Register (30M+ certificates)
- Police.uk API (crime data)
- Postcodes.io API (geocoding)
- ONS House Price Index
- Environment Agency (flood risk)
- Ofsted (school ratings)

### Business
- Companies House (bulk download + API)
- ONS Business Demography (survival rates)
- ONS Retail Sales Index
- VOA Rating List (commercial property costs)
- OpenStreetMap Overpass API (competition)

### Products
- Google Trends (pytrends library)
- Kaggle Datasets (Amazon product data)
- ONS Consumer Trends (market size)

---

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome! Please open an issue to discuss proposed changes.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 👤 Author

**Tuhin (mjrtuhin)**
- GitHub: [@mjrtuhin](https://github.com/mjrtuhin)
- Project: [kalman](https://github.com/mjrtuhin/kalman)

---

## 🙏 Acknowledgments

- UK Government Open Data (Land Registry, Companies House, ONS)
- CatBoost team for excellent documentation
- Anthropic Claude for development assistance

---

**Status:** 🚧 Under Active Development (Week 1-2 of 8)  
**Last Updated:** February 17, 2026

# KALMAN - What Actually Works

## ✅ Working Components

1. **Trained ML Model** - CatBoost on 866K transactions (R² 0.59)
2. **Backend API** - FastAPI with predictions endpoint
3. **LLM Integration** - Ollama + Llama 3 for explanations
4. **Natural Language Parsing** - Extract data from text

## ❌ Current Limitations

**Model only knows:**
- Postcode sector
- Property type (Detached/Semi/Terraced/Flat)
- Tenure (Freehold/Leasehold)

**Model CANNOT predict based on:**
- Number of bedrooms ❌
- Floor area ❌
- Garden/parking ❌
- Condition ❌

**Why:** Land Registry data doesn't include these features.

## 📊 Realistic Use Case

The model gives **area-based estimates**:
- "Semi-detached in SW1" → ~£650K
- "Flat in Manchester M1" → ~£240K

It's basically: **Location + Type = Price**

Not detailed enough for real estate but shows ML/API skills.

## 🎯 For Portfolio

**Strong points to highlight:**
- Full ML pipeline (data → training → deployment)
- REST API with FastAPI
- LLM integration (Ollama + Llama 3)
- Natural language processing
- 866K samples processed

**Honest limitation:**
- Limited features (no bedroom/size data)

## 📁 What's Committed

All code is on GitHub: https://github.com/mjrtuhin/kalman

- Backend: ✅ Working
- Model: ✅ Trained
- LLM: ✅ Integrated
- Frontend: ⚠️ Shows features model doesn't use

## 💡 To Make It Better

Would need:
1. EPC data download (~6GB)
2. Join with Land Registry by address
3. Retrain with floor_area, bedrooms
4. Would take 4-6 hours more

## Final Status

**It's a working ML system** - just more limited than originally planned.

The backend API genuinely works. The model genuinely predicts.
It just doesn't have the detailed features we wanted.

**Session time invested:** ~8 hours
**Lines of code:** 2000+
**What works:** Backend ML pipeline
**What's missing:** Detailed property features

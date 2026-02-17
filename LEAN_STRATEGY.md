# KALMAN - LEAN & POWERFUL Strategy

## 🎯 Philosophy
**Less Data, Smarter Models, Stronger Crawlers**

---

## 📊 Data Strategy

### What We Have (155MB total)
- ✅ **Land Registry 2024:** 918,266 transactions (England & Wales)
- ✅ **ONS Retail Sales:** Monthly sector data (2.4MB)

### What We'll Use Live (APIs - No Download)
- ✅ **EPC API:** Energy certificates on-demand
- ✅ **Postcodes.io API:** Geocoding (free, unlimited)
- ✅ **Police.uk API:** Crime data (free)
- ✅ **Companies House API:** Business data (600/5min free)
- ✅ **Google Trends:** Product trends (free via pytrends)

**Result:** Train on 918K transactions, predict with live data enrichment!

---

## 🤖 ML Strategy

### House Price Model
**Training Data:** 918K transactions (2024)
**Features:** 25-30 (focus on high-impact)
**Model:** CatBoost (handles missing data well)
**Target:** R² 0.75+ (realistic with focused data)

**Key Features:**
1. Property type (D/S/T/F)
2. Postcode sector (categorical)
3. Tenure (F/L)
4. Price (target)
5. **Live enrichment:** EPC rating, crime rate, schools (via APIs)

### Business Model
**Training Data:** Mock dataset (we'll generate from patterns)
**Strategy:** Rule-based + simple classifier
**Target:** 65%+ accuracy

### Product Model  
**Training Data:** Google Trends historical + retail sales
**Strategy:** Trend analysis + market size estimation
**Target:** 60%+ accuracy

---

## 🚀 Implementation Plan

### Phase 1: House Price (2-3 hours)
1. ✅ Load pp-2024.csv (918K rows)
2. Clean & filter (remove outliers, invalid postcodes)
3. Feature engineering (price_per_region, property_type encoding)
4. Train/val/test split (70/15/15)
5. Train CatBoost model
6. Save model (~50MB)

### Phase 2: Strong Crawlers (2 hours)
1. Enhance CrawlerAgent with live API calls
2. Test EPC API integration
3. Test Postcodes.io integration
4. Test Police.uk integration
5. Add caching (SQLite)

### Phase 3: Integration (2 hours)
1. Connect frontend → backend → crawlers
2. Test end-to-end prediction
3. Add SHAP values
4. Display results

**Total Time:** 6-7 hours to working demo!

---

## 💪 Strengths of This Approach

✅ **Fast:** Less data = faster training
✅ **Smart:** Live APIs give fresh data
✅ **Scalable:** Add more training data anytime
✅ **Realistic:** 918K transactions is plenty for R² 0.75+
✅ **Deployable:** Small model size, fast inference

---

**Next:** Build preprocessing script for 918K transactions!

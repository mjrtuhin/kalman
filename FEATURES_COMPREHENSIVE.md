# KALMAN - Comprehensive Features List

Based on extensive UK market research of what buyers, entrepreneurs, and product launchers actually look for.

---

## 🏠 HOUSE PRICE PREDICTION (40+ Features)

### Basic Property Details (Required)
- **Postcode** ✓ (Required)
- **Property Type** ✓ (Required): Detached, Semi-Detached, Terraced, Flat, Bungalow
- **Tenure** ✓ (Required): Freehold, Leasehold
- Year Built / Age Band
- Lease Years Remaining (if leasehold)

### Rooms & Space
- **Bedrooms** ✓ (Required): 1-10
- **Bathrooms** ✓ (Required): 1-5
- En-suite Bathrooms: 0-3
- Reception Rooms: 1-5
- **Total Floor Area (m²)** ✓
- Loft/Attic: None, Unconverted, Converted
- Basement/Cellar: Yes/No

### Outdoor Features & Parking
- **Garden**: None, Small, Medium, Large, South-Facing Large
- Garden Features: Patio, Decking, Shed, Greenhouse, Summer House
- **Parking**: None, Street, Driveway, Single Garage, Double Garage, Carport
- Other Outdoor: Porch, Conservatory, Balcony, Terrace

### Energy Efficiency & Utilities
- **EPC Rating**: Unknown, A-G
- Heating System: Gas Central, Electric, Oil, Storage Heaters
- Boiler Age (years)
- Double Glazing: None, Partial, Full, Triple Glazed
- Solar Panels: Yes/No
- Loft Insulation: Yes/No
- Wall Insulation: Yes/No

### Condition & Features
- General Condition: Excellent, Good, Fair, Needs Work
- Recent Renovations: Kitchen, Bathroom, Extension, Loft Conversion, New Roof, New Windows
- Broadband Speed: Unknown, Slow, Medium, Fast, Ultra-fast
- Mobile Signal Quality: Unknown, Poor, Fair, Good, Excellent

### Auto-Fetched Location Data (From APIs)
- Crime Rate (Police.uk)
- School Quality (Ofsted ratings)
- Distance to Nearest Station (TfL/Postcodes.io)
- Flood Risk (Environment Agency)
- Local Amenities Density
- Population Density (ONS)
- IMD (Index of Multiple Deprivation)

**Total: ~40 fields (20 user input + 20 auto-fetched)**

---

## 💼 BUSINESS VIABILITY ASSESSMENT (25+ Features)

### Business Type (Hierarchical Selection)

**Category 1: Food Service**
- Restaurants: Pakistani Restaurant, Indian Restaurant, Chinese Takeaway
- Fast Food: Fried Chicken Shop, Fish & Chips Shop

**Category 2: Retail Food**
- Specialty Food: Halal Butcher, Asian/Pakistani Grocery Store
- General: Convenience Store (Corner Shop)

**Category 3: Retail Non-Food**
- Clothing: Pakistani/Islamic Clothing Store, General Clothing Boutique
- Other: Phone/Mobile Accessories Shop, Pharmacy/Chemist

**Category 4: Services**
- Personal Care: Barber Shop (Men's), Hair Salon (Women's/Unisex), Beauty Salon

### Business & Location Details (Required)
- **Business Type** ✓ (Required)
- **Location Postcode** ✓ (Required)
- Premises Type: Standalone Shop, Shopping Center Unit, Street Front, Market Stall

### Financial Planning
- **Total Startup Budget (£)** ✓
- **Monthly Rent (£)** ✓
- Personal Investment (£)
- Loan Amount Needed (£)
- Expected Monthly Operating Costs (£)

### Premises & Operations
- Shop Size (sq ft)
- Shop Front Visibility: High, Medium, Low
- Parking Nearby: Yes/No
- Delivery/Loading Access: Yes/No
- Opening Hours
- Days Open Per Week: 1-7

### Experience & Team
- Years of Relevant Experience: 0-50
- Previous Business Ownership: Yes/No
- Industry Qualifications: Yes/No
- Planned Team Size: 1-50

### Target Market
- Target Customer Demographics: Students, Young Professionals, Families, Seniors, Tourists, Local Residents
- Expected Daily Customers
- Average Spend Per Customer (£)
- Peak Trading Hours

### Auto-Fetched Market Data (From APIs)
- Competitor Count (1km radius) - OpenStreetMap/Companies House
- Sector Survival Rates (1/3/5 year) - ONS Business Demography
- Local Population Density - ONS Census
- Demographic Breakdown - ONS
- Transport Links - Postcodes.io
- Crime Rate - Police.uk
- Commercial Property Costs - VOA Rating List

**Total: ~25 fields (15 user input + 10 auto-fetched)**

---

## 🚀 PRODUCT LAUNCH SUCCESS (30+ Features)

### Product Categories (Hierarchical Selection)

**Category 1: Food & Beverages**
- Drinks - Functional: Energy Drink, Electrolyte/Sports Drink, Protein Shake (RTD)
- Drinks - Regular: Flavored Sparkling Water, Fruit Juice (Exotic Flavors)
- Snacks: Protein/Energy Bars

**Category 2: Food - Specialty**
- Ready-to-Eat: Plant-Based Meat Alternative, Ready Meal Kits, Halal Ready Meals

**Category 3: Electronics & Accessories**
- Audio: Wireless Earbuds, Bluetooth Speakers (Portable)
- Mobile: Phone Case (New Design/Brand)

**Category 4: Personal Care**
- Beauty: Skincare Product, Hair Care Product
- Grooming: Beard Care Product

### Product Basics (Required)
- **Product Type** ✓ (Required)
- Product Name
- Product Description
- Target Launch Date

### Pricing Strategy
- **Target Retail Price (£)** ✓
- Cost to Produce (£)
- Profit Margin (%) - Auto-calculated
- Price Positioning: Budget, Mid-Range, Premium, Luxury

### Market & Distribution
- Launch Channel: Online Only, Retail Only, Both
- Target Geographic Area: Local, Regional, National
- Initial Stock Quantity
- Distribution Partners

### Target Audience
- Target Age Groups: 18-24, 25-34, 35-44, 45-54, 55+
- Target Gender: Unisex, Male, Female
- Target Income Level: Low, Middle, High
- Target Lifestyle: Students, Professionals, Athletes, Parents, Health-Conscious, Eco-Conscious

### Marketing & Competition
- Marketing Budget (£)
- Social Media Marketing Planned: Yes/No
- Influencer Marketing Planned: Yes/No
- Main Competitors (names)
- Unique Selling Point (USP)

### Product Attributes
- Packaging Type
- Shelf Life (days)
- Certifications: Halal, Vegan, Organic, Fair Trade, Gluten-Free
- Made in UK: Yes/No

### Auto-Fetched Market Data (From APIs)
- Google Trends Interest (last 12 months) - Google Trends API/pytrends
- Trend Momentum (Rising/Stable/Declining)
- Competitor Count on Amazon UK - Kaggle datasets (training data)
- Average Competitor Rating
- Average Competitor Price
- Market Size (category spending) - ONS Consumer Trends
- Seasonal Demand Pattern - Google Trends

**Total: ~30 fields (15 user input + 15 auto-fetched)**

---

## 📊 Data Source Strategy

### 100% Free Government Data Sources

**Houses:**
- HM Land Registry Price Paid Data (bulk download)
- EPC Register (bulk download)
- Police.uk API
- Postcodes.io API
- ONS House Price Index
- Environment Agency Flood Data
- Ofsted School Data
- TfL API (London)

**Business:**
- Companies House (bulk download + API)
- ONS Business Demography
- ONS Retail Sales Index
- VOA Rating List
- OpenStreetMap Overpass API
- Police.uk API
- Postcodes.io API

**Products:**
- Google Trends (pytrends library)
- Kaggle Datasets (Amazon product data for training)
- ONS Consumer Trends
- ONS Retail Sales

---

## 🎯 Next Steps

1. **Create Instruction JSON files** for each model type
2. **Build data download scripts** for training data
3. **Implement preprocessing pipeline** for feature engineering
4. **Train CatBoost models** (house, restaurant, convenience, energy drink, etc.)
5. **Integrate SHAP** for explainability
6. **Set up Ollama + Llama 3** for LLM interpretation
7. **Connect frontend to backend API**
8. **Deploy to Hugging Face Spaces**

---

**Research Sources:**
- Which? House Viewing Checklist
- Zoopla Buyer's Guide
- HomeOwners Alliance Property Checklist
- UK Restaurant Startup Guides (multiple)
- Product Launch Best Practices (Kantar, Productboard, Atlassian)

**Last Updated:** February 17, 2026

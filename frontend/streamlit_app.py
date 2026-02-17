"""
KALMAN Streamlit Frontend - Complete Feature Set
"""

import streamlit as st
import requests
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

# Page configuration
st.set_page_config(
    page_title="KALMAN - AI Prediction Platform",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 3rem;
    }
    .stExpander {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


# Category definitions
BUSINESS_CATEGORIES = {
    "Food Service": {
        "Restaurants": ["Pakistani Restaurant", "Indian Restaurant", "Chinese Takeaway"],
        "Fast Food": ["Fried Chicken Shop", "Fish & Chips Shop"]
    },
    "Retail Food": {
        "Specialty Food": ["Halal Butcher", "Asian/Pakistani Grocery Store"],
        "General": ["Convenience Store (Corner Shop)"]
    },
    "Retail Non-Food": {
        "Clothing": ["Pakistani/Islamic Clothing Store", "General Clothing Boutique"],
        "Other": ["Phone/Mobile Accessories Shop", "Pharmacy/Chemist"]
    },
    "Services": {
        "Personal Care": ["Barber Shop (Men's)", "Hair Salon (Women's/Unisex)", "Beauty Salon"]
    }
}

PRODUCT_CATEGORIES = {
    "Food & Beverages": {
        "Drinks - Functional": ["Energy Drink", "Electrolyte/Sports Drink", "Protein Shake (RTD)"],
        "Drinks - Regular": ["Flavored Sparkling Water", "Fruit Juice (Exotic Flavors)"],
        "Snacks": ["Protein/Energy Bars"]
    },
    "Food - Specialty": {
        "Ready-to-Eat": ["Plant-Based Meat Alternative", "Ready Meal Kits", "Halal Ready Meals"]
    },
    "Electronics & Accessories": {
        "Audio": ["Wireless Earbuds", "Bluetooth Speakers (Portable)"],
        "Mobile": ["Phone Case (New Design/Brand)"]
    },
    "Personal Care": {
        "Beauty": ["Skincare Product", "Hair Care Product"],
        "Grooming": ["Beard Care Product"]
    }
}


def main():
    """Main application."""
    
    # Header
    st.markdown('<div class="main-header">🔮 KALMAN</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Knowledge Agents for Launch, Market & Asset Navigation</div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📊 Prediction Type")
    category = st.sidebar.selectbox(
        "Select Category",
        ["House Price Prediction", "Business Viability Assessment", "Product Launch Success"],
        help="Choose the type of prediction you need"
    )
    
    # Main content
    if category == "House Price Prediction":
        show_house_price_form()
    elif category == "Business Viability Assessment":
        show_business_viability_form()
    elif category == "Product Launch Success":
        show_product_launch_form()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About KALMAN")
    st.sidebar.info(
        "KALMAN uses AI to predict house prices, business viability, and product launch success "
        "for the UK market using free government data sources."
    )
    st.sidebar.markdown("**Status:** 🚧 Under Development")
    st.sidebar.markdown("**GitHub:** [mjrtuhin/kalman](https://github.com/mjrtuhin/kalman)")


def show_house_price_form():
    """Display comprehensive house price prediction form."""
    
    st.header("🏠 House Price Prediction")
    st.markdown("Estimate property values based on comprehensive features and market data.")
    
    # Section 1: Basic Property Details
    with st.expander("📍 Basic Property Details", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            postcode = st.text_input(
                "Postcode *",
                placeholder="e.g., SW1A 1AA",
                help="UK postcode for the property"
            )
            
            property_type = st.selectbox(
                "Property Type *",
                ["Detached", "Semi-Detached", "Terraced", "Flat", "Bungalow"]
            )
        
        with col2:
            year_built = st.number_input(
                "Year Built",
                min_value=1700,
                max_value=2025,
                value=1990,
                help="Approximate year of construction"
            )
            
            tenure = st.selectbox("Tenure *", ["Freehold", "Leasehold"])
            
        if tenure == "Leasehold":
            lease_years = st.number_input(
                "Lease Years Remaining",
                min_value=1,
                max_value=999,
                value=99
            )
        else:
            lease_years = None
    
    # Section 2: Rooms & Space
    with st.expander("🛏️ Rooms & Space", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            bedrooms = st.number_input("Bedrooms *", min_value=1, max_value=10, value=3)
        with col2:
            bathrooms = st.number_input("Bathrooms *", min_value=1, max_value=5, value=1)
        with col3:
            ensuite = st.number_input("En-suites", min_value=0, max_value=3, value=0)
        with col4:
            reception_rooms = st.number_input("Reception Rooms", min_value=1, max_value=5, value=1)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            floor_area = st.number_input(
                "Total Floor Area (m²)",
                min_value=10.0,
                max_value=1000.0,
                value=100.0,
                step=10.0
            )
        
        with col2:
            loft = st.selectbox("Loft/Attic", ["None", "Unconverted", "Converted"])
        
        with col3:
            basement = st.checkbox("Basement/Cellar")
    
    # Section 3: Outdoor & Parking
    with st.expander("🌳 Outdoor Features & Parking"):
        col1, col2 = st.columns(2)
        
        with col1:
            garden = st.selectbox("Garden", ["None", "Small", "Medium", "Large", "South-Facing Large"])
            
            garden_features = st.multiselect(
                "Garden Features",
                ["Patio", "Decking", "Shed", "Greenhouse", "Summer House"]
            )
        
        with col2:
            parking = st.selectbox(
                "Parking",
                ["None", "Street Parking", "Driveway", "Single Garage", "Double Garage", "Carport"]
            )
            
            outdoor_features = st.multiselect(
                "Other Outdoor Features",
                ["Porch", "Conservatory", "Balcony", "Terrace"]
            )
    
    # Section 4: Energy & Utilities
    with st.expander("⚡ Energy Efficiency & Utilities"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            epc_rating = st.selectbox("EPC Rating", ["Unknown", "A", "B", "C", "D", "E", "F", "G"], index=4)
            heating_system = st.selectbox("Heating System", ["Gas Central", "Electric", "Oil", "Storage Heaters"])
        
        with col2:
            boiler_age = st.number_input("Boiler Age (years)", min_value=0, max_value=30, value=5)
            double_glazing = st.selectbox("Double Glazing", ["None", "Partial", "Full", "Triple Glazed"])
        
        with col3:
            solar_panels = st.checkbox("Solar Panels")
            loft_insulation = st.checkbox("Loft Insulation")
            wall_insulation = st.checkbox("Wall Insulation")
    
    # Section 5: Condition & Features
    with st.expander("🔧 Condition & Additional Features"):
        col1, col2 = st.columns(2)
        
        with col1:
            condition = st.selectbox(
                "General Condition",
                ["Excellent", "Good", "Fair", "Needs Work"]
            )
            
            renovations = st.multiselect(
                "Recent Renovations (last 5 years)",
                ["Kitchen", "Bathroom", "Extension", "Loft Conversion", "New Roof", "New Windows"]
            )
        
        with col2:
            broadband = st.selectbox("Broadband Speed", ["Unknown", "Slow (<10Mbps)", "Medium (10-50Mbps)", "Fast (50-100Mbps)", "Ultra-fast (100Mbps+)"])
            mobile_signal = st.selectbox("Mobile Signal Quality", ["Unknown", "Poor", "Fair", "Good", "Excellent"])
    
    st.markdown("---")
    
    if st.button("🔮 Predict House Price", type="primary", use_container_width=True):
        if not postcode:
            st.error("❌ Please enter a postcode")
        else:
            with st.spinner("Fetching data and generating prediction..."):
                predict_house_price(
                    postcode, property_type, year_built, tenure, lease_years,
                    bedrooms, bathrooms, ensuite, reception_rooms, floor_area, loft, basement,
                    garden, garden_features, parking, outdoor_features,
                    epc_rating, heating_system, boiler_age, double_glazing, solar_panels,
                    loft_insulation, wall_insulation, condition, renovations,
                    broadband, mobile_signal
                )


def show_business_viability_form():
    """Display comprehensive business viability form."""
    
    st.header("💼 Business Viability Assessment")
    st.markdown("Comprehensive assessment of your business idea's success probability.")
    
    # Section 1: Business Type
    with st.expander("🏪 Business Type & Location", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            main_category = st.selectbox("Category", list(BUSINESS_CATEGORIES.keys()))
            subcategories = BUSINESS_CATEGORIES[main_category]
            subcategory = st.selectbox("Sub-category", list(subcategories.keys()))
            business_type = st.selectbox("Specific Business Type *", subcategories[subcategory])
        
        with col2:
            location = st.text_input("Location Postcode *", placeholder="e.g., B1 1AA")
            premises_type = st.selectbox(
                "Premises Type",
                ["Standalone Shop", "Shopping Center Unit", "Street Front", "Market Stall", "Other"]
            )
    
    # Section 2: Financial Details
    with st.expander("💰 Financial Planning", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            startup_budget = st.number_input(
                "Total Startup Budget (£)",
                min_value=1000,
                max_value=1000000,
                value=50000,
                step=1000
            )
            
            monthly_rent = st.number_input(
                "Monthly Rent (£)",
                min_value=100,
                max_value=50000,
                value=2500,
                step=100
            )
            
            personal_investment = st.number_input(
                "Your Personal Investment (£)",
                min_value=0,
                max_value=1000000,
                value=20000,
                step=1000
            )
        
        with col2:
            loan_needed = st.number_input(
                "Loan Amount Needed (£)",
                min_value=0,
                max_value=1000000,
                value=30000,
                step=1000
            )
            
            monthly_operating_costs = st.number_input(
                "Expected Monthly Operating Costs (£)",
                min_value=0,
                max_value=100000,
                value=5000,
                step=500
            )
    
    # Section 3: Premises & Operations
    with st.expander("📐 Premises & Operations"):
        col1, col2 = st.columns(2)
        
        with col1:
            shop_size = st.number_input("Shop Size (sq ft)", min_value=100, max_value=10000, value=800, step=50)
            visibility = st.selectbox("Shop Front Visibility", ["High", "Medium", "Low"])
            parking = st.checkbox("Parking Nearby")
            delivery_access = st.checkbox("Delivery/Loading Access")
        
        with col2:
            opening_hours = st.text_input("Opening Hours (e.g., 9am-6pm)", value="9am-6pm")
            days_open = st.slider("Days Open Per Week", 1, 7, 6)
    
    # Section 4: Experience & Skills
    with st.expander("👤 Experience & Team"):
        col1, col2 = st.columns(2)
        
        with col1:
            experience_years = st.number_input("Years of Relevant Experience", 0, 50, 0)
            previous_business = st.checkbox("Previous Business Ownership")
            qualifications = st.checkbox("Industry Qualifications/Certifications")
        
        with col2:
            team_size = st.number_input("Planned Team Size (including you)", 1, 50, 3)
    
    # Section 5: Target Market
    with st.expander("🎯 Target Market"):
        col1, col2 = st.columns(2)
        
        with col1:
            target_demographics = st.multiselect(
                "Target Customer Demographics",
                ["Students", "Young Professionals", "Families", "Seniors", "Tourists", "Local Residents"]
            )
            daily_footfall = st.number_input("Expected Daily Customers", 10, 1000, 50)
        
        with col2:
            avg_spend = st.number_input("Average Spend Per Customer (£)", 1.0, 500.0, 10.0, step=0.5)
            peak_hours = st.text_input("Peak Trading Hours", value="12pm-2pm, 5pm-7pm")
    
    st.markdown("---")
    
    if st.button("🔮 Assess Business Viability", type="primary", use_container_width=True):
        if not location:
            st.error("❌ Please enter a location")
        else:
            with st.spinner("Analyzing market and generating assessment..."):
                predict_business_viability(
                    business_type, location, premises_type, startup_budget, monthly_rent,
                    personal_investment, loan_needed, monthly_operating_costs, shop_size,
                    visibility, parking, delivery_access, opening_hours, days_open,
                    experience_years, previous_business, qualifications, team_size,
                    target_demographics, daily_footfall, avg_spend, peak_hours
                )


def show_product_launch_form():
    """Display comprehensive product launch form."""
    
    st.header("🚀 Product Launch Success Prediction")
    st.markdown("Comprehensive market analysis for your new product.")
    
    # Section 1: Product Basics
    with st.expander("📦 Product Details", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            main_category = st.selectbox("Category", list(PRODUCT_CATEGORIES.keys()))
            subcategories = PRODUCT_CATEGORIES[main_category]
            subcategory = st.selectbox("Sub-category", list(subcategories.keys()))
            product_type = st.selectbox("Specific Product Type *", subcategories[subcategory])
        
        with col2:
            product_name = st.text_input("Product Name", placeholder="e.g., SuperEnergy Pro")
            target_launch_date = st.date_input("Target Launch Date", value=datetime.now())
        
        product_description = st.text_area(
            "Product Description (Optional)",
            placeholder="Brief description of your product...",
            height=100
        )
    
    # Section 2: Pricing & Positioning
    with st.expander("💷 Pricing Strategy", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            retail_price = st.number_input("Target Retail Price (£)", 0.5, 1000.0, 2.50, step=0.1)
            cost_to_produce = st.number_input("Cost to Produce (£)", 0.1, 500.0, 1.00, step=0.1)
        
        with col2:
            profit_margin = ((retail_price - cost_to_produce) / retail_price * 100) if retail_price > 0 else 0
            st.metric("Profit Margin", f"{profit_margin:.1f}%")
            
            price_position = st.selectbox("Price Positioning", ["Budget", "Mid-Range", "Premium", "Luxury"])
        
        with col3:
            st.info(f"**Profit Per Unit:** £{retail_price - cost_to_produce:.2f}")
    
    # Section 3: Market & Distribution
    with st.expander("🌍 Market & Distribution"):
        col1, col2 = st.columns(2)
        
        with col1:
            launch_channel = st.selectbox("Launch Channel", ["Online Only", "Retail Only", "Both Online and Retail"])
            target_area = st.selectbox("Target Geographic Area", ["Local", "Regional", "National (UK-wide)"])
            initial_stock = st.number_input("Initial Stock Quantity", 100, 100000, 1000, step=100)
        
        with col2:
            distribution_partners = st.text_input("Distribution Partners (if any)", placeholder="e.g., Amazon, Tesco")
    
    # Section 4: Target Audience
    with st.expander("🎯 Target Audience"):
        age_groups = st.multiselect(
            "Target Age Groups",
            ["18-24", "25-34", "35-44", "45-54", "55+"],
            default=["25-34"]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox("Target Gender", ["Unisex", "Male", "Female"])
            income_level = st.selectbox("Target Income Level", ["Low", "Middle", "High"])
        
        with col2:
            lifestyle = st.multiselect(
                "Target Lifestyle",
                ["Students", "Professionals", "Athletes", "Parents", "Health-Conscious", "Eco-Conscious"]
            )
    
    # Section 5: Marketing & Competition
    with st.expander("📢 Marketing & Competition"):
        col1, col2 = st.columns(2)
        
        with col1:
            marketing_budget = st.number_input("Marketing Budget (£)", 0, 100000, 5000, step=500)
            social_media = st.checkbox("Social Media Marketing Planned")
            influencer = st.checkbox("Influencer Marketing Planned")
        
        with col2:
            main_competitors = st.text_input("Main Competitors (comma-separated)", placeholder="e.g., Red Bull, Monster")
            usp = st.text_area("Unique Selling Point (USP)", placeholder="What makes your product different?", height=80)
    
    # Section 6: Product Attributes
    with st.expander("✨ Product Attributes"):
        col1, col2 = st.columns(2)
        
        with col1:
            packaging = st.text_input("Packaging Type", placeholder="e.g., Can, Bottle, Box")
            shelf_life = st.number_input("Shelf Life (days, if applicable)", 0, 365, 180)
        
        with col2:
            certifications = st.multiselect(
                "Certifications",
                ["Halal", "Vegan", "Organic", "Fair Trade", "Gluten-Free", "None"]
            )
            made_in_uk = st.checkbox("Made in UK")
    
    st.markdown("---")
    
    if st.button("🔮 Predict Launch Success", type="primary", use_container_width=True):
        with st.spinner("Analyzing market trends and competition..."):
            predict_product_launch(
                product_type, product_name, product_description, target_launch_date,
                retail_price, cost_to_produce, price_position, launch_channel,
                target_area, initial_stock, distribution_partners, age_groups,
                gender, income_level, lifestyle, marketing_budget, social_media,
                influencer, main_competitors, usp, packaging, shelf_life,
                certifications, made_in_uk
            )


# Prediction functions (simplified - will call backend API)

def predict_house_price(*args):
    """Call API for house price prediction."""
    st.info("⏳ House price prediction API integration pending...")
    st.warning("⚠️ Model training in progress. This feature will be available soon.")


def predict_business_viability(*args):
    """Call API for business viability prediction."""
    st.info("⏳ Business viability API integration pending...")
    st.warning("⚠️ Model training in progress. This feature will be available soon.")


def predict_product_launch(*args):
    """Call API for product launch prediction."""
    st.info("⏳ Product launch API integration pending...")
    st.warning("⚠️ Model training in progress. This feature will be available soon.")


if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page configuration
st.set_page_config(
    page_title="BrickValue AI | Premium Property Valuation Engine",
    page_icon="🧱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Premium Custom CSS for custom dark theme and polished UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Apply custom font */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #0f172a, #030712 70%);
    }
    
    h1, h2, h3, .section-title {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    /* Gradient Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
        border: 1px solid rgba(244, 63, 94, 0.3);
        border-radius: 28px;
        padding: 3rem 2rem;
        margin-bottom: 2.5rem;
        text-align: center;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 40px rgba(244, 63, 94, 0.05);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(244, 63, 94, 0.12) 0%, transparent 60%);
        pointer-events: none;
    }
    
    .hero-badge {
        background: rgba(244, 63, 94, 0.1);
        color: #f43f5e;
        border: 1px solid rgba(244, 63, 94, 0.3);
        padding: 0.35rem 1.2rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 1.25rem;
        box-shadow: 0 0 15px rgba(244, 63, 94, 0.1);
    }
    
    .hero-title {
        background: linear-gradient(90deg, #f43f5e 0%, #fb7185 50%, #fda4af 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.75rem !important;
        letter-spacing: -0.05em !important;
        line-height: 1.1 !important;
        text-shadow: 0 0 35px rgba(244, 63, 94, 0.15);
    }
    
    .hero-subtitle {
        color: #94a3b8 !important;
        font-size: 1.3rem !important;
        font-weight: 300 !important;
        max-width: 600px;
        margin: 0 auto !important;
        opacity: 0.9;
    }
    
    /* Premium Glassmorphic Cards */
    .prediction-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(244, 63, 94, 0.4);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), 0 0 30px rgba(244, 63, 94, 0.05) inset;
        margin: 1.5rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    .prediction-card:hover {
        transform: translateY(-5px);
        border-color: rgba(244, 63, 94, 0.7);
        box-shadow: 0 35px 65px rgba(244, 63, 94, 0.18), 0 0 30px rgba(244, 63, 94, 0.1) inset;
    }
    .prediction-label {
        color: #fb7185;
        font-size: 1.15rem;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    .prediction-value {
        font-size: 4rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        margin: 0;
        background: linear-gradient(135deg, #ffffff 40%, #ffe4e6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 35px rgba(244, 63, 94, 0.4);
    }
    .prediction-confidence {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 1.25rem;
    }
    
    /* Section Headers */
    .section-title {
        color: #f8fafc;
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #1e293b;
        padding-bottom: 0.5rem;
    }
    
    /* Valuation Slider Bar */
    .valuation-bar-container {
        width: 100%;
        background: rgba(255, 255, 255, 0.05);
        height: 10px;
        border-radius: 9999px;
        margin-top: 1.5rem;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .valuation-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #f43f5e, #fb7185);
        border-radius: 9999px;
        box-shadow: 0 0 15px rgba(244, 63, 94, 0.6);
    }
    
    /* Spec Card Grid */
    .spec-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 1rem 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .spec-card:hover {
        transform: translateY(-2px);
        border-color: rgba(244, 63, 94, 0.3);
    }
    .spec-icon {
        font-size: 1.6rem;
        background: rgba(244, 63, 94, 0.12);
        padding: 0.5rem;
        border-radius: 14px;
        color: #f43f5e;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        border: 1px solid rgba(244, 63, 94, 0.2);
    }
    .spec-details {
        display: flex;
        flex-direction: column;
    }
    .spec-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .spec-val {
        font-size: 1.1rem;
        font-weight: 600;
        color: #f1f5f9;
    }
    
    /* Driver Card */
    .driver-card {
        background: rgba(30, 41, 59, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.25rem;
        text-align: left;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        margin-bottom: 1rem;
        min-height: 120px;
    }
    .driver-title {
        font-weight: 600;
        font-size: 1rem;
        color: #f1f5f9;
        margin-bottom: 0.25rem;
    }
    .driver-desc {
        font-size: 0.85rem;
        color: #94a3b8;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# Cacheable dataset loading
@st.cache_data
def load_housing_data():
    data_path = os.path.join('data', 'Housing.csv')
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    return None

# Cacheable pipeline loading
@st.cache_resource
def load_ml_pipeline():
    try:
        model = joblib.load(os.path.join('models', 'house_price_model.joblib'))
        scaler = joblib.load(os.path.join('models', 'scaler.joblib'))
        metadata = joblib.load(os.path.join('models', 'model_metadata.joblib'))
        return model, scaler, metadata
    except Exception as e:
        try:
            # If load fails (e.g. due to scikit-learn version mismatch on remote server vs local)
            # execute train.py dynamically in this environment to generate matching joblibs.
            with open('train.py', 'r') as f:
                exec(f.read(), globals())
            model = joblib.load(os.path.join('models', 'house_price_model.joblib'))
            scaler = joblib.load(os.path.join('models', 'scaler.joblib'))
            metadata = joblib.load(os.path.join('models', 'model_metadata.joblib'))
            return model, scaler, metadata
        except Exception as retrain_err:
            st.error(f"Error loading model: {e}. Attempted auto-training but failed: {retrain_err}")
            return None, None, None

df = load_housing_data()
model, scaler, metadata = load_ml_pipeline()

# City Mock Data Dictionaries representing Indian Cities Price Levels, Locality Scores, and Distances
CITIES_DATA = {
    "Delhi": {
        "avg_price_sqft": 12000,
        "cost_tier": "High Cost",
        "badge_color": "#ef4444",
        "ratings": {"Safety": 3.8, "Schools": 4.5, "Hospitals": 4.6, "Transport": 4.7, "Shopping": 4.5},
        "facilities": [
            {"type": "Hospitals", "name": "AIIMS (Medical Science)", "dist": "2.4 km", "icon": "🏥"},
            {"type": "Schools", "name": "Delhi Public School (R.K. Puram)", "dist": "1.8 km", "icon": "🏫"},
            {"type": "Colleges", "name": "St. Stephen's College (DU)", "dist": "6.2 km", "icon": "🎓"},
            {"type": "Railway Station", "name": "New Delhi Station", "dist": "5.0 km", "icon": "🚂"},
            {"type": "Metro Station", "name": "Rajiv Chowk Metro", "dist": "1.1 km", "icon": "🚇"},
            {"type": "Bus Stand", "name": "Kashmere Gate ISBT", "dist": "7.5 km", "icon": "🚌"},
            {"type": "Airport", "name": "Indira Gandhi International Airport", "dist": "13.8 km", "icon": "✈️"},
            {"type": "Shopping Mall", "name": "Select CITYWALK Mall", "dist": "3.2 km", "icon": "🛍️"}
        ]
    },
    "Mumbai": {
        "avg_price_sqft": 19000,
        "cost_tier": "High Cost",
        "badge_color": "#ef4444",
        "ratings": {"Safety": 4.5, "Schools": 4.7, "Hospitals": 4.8, "Transport": 4.9, "Shopping": 4.8},
        "facilities": [
            {"type": "Hospitals", "name": "Kokilaben Ambani Hospital", "dist": "1.2 km", "icon": "🏥"},
            {"type": "Schools", "name": "Dhirubhai Ambani School", "dist": "2.1 km", "icon": "🏫"},
            {"type": "Colleges", "name": "St. Xavier's College", "dist": "5.4 km", "icon": "🎓"},
            {"type": "Railway Station", "name": "CST Station (CST)", "dist": "4.8 km", "icon": "🚂"},
            {"type": "Metro Station", "name": "Ghatkopar Metro Station", "dist": "1.5 km", "icon": "🚇"},
            {"type": "Bus Stand", "name": "Mumbai Central Bus Depot", "dist": "3.0 km", "icon": "🚌"},
            {"type": "Airport", "name": "Chhatrapati Shivaji Airport", "dist": "8.5 km", "icon": "✈️"},
            {"type": "Shopping Mall", "name": "Phoenix Marketcity Mall", "dist": "2.3 km", "icon": "🛍️"}
        ]
    },
    "Bengaluru": {
        "avg_price_sqft": 8000,
        "cost_tier": "High Cost",
        "badge_color": "#ef4444",
        "ratings": {"Safety": 4.3, "Schools": 4.6, "Hospitals": 4.5, "Transport": 4.1, "Shopping": 4.4},
        "facilities": [
            {"type": "Hospitals", "name": "Manipal Hospital (HAL Road)", "dist": "1.5 km", "icon": "🏥"},
            {"type": "Schools", "name": "The Valley School", "dist": "3.2 km", "icon": "🏫"},
            {"type": "Colleges", "name": "IISc Bangalore", "dist": "7.0 km", "icon": "🎓"},
            {"type": "Railway Station", "name": "KSR City Station", "dist": "6.1 km", "icon": "🚂"},
            {"type": "Metro Station", "name": "Indiranagar Metro Station", "dist": "0.9 km", "icon": "🚇"},
            {"type": "Bus Stand", "name": "Majestic Bus Station", "dist": "5.8 km", "icon": "🚌"},
            {"type": "Airport", "name": "Kempegowda Airport", "dist": "28.5 km", "icon": "✈️"},
            {"type": "Shopping Mall", "name": "Orion Mall", "dist": "4.1 km", "icon": "🛍️"}
        ]
    },
    "Hyderabad": {
        "avg_price_sqft": 7000,
        "cost_tier": "Medium Cost",
        "badge_color": "#eab308",
        "ratings": {"Safety": 4.4, "Schools": 4.4, "Hospitals": 4.5, "Transport": 4.3, "Shopping": 4.3},
        "facilities": [
            {"type": "Hospitals", "name": "Apollo Hospitals Jubilee Hills", "dist": "2.0 km", "icon": "🏥"},
            {"type": "Schools", "name": "Chirec International School", "dist": "3.5 km", "icon": "🏫"},
            {"type": "Colleges", "name": "IIIT Hyderabad", "dist": "1.8 km", "icon": "🎓"},
            {"type": "Railway Station", "name": "Secunderabad Station", "dist": "8.2 km", "icon": "🚂"},
            {"type": "Metro Station", "name": "Hitec City Metro Station", "dist": "1.2 km", "icon": "🚇"},
            {"type": "Bus Stand", "name": "MGBS Hyderabad", "dist": "9.5 km", "icon": "🚌"},
            {"type": "Airport", "name": "Rajiv Gandhi Airport", "dist": "24.0 km", "icon": "✈️"},
            {"type": "Shopping Mall", "name": "Inorbit Mall Cyberabad", "dist": "1.0 km", "icon": "🛍️"}
        ]
    },
    "Chennai": {
        "avg_price_sqft": 6500,
        "cost_tier": "Medium Cost",
        "badge_color": "#eab308",
        "ratings": {"Safety": 4.6, "Schools": 4.5, "Hospitals": 4.7, "Transport": 4.4, "Shopping": 4.2},
        "facilities": [
            {"type": "Hospitals", "name": "Fortis Malar Hospital", "dist": "1.7 km", "icon": "🏥"},
            {"type": "Schools", "name": "PSBB School Chennai", "dist": "2.5 km", "icon": "🏫"},
            {"type": "Colleges", "name": "IIT Madras", "dist": "4.1 km", "icon": "🎓"},
            {"type": "Railway Station", "name": "Chennai Central Station", "dist": "6.8 km", "icon": "🚂"},
            {"type": "Metro Station", "name": "Thirumangalam Metro Station", "dist": "1.5 km", "icon": "🚇"},
            {"type": "Bus Stand", "name": "Koyambedu CMBT", "dist": "3.5 km", "icon": "🚌"},
            {"type": "Airport", "name": "Chennai Airport", "dist": "9.2 km", "icon": "✈️"},
            {"type": "Shopping Mall", "name": "Express Avenue Mall", "dist": "5.0 km", "icon": "🛍️"}
        ]
    },
    "Kolkata": {
        "avg_price_sqft": 5500,
        "cost_tier": "Low Cost",
        "badge_color": "#22c55e",
        "ratings": {"Safety": 4.4, "Schools": 4.3, "Hospitals": 4.4, "Transport": 4.6, "Shopping": 4.1},
        "facilities": [
            {"type": "Hospitals", "name": "AMRI Hospital Salt Lake", "dist": "1.4 km", "icon": "🏥"},
            {"type": "Schools", "name": "La Martiniere for Boys", "dist": "4.2 km", "icon": "🏫"},
            {"type": "Colleges", "name": "Presidency University", "dist": "5.1 km", "icon": "🎓"},
            {"type": "Railway Station", "name": "Howrah Station", "dist": "7.5 km", "icon": "🚂"},
            {"type": "Metro Station", "name": "Sector V Metro", "dist": "0.8 km", "icon": "🚇"},
            {"type": "Bus Stand", "name": "Esplanade Terminus", "dist": "6.0 km", "icon": "🚌"},
            {"type": "Airport", "name": "Netaji Subhash Airport", "dist": "11.5 km", "icon": "✈️"},
            {"type": "Shopping Mall", "name": "South City Mall", "dist": "5.3 km", "icon": "🛍️"}
        ]
    },
    "Pune": {
        "avg_price_sqft": 6800,
        "cost_tier": "Medium Cost",
        "badge_color": "#eab308",
        "ratings": {"Safety": 4.5, "Schools": 4.4, "Hospitals": 4.3, "Transport": 4.0, "Shopping": 4.3},
        "facilities": [
            {"type": "Hospitals", "name": "Ruby Hall Clinic", "dist": "2.8 km", "icon": "🏥"},
            {"type": "Schools", "name": "Bishop's School", "dist": "1.6 km", "icon": "🏫"},
            {"type": "Colleges", "name": "Fergusson College", "dist": "4.5 km", "icon": "🎓"},
            {"type": "Railway Station", "name": "Pune Junction Station", "dist": "3.2 km", "icon": "🚂"},
            {"type": "Metro Station", "name": "Garware College Metro", "dist": "2.0 km", "icon": "🚇"},
            {"type": "Bus Stand", "name": "Swargate Bus Stand", "dist": "5.1 km", "icon": "🚌"},
            {"type": "Airport", "name": "Pune Airport", "dist": "7.8 km", "icon": "✈️"},
            {"type": "Shopping Mall", "name": "Phoenix Marketcity", "dist": "2.5 km", "icon": "🛍️"}
        ]
    },
    "Ahmedabad": {
        "avg_price_sqft": 4800,
        "cost_tier": "Low Cost",
        "badge_color": "#22c55e",
        "ratings": {"Safety": 4.7, "Schools": 4.2, "Hospitals": 4.4, "Transport": 4.2, "Shopping": 4.3},
        "facilities": [
            {"type": "Hospitals", "name": "Zydus Hospital", "dist": "2.5 km", "icon": "🏥"},
            {"type": "Schools", "name": "Adani Vidya Mandir", "dist": "4.0 km", "icon": "🏫"},
            {"type": "Colleges", "name": "IIM Ahmedabad", "dist": "3.8 km", "icon": "🎓"},
            {"type": "Railway Station", "name": "Ahmedabad Station", "dist": "6.2 km", "icon": "🚂"},
            {"type": "Metro Station", "name": "Kalupur Metro Station", "dist": "6.0 km", "icon": "🚇"},
            {"type": "Bus Stand", "name": "Gita Mandir Bus Port", "dist": "5.2 km", "icon": "🚌"},
            {"type": "Airport", "name": "Sardar Vallabhbhai Airport", "dist": "8.0 km", "icon": "✈️"},
            {"type": "Shopping Mall", "name": "Alpha One Mall", "dist": "3.0 km", "icon": "🛍️"}
        ]
    },
    "Lucknow": {
        "avg_price_sqft": 4200,
        "cost_tier": "Low Cost",
        "badge_color": "#22c55e",
        "ratings": {"Safety": 4.1, "Schools": 4.1, "Hospitals": 4.2, "Transport": 4.3, "Shopping": 4.2},
        "facilities": [
            {"type": "Hospitals", "name": "Medanta Hospital Lucknow", "dist": "3.0 km", "icon": "🏥"},
            {"type": "Schools", "name": "City Montessori School", "dist": "1.2 km", "icon": "🏫"},
            {"type": "Colleges", "name": "IIM Lucknow", "dist": "9.5 km", "icon": "🎓"},
            {"type": "Railway Station", "name": "Charbagh Railway Station", "dist": "5.6 km", "icon": "🚂"},
            {"type": "Metro Station", "name": "Hazratganj Metro Station", "dist": "2.4 km", "icon": "🚇"},
            {"type": "Bus Stand", "name": "Alambagh ISBT", "dist": "4.8 km", "icon": "🚌"},
            {"type": "Airport", "name": "Lucknow Airport", "dist": "12.0 km", "icon": "✈️"},
            {"type": "Shopping Mall", "name": "Phoenix Palassio Mall", "dist": "4.0 km", "icon": "🛍️"}
        ]
    },
    "Noida": {
        "avg_price_sqft": 6500,
        "cost_tier": "Medium Cost",
        "badge_color": "#eab308",
        "ratings": {"Safety": 4.0, "Schools": 4.5, "Hospitals": 4.3, "Transport": 4.5, "Shopping": 4.4},
        "facilities": [
            {"type": "Hospitals", "name": "Max Super Speciality Hospital", "dist": "2.2 km", "icon": "🏥"},
            {"type": "Schools", "name": "Step by Step School", "dist": "3.8 km", "icon": "🏫"},
            {"type": "Colleges", "name": "Amity University Noida", "dist": "4.0 km", "icon": "🎓"},
            {"type": "Railway Station", "name": "Hazrat Nizamuddin Station", "dist": "11.2 km", "icon": "🚂"},
            {"type": "Metro Station", "name": "Noida Sector 18 Metro", "dist": "1.0 km", "icon": "🚇"},
            {"type": "Bus Stand", "name": "Noida Depot Bus Stand", "dist": "5.5 km", "icon": "🚌"},
            {"type": "Airport", "name": "IGI Airport Delhi", "dist": "26.5 km", "icon": "✈️"},
            {"type": "Shopping Mall", "name": "DLF Mall of India", "dist": "1.2 km", "icon": "🛍️"}
        ]
    }
}

# Indian Rupee Formatting (e.g. ₹ 74.50 Lakhs or Crore)
def format_currency_inr(value):
    if value >= 10000000:
        return f"₹ {value/10000000:.2f} Cr"
    elif value >= 100000:
        return f"₹ {value/100000:.2f} Lakhs"
    else:
        return f"₹ {value:,.2f}"

# Hero Banner Header
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">Next-Gen Real Estate AI</div>
    <h1 class="hero-title">BrickValue AI</h1>
    <p class="hero-subtitle">High-fidelity property valuations and deep market analytics powered by machine learning.</p>
</div>
""", unsafe_allow_html=True)

if df is not None and model is not None:
    # 5 Tab Navigation Panel
    tab_predict, tab_compare, tab_locality, tab_projections, tab_metrics = st.tabs([
        "🏠 Estimate Valuation", 
        "⚖️ Compare Properties",
        "📍 Locality & Nearby Insights",
        "📈 Appreciation & City Trends",
        "📊 Market Analytics & Model"
    ])
    
    # ------------------- TAB 1: PREDICT & FINANCIALS -------------------
    with tab_predict:
        st.markdown('<h2 class="section-title">Configure Property Specifications</h2>', unsafe_allow_html=True)
        
        # Grid layout for inputs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            area = st.slider("Area (Square Feet)", 
                             min_value=100, 
                             max_value=int(df['area'].max()), 
                             value=5000, 
                             step=50,
                             help="Select the total carpet/plot area of the house.")
            bedrooms = st.selectbox("Number of Bedrooms", 
                                    options=sorted(df['bedrooms'].unique()), 
                                    index=2,
                                    help="Total number of bedrooms in the property.")
            bathrooms = st.selectbox("Number of Bathrooms", 
                                     options=sorted(df['bathrooms'].unique()), 
                                     index=0,
                                     help="Total number of bathrooms in the property.")
            stories = st.selectbox("Number of Stories", 
                                   options=sorted(df['stories'].unique()), 
                                   index=1,
                                   help="Total number of floors/stories in the building.")
            
        with col2:
            parking = st.selectbox("Parking Spaces", 
                                   options=sorted(df['parking'].unique()), 
                                   index=1,
                                   help="Number of dedicated parking spaces.")
            furnishingstatus = st.selectbox("Furnishing Status", 
                                            options=["Furnished", "Semi-Furnished", "Unfurnished"],
                                            index=1,
                                            help="Furnishing state of the property.")
            mainroad = st.toggle("Main Road Access", value=True, help="Does the house have direct access to a main road?")
            guestroom = st.toggle("Has Guest Room", value=False, help="Does the house include a dedicated guest room?")
            
        with col3:
            basement = st.toggle("Has Basement", value=False, help="Is there a basement in the house?")
            hotwaterheating = st.toggle("Has Hot Water Heating", value=False, help="Is hot water heating installed?")
            airconditioning = st.toggle("Has Air Conditioning", value=True, help="Does the house have central or window air conditioning?")
            prefarea = st.toggle("Located in Preferred Area", value=False, help="Is the house located in a highly preferred residential zone?")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Preprocessing inputs to match pipeline format
        input_data = {
            'area': area,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'stories': stories,
            'mainroad': 1 if mainroad else 0,
            'guestroom': 1 if guestroom else 0,
            'basement': 1 if basement else 0,
            'hotwaterheating': 1 if hotwaterheating else 0,
            'airconditioning': 1 if airconditioning else 0,
            'parking': parking,
            'prefarea': 1 if prefarea else 0,
        }
        
        # Add dummy encoded furnishing status
        input_data['furnishingstatus_semi-furnished'] = 1 if furnishingstatus == "Semi-Furnished" else 0
        input_data['furnishingstatus_unfurnished'] = 1 if furnishingstatus == "Unfurnished" else 0
        
        # Convert to DataFrame aligning columns precisely
        input_df = pd.DataFrame([input_data])
        input_df = input_df[metadata['features']]
        
        # Scale inputs
        input_scaled = scaler.transform(input_df)
        
        # Prediction
        predicted_price = model.predict(input_scaled)[0]
        
        # Calculate market positioning percentage
        min_p = df['price'].min()
        max_p = df['price'].max()
        percent_of_max = min(100, max(0, int((predicted_price - min_p) / (max_p - min_p) * 100)))

        # Render Prediction Card
        st.markdown(f"""
        <div class="prediction-card">
            <div class="prediction-label">Estimated Valuation</div>
            <div class="prediction-value">{format_currency_inr(predicted_price)}</div>
            <div class="prediction-confidence">
                Raw Value: <b>₹ {predicted_price:,.0f}</b> | Model Engine: <b>{metadata['best_model_name']}</b> (R²: <b>{metadata['results'][metadata['best_model_name']]['R2']:.2%}</b>)
            </div>
            <div class="valuation-bar-container">
                <div class="valuation-bar-fill" style="width: {percent_of_max}%;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #94a3b8; margin-top: 10px;">
                <span>Min Market: {format_currency_inr(min_p)}</span>
                <span><b>{percent_of_max}%</b> relative price position</span>
                <span>Max Market: {format_currency_inr(max_p)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Grid layout for selected property specs
        st.markdown('<h3 style="color:#f8fafc; margin-top:2rem; margin-bottom:1rem;">Selected Specifications Review</h3>', unsafe_allow_html=True)
        spec_col1, spec_col2, spec_col3, spec_col4 = st.columns(4)
        
        with spec_col1:
            st.markdown(f"""
            <div class="spec-card">
                <div class="spec-icon">📐</div>
                <div class="spec-details">
                    <span class="spec-label">Carpet Area</span>
                    <span class="spec-val">{area:,} sq ft</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="spec-card">
                <div class="spec-icon">🛏️</div>
                <div class="spec-details">
                    <span class="spec-label">Bedrooms</span>
                    <span class="spec-val">{bedrooms} Rooms</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with spec_col2:
            st.markdown(f"""
            <div class="spec-card">
                <div class="spec-icon">🚿</div>
                <div class="spec-details">
                    <span class="spec-label">Bathrooms</span>
                    <span class="spec-val">{bathrooms} Baths</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="spec-card">
                <div class="spec-icon">🏢</div>
                <div class="spec-details">
                    <span class="spec-label">Total Stories</span>
                    <span class="spec-val">{stories} Floors</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with spec_col3:
            st.markdown(f"""
            <div class="spec-card">
                <div class="spec-icon">🚗</div>
                <div class="spec-details">
                    <span class="spec-label">Parking slots</span>
                    <span class="spec-val">{parking} Cars</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="spec-card">
                <div class="spec-icon">🛋️</div>
                <div class="spec-details">
                    <span class="spec-label">Furnishing</span>
                    <span class="spec-val">{furnishingstatus}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with spec_col4:
            st.markdown(f"""
            <div class="spec-card">
                <div class="spec-icon">❄️</div>
                <div class="spec-details">
                    <span class="spec-label">Air Condition</span>
                    <span class="spec-val">{"Installed" if airconditioning else "None"}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="spec-card">
                <div class="spec-icon">📍</div>
                <div class="spec-details">
                    <span class="spec-label">Location Zone</span>
                    <span class="spec-val">{"Preferred Area" if prefarea else "Standard"}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # FINANCIALS SECTION: EMI CALCULATOR & AFFORDABILITY METER
        st.markdown('<h2 class="section-title">💸 Financial Planning & Affordability</h2>', unsafe_allow_html=True)
        fin_col1, fin_col2 = st.columns(2)
        
        with fin_col1:
            st.markdown('<h3 style="color:#f8fafc; margin-bottom:1rem;">EMI Calculator</h3>', unsafe_allow_html=True)
            down_payment = st.slider("Down Payment (₹)", 
                                     min_value=0.0, 
                                     max_value=float(predicted_price), 
                                     value=float(predicted_price * 0.20), 
                                     step=50000.0,
                                     format="%.0f",
                                     help="Enter the amount you can pay upfront.")
            
            interest_rate = st.slider("Annual Interest Rate (%)", 
                                      min_value=5.0, 
                                      max_value=15.0, 
                                      value=8.5, 
                                      step=0.1,
                                      help="Interest rate of the bank housing loan.")
            
            tenure_years = st.slider("Loan Tenure (Years)", 
                                     min_value=5, 
                                     max_value=30, 
                                     value=20, 
                                     step=1,
                                     help="Number of years to repay the loan.")
            
            # Mathematics of EMI
            loan_amount = predicted_price - down_payment
            r = interest_rate / (12 * 100)  # Monthly rate
            n = tenure_years * 12           # Monthly periods
            
            if loan_amount > 0:
                emi = loan_amount * r * ((1 + r)**n) / (((1 + r)**n) - 1)
                total_payment = emi * n
                total_interest = total_payment - loan_amount
                total_payable = total_payment + down_payment
            else:
                emi = 0.0
                total_payment = 0.0
                total_interest = 0.0
                total_payable = down_payment
                
            st.markdown(f"""
            <div style="background:rgba(30,41,59,0.3); padding:1.5rem; border-radius:18px; border:1px solid rgba(255,255,255,0.06); margin-top:1rem;">
                <table style="width:100%; border-collapse:collapse; color:#f1f5f9; font-size:0.95rem;">
                    <tr>
                        <td style="padding:6px 0;">House Valuation:</td>
                        <td style="text-align:right; font-weight:600;">{format_currency_inr(predicted_price)}</td>
                    </tr>
                    <tr>
                        <td style="padding:6px 0;">Down Payment:</td>
                        <td style="text-align:right; font-weight:600; color:#fb7185;">- {format_currency_inr(down_payment)}</td>
                    </tr>
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.1);">
                        <td style="padding:6px 0; font-weight:600; color:#38bdf8;">Loan Principal Amount:</td>
                        <td style="text-align:right; font-weight:700; color:#38bdf8;">{format_currency_inr(loan_amount)}</td>
                    </tr>
                    <tr>
                        <td style="padding:10px 0; font-size:1.15rem; font-weight:700; color:#f43f5e;">Monthly EMI:</td>
                        <td style="text-align:right; font-size:1.25rem; font-weight:700; color:#f43f5e;">{format_currency_inr(emi)} / mo</td>
                    </tr>
                    <tr>
                        <td style="padding:6px 0;">Total Interest:</td>
                        <td style="text-align:right; font-weight:600; color:#94a3b8;">{format_currency_inr(total_interest)}</td>
                    </tr>
                    <tr style="border-top:1px solid rgba(255,255,255,0.1); font-size:1.05rem;">
                        <td style="padding:10px 0; font-weight:600;">Total Payable Outflow:</td>
                        <td style="text-align:right; font-weight:700; color:#f8fafc;">{format_currency_inr(total_payable)}</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
        with fin_col2:
            st.markdown('<h3 style="color:#f8fafc; margin-bottom:1rem;">Affordability Meter</h3>', unsafe_allow_html=True)
            monthly_salary = st.number_input("Enter Monthly Salary (₹)", 
                                             min_value=10000.0, 
                                             max_value=10000000.0, 
                                             value=150000.0, 
                                             step=5000.0,
                                             help="Enter your net monthly take-home salary.")
            
            # Affordability thresholds
            if emi == 0:
                affordability = "Affordable (No Loan Required)"
                color = "#22c55e"  # Green
                pct = 0
                desc = "Excellent! You can afford the property entirely via cash/down payment. Zero monthly debt obligations."
            else:
                pct = min(100, int((emi / monthly_salary) * 100))
                if pct <= 30:
                    affordability = "Affordable"
                    color = "#22c55e"  # Green
                    desc = "Excellent! The monthly EMI consumes less than 30% of your salary. This is considered financially healthy and fits safely within bank lending limits."
                elif pct <= 50:
                    affordability = "Moderately Affordable"
                    color = "#eab308"  # Yellow
                    desc = "Manageable, but approach with caution. The monthly EMI represents 30% to 50% of your salary. You will need to maintain a strict budget."
                else:
                    affordability = "Expensive / Overleveraged"
                    color = "#ef4444"  # Red
                    desc = "Risky investment! The monthly EMI exceeds 50% of your take-home pay. Standard lenders may reject this. We recommend increasing your down payment or choosing a lower-priced home."
                    
            st.markdown(f"""
            <div style="background:rgba(30,41,59,0.3); padding:1.5rem; border-radius:18px; border:1px solid rgba(255,255,255,0.06); text-align:center; min-height:330px; display:flex; flex-direction:column; justify-content:center;">
                <p style="margin:0; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.1em; color:#94a3b8;">Valuation Income Ratio</p>
                <h3 style="color:{color}; font-size:1.9rem; font-weight:700; margin:0.5rem 0;">{affordability}</h3>
                
                <div style="width:100%; background:rgba(255,255,255,0.05); height:12px; border-radius:9999px; overflow:hidden; margin:1rem 0; border:1px solid rgba(255,255,255,0.1);">
                    <div style="width:{pct}%; height:100%; background:{color}; border-radius:9999px; box-shadow:0 0 12px {color};"></div>
                </div>
                
                <p style="margin:0; font-size:1.1rem; color:#f1f5f9;">
                    EMI consumes <b>{pct}%</b> of your monthly earnings.
                </p>
                <p style="margin-top:1.25rem; font-size:0.85rem; color:#94a3b8; line-height:1.5; padding:0 0.5rem;">
                    {desc}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        # DYNAMIC AI-BASED SUGGESTIONS & INSIGHTS (RULE-BASED)
        st.markdown('<h2 class="section-title">💡 AI-Based Valuation Suggestions</h2>', unsafe_allow_html=True)
        
        # Build rule-based recommendations
        ai_suggestions = []
        
        # 1. Bedroom-to-Area Density rule
        density = area / bedrooms
        if density < 400:
            ai_suggestions.append({
                "icon": "⚠️",
                "title": "High Bedroom Density",
                "desc": f"The property features only {density:.0f} sq ft per bedroom. This points to cramped rooms. Consider lowering the bedroom count or selecting an area of at least {bedrooms * 450} sq ft."
            })
        elif density > 1400:
            ai_suggestions.append({
                "icon": "✨",
                "title": "Spacious Room Layout",
                "desc": f"Generous spacing of {density:.0f} sq ft per bedroom. Room sizes will feel very luxurious, large, and spacious."
            })
            
        # 2. Bathroom ratio rule
        if stories > 1 and bathrooms < 2:
            ai_suggestions.append({
                "icon": "🚽",
                "title": "Bathroom Shortage",
                "desc": f"This {stories}-story house has only 1 bathroom. Adding at least one more bathroom is recommended for multi-story convenience and value retention."
            })
            
        # 3. Amenity appreciation rating rule
        if prefarea == 1 and airconditioning == 1:
            ai_suggestions.append({
                "icon": "📈",
                "title": "High Resale Appeal",
                "desc": "Corner/preferred location combined with central AC. Properties with these exact amenities historically retain value and command rent premiums."
            })
        else:
            ai_suggestions.append({
                "icon": "🏠",
                "title": "Upgrade Recommendation",
                "desc": "Adding air conditioning or buying in a preferred zone represents a high ROI upgrade that significantly improves valuation multiplier."
            })
            
        # 4. Budget constraints rule
        if emi > 0.40 * monthly_salary:
            ai_suggestions.append({
                "icon": "💡",
                "title": "Financial Re-alignment",
                "desc": "The predicted valuation is stretching your income limits. Try searching in lower-cost nodes like Noida or Ahmedabad, or lower the carpet area specifications."
            })
            
        # Render dynamic suggestions in grid
        cols_sug = st.columns(len(ai_suggestions))
        for idx, sug in enumerate(ai_suggestions):
            with cols_sug[idx]:
                st.markdown(f"""
                <div class="driver-card">
                    <div class="spec-icon">{sug['icon']}</div>
                    <div>
                        <div class="driver-title">{sug['title']}</div>
                        <div class="driver-desc">{sug['desc']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    # ------------------- TAB 2: COMPARE PROPERTIES -------------------
    with tab_compare:
        st.markdown('<h2 class="section-title">⚖️ Compare Two Properties Side-by-Side</h2>', unsafe_allow_html=True)
        st.write("Easily cross-examine two different property specifications and calculate model-predicted values to find the best market deal.")
        
        comp_col1, comp_col2 = st.columns(2)
        
        with comp_col1:
            st.markdown('<h3 style="color:#fb7185;">Property A Specs</h3>', unsafe_allow_html=True)
            area_a = st.slider("Property A: Area (Sq Ft)", 100, int(df['area'].max()), 4500, step=50, key="area_a")
            bedrooms_a = st.selectbox("Property A: Bedrooms", options=sorted(df['bedrooms'].unique()), index=2, key="beds_a")
            bathrooms_a = st.selectbox("Property A: Bathrooms", options=sorted(df['bathrooms'].unique()), index=1, key="baths_a")
            stories_a = st.selectbox("Property A: Stories", options=sorted(df['stories'].unique()), index=1, key="stories_a")
            parking_a = st.selectbox("Property A: Parking Spaces", options=sorted(df['parking'].unique()), index=1, key="park_a")
            furnishing_a = st.selectbox("Property A: Furnishing Status", options=["Furnished", "Semi-Furnished", "Unfurnished"], index=1, key="furn_a")
            ac_a = st.toggle("Property A: Air Conditioning", value=True, key="ac_a")
            prefarea_a = st.toggle("Property A: Preferred Area", value=False, key="pref_a")
            mainroad_a = st.toggle("Property A: Main Road Access", value=True, key="mr_a")
            guestroom_a = st.toggle("Property A: Guest Room", value=False, key="gr_a")
            basement_a = st.toggle("Property A: Basement", value=False, key="bsmt_a")
            hwh_a = st.toggle("Property A: Hot Water Heating", value=False, key="hwh_a")
            
        with comp_col2:
            st.markdown('<h3 style="color:#fb7185;">Property B Specs</h3>', unsafe_allow_html=True)
            area_b = st.slider("Property B: Area (Sq Ft)", 100, int(df['area'].max()), 6000, step=50, key="area_b")
            bedrooms_b = st.selectbox("Property B: Bedrooms", options=sorted(df['bedrooms'].unique()), index=3, key="beds_b")
            bathrooms_b = st.selectbox("Property B: Bathrooms", options=sorted(df['bathrooms'].unique()), index=2, key="baths_b")
            stories_b = st.selectbox("Property B: Stories", options=sorted(df['stories'].unique()), index=1, key="stories_b")
            parking_b = st.selectbox("Property B: Parking Spaces", options=sorted(df['parking'].unique()), index=2, key="park_b")
            furnishing_b = st.selectbox("Property B: Furnishing Status", options=["Furnished", "Semi-Furnished", "Unfurnished"], index=0, key="furn_b")
            ac_b = st.toggle("Property B: Air Conditioning", value=True, key="ac_b")
            prefarea_b = st.toggle("Property B: Preferred Area", value=True, key="pref_b")
            mainroad_b = st.toggle("Property B: Main Road Access", value=True, key="mr_b")
            guestroom_b = st.toggle("Property B: Guest Room", value=True, key="gr_b")
            basement_b = st.toggle("Property B: Basement", value=True, key="bsmt_b")
            hwh_b = st.toggle("Property B: Hot Water Heating", value=False, key="hwh_b")
            
        # Run comparison predictions
        input_a = {
            'area': area_a, 'bedrooms': bedrooms_a, 'bathrooms': bathrooms_a, 'stories': stories_a,
            'mainroad': 1 if mainroad_a else 0, 'guestroom': 1 if guestroom_a else 0,
            'basement': 1 if basement_a else 0, 'hotwaterheating': 1 if hwh_a else 0,
            'airconditioning': 1 if ac_a else 0, 'parking': parking_a, 'prefarea': 1 if prefarea_a else 0,
            'furnishingstatus_semi-furnished': 1 if furnishing_a == "Semi-Furnished" else 0,
            'furnishingstatus_unfurnished': 1 if furnishing_a == "Unfurnished" else 0
        }
        
        input_b = {
            'area': area_b, 'bedrooms': bedrooms_b, 'bathrooms': bathrooms_b, 'stories': stories_b,
            'mainroad': 1 if mainroad_b else 0, 'guestroom': 1 if guestroom_b else 0,
            'basement': 1 if basement_b else 0, 'hotwaterheating': 1 if hwh_b else 0,
            'airconditioning': 1 if ac_b else 0, 'parking': parking_b, 'prefarea': 1 if prefarea_b else 0,
            'furnishingstatus_semi-furnished': 1 if furnishing_b == "Semi-Furnished" else 0,
            'furnishingstatus_unfurnished': 1 if furnishing_b == "Unfurnished" else 0
        }
        
        df_a = pd.DataFrame([input_a])[metadata['features']]
        df_b = pd.DataFrame([input_b])[metadata['features']]
        
        pred_a = model.predict(scaler.transform(df_a))[0]
        pred_b = model.predict(scaler.transform(df_b))[0]
        
        psqft_a = pred_a / area_a
        psqft_b = pred_b / area_b
        
        # Highlight best valuation deal (lower price per sq ft)
        if psqft_a < psqft_b:
            val_a_badge = "🏆 Best Valuation Deal"
            val_b_badge = ""
            best_prop = "Property A"
        else:
            val_a_badge = ""
            val_b_badge = "🏆 Best Valuation Deal"
            best_prop = "Property B"
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h3 style="color:#f8fafc; margin-bottom:1rem;">Comparison Matrix</h3>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <table style="width:100%; border-collapse:collapse; color:#f1f5f9; font-size:1rem; border:1px solid rgba(255,255,255,0.05); text-align:left;">
            <thead>
                <tr style="background:rgba(244,63,94,0.1); border-bottom:2px solid rgba(255,255,255,0.1);">
                    <th style="padding:12px;">Parameter</th>
                    <th style="padding:12px;">Property A Details</th>
                    <th style="padding:12px;">Property B Details</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                    <td style="padding:12px; font-weight:600;">Valuation Verdict</td>
                    <td style="padding:12px; color:#fb7185; font-weight:700; font-size:1.15rem;">{format_currency_inr(pred_a)}</td>
                    <td style="padding:12px; color:#fb7185; font-weight:700; font-size:1.15rem;">{format_currency_inr(pred_b)}</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05); background:rgba(255,255,255,0.01);">
                    <td style="padding:12px; font-weight:600;">Property Size (Carpet Area)</td>
                    <td style="padding:12px;">{area_a:,} sq ft</td>
                    <td style="padding:12px;">{area_b:,} sq ft</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                    <td style="padding:12px; font-weight:600;">Price per Square Foot</td>
                    <td style="padding:12px; font-weight:600; color:#38bdf8;">{format_currency_inr(psqft_a)} / sq ft</td>
                    <td style="padding:12px; font-weight:600; color:#38bdf8;">{format_currency_inr(psqft_b)} / sq ft</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05); background:rgba(255,255,255,0.01);">
                    <td style="padding:12px; font-weight:600;">Bedrooms</td>
                    <td style="padding:12px;">{bedrooms_a} Beds</td>
                    <td style="padding:12px;">{bedrooms_b} Beds</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                    <td style="padding:12px; font-weight:600;">Bathrooms</td>
                    <td style="padding:12px;">{bathrooms_a} Baths</td>
                    <td style="padding:12px;">{bathrooms_b} Baths</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05); background:rgba(255,255,255,0.01);">
                    <td style="padding:12px; font-weight:600;">Total Stories</td>
                    <td style="padding:12px;">{stories_a} Floors</td>
                    <td style="padding:12px;">{stories_b} Floors</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                    <td style="padding:12px; font-weight:600;">Parking spots</td>
                    <td style="padding:12px;">{parking_a} Cars</td>
                    <td style="padding:12px;">{parking_b} Cars</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05); background:rgba(255,255,255,0.01);">
                    <td style="padding:12px; font-weight:600;">Furnishing</td>
                    <td style="padding:12px;">{furnishing_a}</td>
                    <td style="padding:12px;">{furnishing_b}</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                    <td style="padding:12px; font-weight:600;">Air Conditioning</td>
                    <td style="padding:12px;">{"Installed" if ac_a else "None"}</td>
                    <td style="padding:12px;">{"Installed" if ac_b else "None"}</td>
                </tr>
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05); background:rgba(255,255,255,0.01);">
                    <td style="padding:12px; font-weight:600;">Valuation Analysis Recommendation</td>
                    <td style="padding:12px; font-weight:700; color:#22c55e;">{val_a_badge}</td>
                    <td style="padding:12px; font-weight:700; color:#22c55e;">{val_b_badge}</td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)
        
        st.info(f"💡 **Analysis Recommendation:** **{best_prop}** offers a lower price-per-square-foot of valuation, indicating it represents a higher relative asset value for its size!")

    # ------------------- TAB 3: LOCALITY & NEARBY INSIGHTS -------------------
    with tab_locality:
        st.markdown('<h2 class="section-title">📍 City Locality & Nearby Infrastructure Insights</h2>', unsafe_allow_html=True)
        st.write("Browse star ratings and nearby public facilities based on major Indian metropolitan markets.")
        
        selected_city = st.selectbox("Select City for Locality Insights", options=list(CITIES_DATA.keys()), index=0)
        city_info = CITIES_DATA[selected_city]
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h3 style="color:#f8fafc; margin-bottom:1rem;">Locality Ratings (Quality of Life)</h3>', unsafe_allow_html=True)
        
        ratings = city_info["ratings"]
        overall_score = sum(ratings.values()) / len(ratings)
        
        # Build 6 rating cards in columns
        rate_cols = st.columns(6)
        
        labels_map = [
            ("Safety Rating", "Safety", "🛡️"),
            ("Schooling Quality", "Schools", "🎓"),
            ("Healthcare System", "Hospitals", "🏥"),
            ("Public Transport", "Transport", "🚇"),
            ("Markets & Retail", "Shopping", "🛍️")
        ]
        
        for idx, (label, key, emoji) in enumerate(labels_map):
            with rate_cols[idx]:
                score = ratings[key]
                full_stars = int(score)
                empty_stars = 5 - full_stars
                stars_txt = "★" * full_stars + "☆" * empty_stars
                st.markdown(f"""
                <div style="background:rgba(30,41,59,0.3); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:1.25rem; text-align:center;">
                    <div style="font-size:1.8rem; margin-bottom:0.25rem;">{emoji}</div>
                    <div style="font-size:0.75rem; text-transform:uppercase; color:#94a3b8; letter-spacing:0.05em; margin-bottom:0.5rem;">{label}</div>
                    <div style="font-size:1.25rem; font-weight:700; color:#fb7185; margin-bottom:0.25rem;">{score:.1f} / 5</div>
                    <div style="font-size:0.85rem; color:#f59e0b;">{stars_txt}</div>
                </div>
                """, unsafe_allow_html=True)
                
        with rate_cols[5]:
            st.markdown(f"""
            <div style="background:rgba(244,63,94,0.12); border:1px solid rgba(244,63,94,0.3); border-radius:16px; padding:1.25rem; text-align:center; min-height:136px; display:flex; flex-direction:column; justify-content:center;">
                <div style="font-size:0.75rem; text-transform:uppercase; color:#fb7185; letter-spacing:0.05em; font-weight:600; margin-bottom:0.5rem;">Overall Locality Score</div>
                <div style="font-size:1.6rem; font-weight:700; color:#f43f5e; margin-bottom:0.25rem;">{overall_score:.2f} / 5</div>
                <div style="font-size:0.85rem; color:#f43f5e; font-weight:600;">{"Excellent Node" if overall_score >= 4.3 else "Prime Node"}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<h3 style="color:#f8fafc; margin-bottom:1rem;">Nearby Facilities (Demo Data)</h3>', unsafe_allow_html=True)
        
        facilities = city_info["facilities"]
        fac_cols = st.columns(4)
        for index, fac in enumerate(facilities):
            col_idx = index % 4
            with fac_cols[col_idx]:
                st.markdown(f"""
                <div class="spec-card">
                    <div class="spec-icon">{fac['icon']}</div>
                    <div class="spec-details">
                        <span class="spec-label">{fac['type']}</span>
                        <span class="spec-val" style="font-size:0.95rem; color:#f1f5f9;">{fac['name']}</span>
                        <span style="font-size:0.8rem; color:#fb7185; font-weight:600;">{fac['dist']} away</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ------------------- TAB 4: APPRECIATION & CITY TRENDS -------------------
    with tab_projections:
        st.markdown('<h2 class="section-title">📈 Property Appreciation & City Comparisons</h2>', unsafe_allow_html=True)
        
        p_col1, p_col2 = st.columns(2)
        
        with p_col1:
            st.markdown('<h3 style="color:#f8fafc; margin-bottom:1rem;">Future Price Appreciation Projection</h3>', unsafe_allow_html=True)
            st.write("Compounding annual valuation forecasts based on configurable market appreciation sliders.")
            appreciation_rate = st.slider("Assumed Compound Annual Growth Rate (CAGR %)", 
                                         min_value=1.0, 
                                         max_value=20.0, 
                                         value=7.0, 
                                         step=0.5,
                                         help="Adjust expected annual real estate growth rate.")
            
            years = [0, 1, 3, 5, 10]
            projected_vals = []
            for yr in years:
                val = predicted_price * ((1 + appreciation_rate / 100)**yr)
                projected_vals.append(val)
                
            proj_df = pd.DataFrame({
                'Timeline': ['Current', '1 Year', '3 Years', '5 Years', '10 Years'],
                'Valuation (₹)': projected_vals,
                'Value Display': [format_currency_inr(v) for v in projected_vals]
            })
            
            fig_proj = px.line(
                proj_df,
                x='Timeline',
                y='Valuation (₹)',
                text='Value Display',
                markers=True,
                color_discrete_sequence=["#fb7185"]
            )
            fig_proj.update_traces(textposition="top center", line=dict(width=3, color="#f43f5e"))
            fig_proj.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            )
            st.plotly_chart(fig_proj, use_container_width=True)
            st.caption("⚠️ **Projections disclaimer:** These calculations compounded future values based on a set CAGR. Real-world property markets vary based on infrastructure nodes, macro inflation, and micro demand.")
            
        with p_col2:
            st.markdown('<h3 style="color:#f8fafc; margin-bottom:1rem;">City-wise Pricing Trends</h3>', unsafe_allow_html=True)
            selected_trend_city = st.selectbox("Select City for Market Cost Info", options=list(CITIES_DATA.keys()), index=0, key="trend_city")
            trend_city_info = CITIES_DATA[selected_trend_city]
            
            st.markdown(f"""
            <div style="background:rgba(30,41,59,0.3); border:1px solid rgba(255,255,255,0.05); border-radius:18px; padding:1.5rem; margin-bottom:1.5rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; color:#f8fafc; font-family:'Space Grotesk',sans-serif;">{selected_trend_city} Real Estate Category</h4>
                    <span style="background:{trend_city_info['badge_color']}; color:#ffffff; font-size:0.85rem; font-weight:600; padding:0.3rem 0.9rem; border-radius:9999px; box-shadow:0 0 10px {trend_city_info['badge_color']}80;">
                        {trend_city_info['cost_tier']}
                    </span>
                </div>
                <p style="margin-top:1.25rem; margin-bottom:0; font-size:1.2rem; color:#f1f5f9;">
                    Average Market Price per Sq Ft: <b>{format_currency_inr(trend_city_info['avg_price_sqft'])} / sq ft</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Chart sorting and coloring
            all_cities = list(CITIES_DATA.keys())
            all_prices = [CITIES_DATA[c]["avg_price_sqft"] for c in all_cities]
            colors_chart = ["#f43f5e" if c == selected_trend_city else "#334155" for c in all_cities]
            
            city_df = pd.DataFrame({
                'City': all_cities,
                'Price / Sq Ft (₹)': all_prices,
                'Color': colors_chart
            }).sort_values(by='Price / Sq Ft (₹)', ascending=True)
            
            fig_city = px.bar(
                city_df,
                x='Price / Sq Ft (₹)',
                y='City',
                orientation='h',
                color='City',
                color_discrete_map={row['City']: row['Color'] for _, row in city_df.iterrows()}
            )
            fig_city.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(showgrid=False),
            )
            st.plotly_chart(fig_city, use_container_width=True)

    # ------------------- TAB 5: HISTORIC DATA & MODEL METRICS -------------------
    with tab_metrics:
        st.markdown('<h2 class="section-title">📊 Historical Data Analysis & Model Mechanics</h2>', unsafe_allow_html=True)
        
        # Display EDA Selector and charts
        eda_plot = st.selectbox("Select Historical Visualization", 
                                options=[
                                    "Price vs Area Scatter Matrix", 
                                    "Property Price Distribution", 
                                    "Price Range by Furnishing Status",
                                    "Feature Correlation Heatmap"
                                ])
        
        if eda_plot == "Price vs Area Scatter Matrix":
            st.write("Explore the relationship between carpet area and sale price, segmented by air conditioning.")
            fig = px.scatter(
                df, 
                x="area", 
                y="price", 
                color="airconditioning", 
                hover_data=["bedrooms", "bathrooms", "furnishingstatus"],
                labels={"area": "Area (Sq Ft)", "price": "Price (INR)", "airconditioning": "Has AC"},
                color_discrete_map={"yes": "#fb7185", "no": "#475569"},
                trendline="ols",
                opacity=0.75
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif eda_plot == "Property Price Distribution":
            st.write("Understand the density distribution of house valuations.")
            fig = px.histogram(
                df, 
                x="price", 
                nbins=40,
                marginal="box",
                labels={"price": "Price (INR)"},
                color_discrete_sequence=["#fb7185"]
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif eda_plot == "Price Range by Furnishing Status":
            st.write("Analyze how different levels of furnishing dictate property price ranges.")
            fig = px.box(
                df, 
                x="furnishingstatus", 
                y="price", 
                color="furnishingstatus",
                labels={"furnishingstatus": "Furnishing Status", "price": "Price (INR)"},
                color_discrete_map={"furnished": "#10b981", "semi-furnished": "#fb7185", "unfurnished": "#475569"}
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif eda_plot == "Feature Correlation Heatmap":
            st.write("Observe numerical correlations across features (binary mappings and metrics).")
            num_df = df.copy()
            binary_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
            for col in binary_cols:
                num_df[col] = num_df[col].map({'yes': 1, 'no': 0})
            num_df = pd.get_dummies(num_df, columns=['furnishingstatus'], drop_first=True)
            
            corr = num_df.corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale="magma",
                zmin=-1, zmax=1
            ))
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                width=800,
                height=650
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # ML metrics
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.subheader("Algorithm Comparison Matrix")
            results_df = pd.DataFrame(metadata['results']).T
            results_df['R² Accuracy Score'] = results_df['R2'].apply(lambda x: f"{x:.2%}")
            results_df['Training R² Score'] = results_df['Train_R2'].apply(lambda x: f"{x:.2%}")
            results_df['Mean Absolute Error'] = results_df['MAE'].apply(lambda x: f"₹ {x:,.2f}")
            results_df['RMSE'] = results_df['RMSE'].apply(lambda x: f"₹ {x:,.2f}")
            st.table(results_df[['R² Accuracy Score', 'Training R² Score', 'Mean Absolute Error', 'RMSE']])
            
        with col_m2:
            st.subheader("Model Feature Importance Weight")
            if hasattr(model, 'feature_importances_'):
                importances = model.feature_importances_
                indices = np.argsort(importances)[::-1]
                features_sorted = [metadata['features'][i] for i in indices]
                importances_sorted = importances[indices]
                
                fig_imp = px.bar(
                    x=importances_sorted,
                    y=features_sorted,
                    orientation='h',
                    labels={'x': 'Relative Weight in valuation', 'y': 'Feature'},
                    color=importances_sorted,
                    color_continuous_scale="Reds"
                )
                fig_imp.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    yaxis=dict(autorange="reversed"),
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_imp, use_container_width=True)
            else:
                st.info("Feature importance is not supported for Linear Regression.")
else:
    st.warning("Ensure the system is trained first by running the training pipeline.")

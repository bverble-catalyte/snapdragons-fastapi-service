import streamlit as st
import requests

# ===============================================
# Page Configuration & Styling
# ===============================================
st.set_page_config(
    page_title="Bloom & Timber Garden Supply",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Garden Theme CSS (Targeted Light Theme Overrides)
st.markdown("""
    <style>
    /* Force Light Backgrounds Throughout the App */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #f4f8f3 !important;
        color: #1a331e;
    }

    /* Force Light Sidebar */
    [data-testid="stSidebar"] {
        background-color: #e2ede0 !important;
        border-right: 1px solid #cce0ca !important;
    }

    /* Top Page Padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 95% !important;
    }
    
    /* Header Banner with Specific White Text Rules */
    .main-header {
        background: linear-gradient(135deg, #2D5A27 0%, #4E8752 100%);
        padding: 1.25rem 1.8rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(45, 90, 39, 0.15);
    }
    .main-header h1 {
        color: #ffffff !important;
        font-size: 2.2rem !important;
        font-weight: 700;
        margin: 0 !important;
    }
    .main-header p {
        color: #eaf5e9 !important;
        font-size: 1.05rem !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0 !important;
    }

    /* Stakeholder Notice */
    .dev-badge {
        background-color: #ffffff;
        border: 1px solid #b8dbc1;
        border-left: 5px solid #2D5A27;
        border-radius: 8px;
        padding: 12px 18px;
        margin-bottom: 1.2rem;
        color: #1a331e !important;
        font-size: 0.95rem;
    }

    /* Equal-Height Feature Cards */
    .feature-card {
        background-color: #ffffff;
        border: 1px solid #d0e5d4;
        border-radius: 10px;
        padding: 18px;
        color: #1f3a23 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03);
        height: 125px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }
    .feature-card h4 {
        color: #2D5A27 !important;
        margin-top: 0;
        margin-bottom: 8px;
        font-weight: 700;
        font-size: 1.05rem;
    }
    .feature-card p {
        color: #3b523e !important;
        margin-bottom: 0;
        font-size: 0.90rem;
        line-height: 1.35;
    }

    /* Form Container */
    [data-testid="stForm"] {
        background-color: #ffffff !important;
        border: 1px solid #d0e5d4 !important;
        border-radius: 10px !important;
        padding: 1.5rem !important;
    }

    /* Clean JSON and Code Block Background Fix */
    [data-testid="stJson"], pre {
        background-color: #ffffff !important;
        border: 1px solid #c8e6c9 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }

    /* Primary Action Buttons */
    .stButton>button[kind="primary"] {
        background-color: #2D5A27 !important;
        color: #ffffff !important;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        width: 100%;
        padding: 0.5rem 1rem;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #1e3f1a !important;
    }

    /* Result Card Formatting */
    .result-card {
        background-color: #ffffff;
        border: 1px solid #c8e6c9;
        border-radius: 8px;
        padding: 15px;
        margin-top: 10px;
    }
    .result-card-item {
        font-size: 0.95rem;
        margin-bottom: 6px;
        color: #1a331e;
    }
    </style>
""", unsafe_allow_html=True)

FASTAPI_URL = "http://127.0.0.1:8000"

# ===============================================
# Header Section
# ===============================================
st.markdown("""
    <div class="main-header">
        <h1>🌿 Bloom & Timber Garden Supply</h1>
        <p>Retail Operations & Management Platform</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="dev-badge">
        <strong>📋 Stakeholder Preview:</strong> Platform capabilities are currently under active development by the engineering team (Snapdragon). 
        Features and data endpoints are being integrated incrementally.
    </div>
""", unsafe_allow_html=True)

# ===============================================
# Sidebar Navigation
# ===============================================
st.sidebar.image("https://img.icons8.com/color/96/potted-plant.png", width=65)
st.sidebar.title("Garden Portal")
demo_stage = st.sidebar.radio(
    "Explore Platform:",
    ["🌱 Overview & Status", "🔎 Inventory Search", "📦 Stock Management", "📊 Store Analytics"]
)

st.sidebar.markdown("---")
st.sidebar.caption("🔒 **Environment:** Local Demo")
st.sidebar.caption("⚡ **Engineered by:** Team Snapdragon")

# ===============================================
# View 1: Overview Tab
# ===============================================
if demo_stage == "🌱 Overview & Status":
    st.subheader("Welcome to the Operations Portal")
    st.write(
        "This interactive dashboard demonstrates how store inventory tracking, "
        "pricing rules, and catalog operations are processed live by our API backend."
    )
    
    st.markdown("### ✨ Active Modules")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h4>✅ Inventory Tracking</h4>
                <p>Live verification of store items, measurement units, and current stock counts.</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h4>🛡️ Data Validation</h4>
                <p>Automatic backend rules preventing pricing mistakes and negative stock quantities.</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="feature-card" style="border-color: #ffe082; background-color: #fffdf5;">
                <h4 style="color: #8f6b00 !important;">⏳ Database Integration</h4>
                <p style="color: #5c4700 !important;"><em>In Progress</em> — Currently operating on fast, in-memory state objects.</p>
            </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.info("💡 **Presenter Note:** Use the sidebar on the left to navigate between live product search lookups and inventory updates.")

# ===============================================
# View 2: GET Requests (Inventory Search)
# ===============================================
elif demo_stage == "🔎 Inventory Search":
    st.subheader("🔎 Product & Inventory Search")
    st.write("Retrieve real-time product pricing and stock details directly from the core service.")
    
    submit_button = False
    search_id = ""

    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("##### Search Inputs")
        category = st.selectbox("Category", ["Products", "Customers (Upcoming)", "Orders (Upcoming)"])
        
        if category == "Products":
            search_id = st.text_input("Product Name Filter", value="Basil Plant 4in Pot")
            submit_button = st.button("Fetch Details", type="primary")
        else:
            st.caption("🔒 This category will be available in a future release.")

    with col2:
        st.markdown("##### API Output")
        if submit_button:
            with st.spinner("Querying engine..."):
                try:
                    response = requests.get(f"{FASTAPI_URL}/products")
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error(f"Record not found. (Status Code: {response.status_code})")
                except requests.RequestException:
                    st.error("⚠️ Server Offline: Could not connect to the backend engine.")
        else:
            st.info("Click **'Fetch Details'** to submit request.")

# ===============================================
# View 3: POST Requests (Add Stock/Products)
# ===============================================
elif demo_stage == "📦 Stock Management":
    st.subheader("📦 Add New Inventory Item")
    st.write("Test backend input validation rules (rejects negative prices or invalid stock counts).")
    
    submitted = False
    payload = {}
    item_name = ""

    category = st.selectbox("Select Record Type", ["Products"])
    col1, col2 = st.columns([1, 1.2])

    with col1:
        if category == "Products":
            with st.form("action_form"):
                st.markdown("##### Item Specifications")
                item_name = st.text_input("Product Name", value="Organic Potting Soil 20lb")
                unit_name = st.text_input("Unit Type", value="bag")
                cost_per_unit = st.number_input("Supplier Cost ($)", min_value=0.0, value=3.50, step=0.25)
                price_per_unit = st.number_input("Retail Price ($)", min_value=0.0, value=8.99, step=0.25)
                quantity_in_stock = st.number_input("Initial Quantity in Stock", min_value=0, value=25, step=1)

                submitted = st.form_submit_button("Add to Inventory", type="primary")
                
                payload = {
                    "name": item_name,
                    "unit": unit_name,
                    "cost_per_unit": cost_per_unit,
                    "price_per_unit": price_per_unit,
                    "quantity_in_stock": quantity_in_stock
                }

    with col2:
        st.markdown("##### Creation Status")
        if submitted:
            with st.spinner("Submitting product..."):
                try:
                    response = requests.post(f"{FASTAPI_URL}/products", json=payload)
                    if response.status_code in [200, 201]:
                        st.success(f"🌱 Product '{item_name}' created successfully!")
                        st.json(response.json())
                    else:
                        st.error(f"Validation Error ({response.status_code})")
                        st.json(response.json())
                except requests.RequestException:
                    st.error("⚠️ Server Offline: Could not connect to backend.")
        else:
            st.info("Fill out specifications and click **'Add to Inventory'**.")

# ===============================================
# View 4: Analytics / Business Metrics
# ===============================================
elif demo_stage == "📊 Store Analytics":
    st.subheader("📊 Garden Center Health & Analytics")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Total Requests", value="1,245", delta="+12%")
    m2.metric(label="Response Time", value="38 ms", delta="-4 ms", delta_color="inverse")
    m3.metric(label="System Health", value="99.9%", delta="Optimal")
    m4.metric(label="Catalog Status", value="Live", delta="In-Memory")
    
    st.markdown("---")
    st.markdown("##### 📈 Planned Metric Dashboards")
    st.caption("Sales volume charts, inventory margin analysis, and re-order thresholds will populate once database persistence is added.")
import streamlit as st
import requests

# ===============================================
#   Page Configuration (Title, Tab Icon, Layout)
# ===============================================
st.set_page_config(
    page_title="Snapdragons | Business Demo",
    page_icon="🌺",
    layout="wide"
)

# Header Section
st.title("🌺 Team Snapdragons")
st.subheader("Backend Platform & API Operations Demo")
st.caption("Presenting real-time system capability for business stakeholders")
st.markdown("---")

# Sidebar Navigation
st.sidebar.title("Navigation")
demo_stage = st.sidebar.radio(
    "Select Workflow / Feature:",
    ["Overview", "Get Requests", "Post Requests", "System Metrics"]
)

FASTAPI_URL = "http://127.0.0.1:8000"

# View - Overview Tab
if demo_stage == "Overview":
    st.header("Project Overview & Value")
    st.write(
        "Welcome! This demo highlights how our backend handles data flow, "
        "validates input, and supports core business actions."
    )
    
    st.info("💡 **Presenter Tip:** Use the sidebar on the left to navigate through each business workflow live.")

# View - Get Requests Tab
elif demo_stage == "Get Requests":
    st.header("🔍 Search & Retrieve Data")
    st.write("Demonstrating real-time data retrieval from our backend database.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        search_id = ""
        submit_button = False
        category = st.selectbox("Category", ["Products", "Customers", "Orders"])
        if category == "Products":
            st.markdown("### Inputs")
            search_id = st.text_input("Enter Product ID", value="1001")
            submit_button = st.button("Fetch Data", type="primary")
    with col2:
        st.markdown("### Output")
        if submit_button:
            try:
                response = requests.get(f"{FASTAPI_URL}/products/{search_id}")
                if response.status_code == 200:
                    st.json(response.json())
                else:
                    st.error("Record not found.")
            except requests.RequestException as e:
                st.error(f"Error Connecting to Server")
        else:
            st.info("Click 'Fetch Data' to send a request to FastAPI.")

# View - Post Requests Tab
elif demo_stage == "Post Requests":
    st.header("📝 Create Item")
    st.write("Demonstrating input validation and backend state mutation.")
    
    category = st.selectbox("Category", ["Product", "Priority", "Express"])

    if category == "Product":
        with st.form("action_form"):
            item_name = st.text_input("Product Name", value="Product Name")
            unit_name = st.text_input("Unit Type", value="bag")
            cost_per_unit = st.number_input("Cost per Unit", min_value=0.0, value=9.99, step=0.01)
            price_per_unit = st.number_input("Price per Unit", min_value=0.0, value=19.99, step=0.01)
            quantity_in_stock = st.number_input("Quantity in Stock", min_value=0, value=3, step=1)

            submitted = st.form_submit_button("Submit Request", type="primary")
            payload = {"name": item_name, "unit": unit_name, "cost_per_unit": cost_per_unit, "price_per_unit": price_per_unit, "quantity_in_stock": quantity_in_stock}
            try:
                response = requests.post(f"{FASTAPI_URL}/{category.lower()}", json=payload)
                if response.status_code == 201:
                    st.success(f"{category} created successfully!")
                    st.json(response.json())
                else:
                    st.error(f"Failed to create {category}. Status Code: {response.status_code}")
            except requests.RequestException as e:
                st.error(f"Error Connecting to Server")
    
# View - Analytics/Metrics Placeholder
elif demo_stage == "System Metrics":
    st.header("📊 Business Analytics & Status")
    
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Total Requests Handled", value="1,245", delta="+12%")
    m2.metric(label="Avg Response Time", value="42 ms", delta="-5 ms", delta_color="inverse")
    m3.metric(label="API Health Status", value="99.9%", delta="Stable")
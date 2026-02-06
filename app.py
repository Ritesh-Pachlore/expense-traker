import streamlit as st
import pandas as pd
import plotly.express as px
from data_manager import load_data, add_expense, get_summary_by_category
from datetime import date

# Page Layout
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

st.title("💰 Personal Expense Tracker")

# Sidebar - Add Expense
st.sidebar.header("Add New Expense")
with st.sidebar.form("expense_form"):
    expense_date = st.date_input("Date", date.today())
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Other"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    description = st.text_input("Description (Optional)")
    
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        if amount > 0:
            add_expense(expense_date, category, amount, description)
            st.sidebar.success("Expense Added!")
        else:
            st.sidebar.error("Amount must be greater than 0.")

# Main Dashboard
tab1, tab2 = st.tabs(["📊 Dashboard", "📝 History"])

with tab1:
    st.header("Spending Overview")
    
    # Metrics
    df = load_data()
    if not df.empty:
        total_spent = df["Amount"].sum()
        st.metric("Total Spent", f"${total_spent:,.2f}")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Expenses by Category")
            summary = get_summary_by_category()
            fig = px.pie(summary, values="Amount", names="Category", title="Category Distribution", hole=0.3)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.subheader("Recent Expenses")
            st.dataframe(df.tail(5).sort_index(ascending=False), use_container_width=True)
    else:
        st.info("No expenses recorded yet. Note some expenses in the sidebar!")

with tab2:
    st.header("Transaction History")
    df = load_data()
    if not df.empty:
        # Simple filter
        category_filter = st.multiselect("Filter by Category", options=df["Category"].unique(), default=df["Category"].unique())
        filtered_df = df[df["Category"].isin(category_filter)]
        
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("No history available.")

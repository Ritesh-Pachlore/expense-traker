import pandas as pd
import os
from datetime import datetime

# Use relative path for cloud compatibility
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "expenses.csv")

def ensure_data_dir():
    """Ensures the data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_data():
    """Loads data from the CSV file. Creates it if it doesn't exist."""
    ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        df.to_csv(DATA_FILE, index=False)
        return df
    else:
        return pd.read_csv(DATA_FILE)

def add_expense(date, category, amount, description):
    """Adds a new expense to the CSV file."""
    df = load_data()
    new_entry = pd.DataFrame({
        "Date": [date],
        "Category": [category],
        "Amount": [amount],
        "Description": [description]
    })
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def get_summary_by_category():
    """Groups expenses by category for visualization."""
    df = load_data()
    if df.empty:
        return pd.DataFrame(columns=["Category", "Amount"])
    summary = df.groupby("Category")["Amount"].sum().reset_index()
    return summary

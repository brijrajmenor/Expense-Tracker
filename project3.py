import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime


# Initialize database
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount REAL,
            description TEXT,
            category TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def add_expense(date, amount, description, category):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO expenses (date, amount, description, category)
        VALUES (?, ?, ?, ?)
    """,
        (date, amount, description, category),
    )
    conn.commit()
    conn.close()


def get_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    data = cursor.fetchall()
    conn.close()
    return data


def get_summary():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()
    return data


# Initialize database
init_db()

# Streamlit UI
st.title("Expense Tracker")

menu = ["Add Expense", "View Expenses", "View Summary"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Expense":
    st.subheader("Add Expense")
    date = st.date_input("Date")
    amount = st.number_input("Amount", min_value=0)
    description = st.text_input("Description")
    category = st.selectbox(
        "Category", ["Food", "Transportation", "Entertainment", "Utilities", "Other"]
    )

    if st.button("Add"):
        add_expense(date, amount, description, category)
        st.success("Expense added successfully")

elif choice == "View Expenses":
    st.subheader("View Expenses")
    data = get_expenses()
    df = pd.DataFrame(data, columns=["ID", "Date", "Amount", "Description", "Category"])
    st.dataframe(df)

elif choice == "View Summary":
    st.subheader("View Summary")
    data = get_summary()
    df = pd.DataFrame(data, columns=["Category", "Total Amount"])
    st.bar_chart(df.set_index("Category"))

# Run with: streamlit run <this_script.py>

# import streamlit as st
# import sqlite3
# import pandas as pd
# import joblib
# import os
# BASE = os.path.dirname(__file__)
# DB = os.path.join(BASE, 'ecommerce_hackathon.db')
# st.set_page_config(
#     page_title='E-Commerce Customer Intelligence', layout='wide')


# @st.cache_resource
# def load_models(): return joblib.load(os.path.join(BASE, 'churn_model.pkl')
#                                       ), joblib.load(os.path.join(BASE, 'sentiment_model.pkl'))


# @st.cache_data
# def sql(q):
#     with sqlite3.connect(DB) as c:
#         return pd.read_sql_query(q, c)


# page = st.sidebar.radio(
#     'Section', ['Dashboard', 'Churn Prediction', 'Sentiment Analysis'])
# if page == 'Dashboard':
#     st.title('E-Commerce Customer Intelligence Dashboard')
#     # These outputs are executed directly against SQLite (requirement: >=3 SQL dashboard outputs).
#     total = sql("SELECT SUM(quantity*unit_price*(1-discount)*(1-returned)) revenue, COUNT(DISTINCT order_id) orders, COUNT(DISTINCT customer_id) customers FROM orders WHERE quantity>0 AND unit_price>0 AND date(order_date) IS NOT NULL")
#     a, b, c = st.columns(3)
#     a.metric('Net Revenue', f"PKR {total.revenue.iloc[0]:,.0f}")
#     b.metric('Valid Orders', f"{int(total.orders.iloc[0]):,}")
#     c.metric('Customers', f"{int(total.customers.iloc[0]):,}")
#     monthly = sql("SELECT strftime('%Y-%m',order_date) month, SUM(quantity*unit_price*(1-discount)*(1-returned)) revenue FROM orders WHERE quantity>0 AND unit_price>0 AND date(order_date) IS NOT NULL GROUP BY month ORDER BY month")
#     category = sql("SELECT TRIM(LOWER(p.category)) category, SUM(o.quantity*o.unit_price*(1-o.discount)*(1-o.returned)) revenue FROM orders o JOIN products p USING(product_id) WHERE o.quantity>0 AND o.unit_price>0 AND date(o.order_date) IS NOT NULL GROUP BY TRIM(LOWER(p.category)) ORDER BY revenue DESC")
#     st.subheader('Monthly Net Revenue')
#     st.line_chart(monthly.set_index('month'))
#     st.subheader('Category Revenue')
#     st.bar_chart(category.set_index('category'))
# elif page == 'Churn Prediction':
#     st.title('Customer Churn Prediction')
#     churn, _ = load_models()
#     with st.form('churn'):
#         total_orders = st.number_input('Total orders', 0, 1000, 10)
#         total_spending = st.number_input('Total spending', 0.0, value=100000.0)
#         avg_order_value = st.number_input(
#             'Average order value', 0.0, value=10000.0)
#         days_since_last_order = st.number_input(
#             'Days since last order', 0, 2000, 30)
#         return_rate = st.slider('Return rate', 0.0, 1.0, 0.05)
#         avg_delivery_days = st.number_input(
#             'Average delivery days', 0.0, 30.0, 3.0)
#         age = st.number_input('Age', 18, 100, 30)
#         membership_type = st.selectbox(
#             'Membership type', ['Standard', 'Silver', 'Gold', 'Premium'])
#         go = st.form_submit_button('Predict')
#     if go:
#         x = pd.DataFrame([locals()])[['total_orders', 'total_spending', 'avg_order_value',
#                                       'days_since_last_order', 'return_rate', 'avg_delivery_days', 'age', 'membership_type']]
#         pred = int(churn.predict(x)[0])
#         prob = float(churn.predict_proba(x)[0, 1])
#         st.metric('Churn probability', f'{prob:.1%}')
#         st.success('Predicted: Churn' if pred else 'Predicted: Active')
# else:
#     st.title('Review Sentiment Analysis')
#     _, sent = load_models()
#     text = st.text_area('Review text')
#     if st.button('Analyze sentiment') and text.strip():
#         st.success(f"Predicted sentiment: {sent.predict([text])[0]}")

import streamlit as st
import pandas as pd
import sqlite3
import joblib
from pathlib import Path


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="E-Commerce Customer Intelligence",
    page_icon="🛒",
    layout="wide"
)


# =========================================================
# FILE PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "ecommerce_hackathon.db"
CHURN_MODEL_PATH = BASE_DIR / "churn_model.pkl"
SENTIMENT_MODEL_PATH = BASE_DIR / "sentiment_model.pkl"


# =========================================================
# LOAD MODELS
# =========================================================

@st.cache_resource
def load_churn_model():
    return joblib.load(CHURN_MODEL_PATH)


@st.cache_resource
def load_sentiment_model():
    return joblib.load(SENTIMENT_MODEL_PATH)


churn_model = load_churn_model()
sentiment_model = load_sentiment_model()


# =========================================================
# DATABASE FUNCTION
# =========================================================

def run_query(query):
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🛒 E-Commerce AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Churn Prediction",
        "Sentiment Analysis"
    ]
)


# =========================================================
# PAGE 1: DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("📊 E-Commerce Dashboard")

    st.write(
        "Business overview of customer activity, "
        "sales performance and product categories."
    )

    # -----------------------------------------------------
    # SQL QUERY 1: TOTAL REVENUE
    # -----------------------------------------------------

    revenue_query = """
    SELECT
        SUM(
            quantity * unit_price *
            (1 - discount) *
            (1 - returned)
        ) AS total_revenue
    FROM orders
    WHERE
        date(order_date) IS NOT NULL
        AND quantity > 0
        AND unit_price > 0;
    """

    revenue_df = run_query(revenue_query)

    total_revenue = revenue_df["total_revenue"].iloc[0]

    # -----------------------------------------------------
    # SQL QUERY 2: TOTAL ORDERS
    # -----------------------------------------------------

    orders_query = """
    SELECT
        COUNT(DISTINCT order_id) AS total_orders
    FROM orders
    WHERE
        date(order_date) IS NOT NULL
        AND quantity > 0
        AND unit_price > 0;
    """

    orders_df = run_query(orders_query)

    total_orders = orders_df["total_orders"].iloc[0]

    # -----------------------------------------------------
    # SQL QUERY 3: TOTAL CUSTOMERS
    # -----------------------------------------------------

    customers_query = """
    SELECT
        COUNT(DISTINCT customer_id) AS total_customers
    FROM orders
    WHERE
        date(order_date) IS NOT NULL
        AND quantity > 0
        AND unit_price > 0;
    """

    customers_df = run_query(customers_query)

    total_customers = customers_df["total_customers"].iloc[0]

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Total Net Revenue",
            f"PKR {total_revenue:,.0f}"
        )

    with col2:
        st.metric(
            "📦 Total Orders",
            f"{total_orders:,}"
        )

    with col3:
        st.metric(
            "👥 Total Customers",
            f"{total_customers:,}"
        )

    st.divider()

    # -----------------------------------------------------
    # SQL QUERY 4: MONTHLY REVENUE
    # -----------------------------------------------------

    monthly_query = """
    SELECT
        strftime('%Y-%m', order_date) AS month,

        SUM(
            quantity * unit_price *
            (1 - discount) *
            (1 - returned)
        ) AS net_revenue

    FROM orders

    WHERE
        date(order_date) IS NOT NULL
        AND quantity > 0
        AND unit_price > 0

    GROUP BY
        strftime('%Y-%m', order_date)

    ORDER BY
        month;
    """

    monthly_revenue = run_query(monthly_query)

    # -----------------------------------------------------
    # SQL QUERY 5: CATEGORY REVENUE
    # -----------------------------------------------------

    category_query = """
    SELECT
        p.category,

        SUM(
            o.quantity * o.unit_price *
            (1 - o.discount) *
            (1 - o.returned)
        ) AS net_revenue

    FROM orders o

    JOIN products p
        ON o.product_id = p.product_id

    WHERE
        date(o.order_date) IS NOT NULL
        AND o.quantity > 0
        AND o.unit_price > 0

    GROUP BY
        p.category

    ORDER BY
        net_revenue DESC;
    """

    category_revenue = run_query(category_query)

    # -----------------------------------------------------
    # CHARTS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📈 Monthly Revenue Trend")

        monthly_chart = monthly_revenue.set_index("month")

        st.line_chart(
            monthly_chart["net_revenue"]
        )

    with col2:

        st.subheader("📊 Revenue by Category")

        category_chart = category_revenue.set_index("category")

        st.bar_chart(
            category_chart["net_revenue"]
        )

    # -----------------------------------------------------
    # RETURN RATE BY CATEGORY
    # -----------------------------------------------------

    return_query = """
    SELECT
        p.category,

        AVG(o.returned) * 100 AS return_rate

    FROM orders o

    JOIN products p
        ON o.product_id = p.product_id

    WHERE
        date(o.order_date) IS NOT NULL
        AND o.quantity > 0
        AND o.unit_price > 0

    GROUP BY
        p.category

    ORDER BY
        return_rate DESC;
    """

    return_rate = run_query(return_query)

    st.subheader("↩️ Return Rate by Product Category")

    st.bar_chart(
        return_rate.set_index("category")["return_rate"]
    )


# =========================================================
# PAGE 2: CHURN PREDICTION
# =========================================================

elif page == "Churn Prediction":

    st.title("🔮 Customer Churn Prediction")

    st.write(
        "Enter customer purchase-history information "
        "to estimate the probability of churn."
    )

    # -----------------------------------------------------
    # INPUTS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        total_orders = st.number_input(
            "Total Orders",
            min_value=1,
            value=5,
            step=1
        )

        total_spending = st.number_input(
            "Total Spending",
            min_value=0.0,
            value=50000.0
        )

        avg_order_value = st.number_input(
            "Average Order Value",
            min_value=0.0,
            value=10000.0
        )

        days_since_last_order = st.number_input(
            "Days Since Last Order",
            min_value=0,
            value=30,
            step=1
        )

    with col2:

        return_rate = st.number_input(
            "Return Rate",
            min_value=0.0,
            max_value=1.0,
            value=0.10
        )

        avg_delivery_days = st.number_input(
            "Average Delivery Days",
            min_value=0.0,
            value=4.0
        )

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30
        )

        membership_type = st.selectbox(
            "Membership Type",
            [
                "Basic",
                "Silver",
                "Gold",
                "Platinum"
            ]
        )

    # -----------------------------------------------------
    # INPUT DATAFRAME
    # -----------------------------------------------------

    input_data = pd.DataFrame({
        "total_orders": [total_orders],
        "total_spending": [total_spending],
        "avg_order_value": [avg_order_value],
        "days_since_last_order": [days_since_last_order],
        "return_rate": [return_rate],
        "avg_delivery_days": [avg_delivery_days],
        "age": [age],
        "membership_type": [membership_type]
    })

    # -----------------------------------------------------
    # PREDICTION
    # -----------------------------------------------------

    if st.button(
        "Predict Churn",
        type="primary"
    ):

        prediction = churn_model.predict(
            input_data
        )[0]

        probability = churn_model.predict_proba(
            input_data
        )[0][1]

        if prediction == 1:

            st.error(
                "⚠️ Customer is predicted to CHURN."
            )

        else:

            st.success(
                "✅ Customer is predicted to remain ACTIVE."
            )

        st.metric(
            "Churn Probability",
            f"{probability:.2%}"
        )


# =========================================================
# PAGE 3: SENTIMENT ANALYSIS
# =========================================================

elif page == "Sentiment Analysis":

    st.title("💬 Customer Review Sentiment Analysis")

    st.write(
        "Enter a customer review to classify it as "
        "Positive, Neutral or Negative."
    )

    # -----------------------------------------------------
    # TEXT INPUT
    # -----------------------------------------------------

    review_text = st.text_area(
        "Customer Review",
        placeholder="Enter customer review here...",
        height=150
    )

    # -----------------------------------------------------
    # PREDICTION
    # -----------------------------------------------------

    if st.button(
        "Analyze Sentiment",
        type="primary"
    ):

        if review_text.strip() == "":

            st.warning(
                "Please enter a review."
            )

        else:

            prediction = sentiment_model.predict(
                [review_text]
            )[0]

            if prediction == "Positive":

                st.success(
                    f"😊 Predicted Sentiment: {prediction}"
                )

            elif prediction == "Negative":

                st.error(
                    f"😞 Predicted Sentiment: {prediction}"
                )

            else:

                st.info(
                    f"😐 Predicted Sentiment: {prediction}"
                )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI-Powered E-Commerce Customer Intelligence System"
)

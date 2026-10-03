# AI-Powered E-Commerce Customer Intelligence System

End-to-end solution for the supplied SQLite hackathon database: data inspection/cleaning, five SQL business queries, EDA, churn ML, a 32→16→1 neural network, TF-IDF sentiment classification, saved models, and a three-section Streamlit app.

## Cleaning decisions
- Customer age: 100 missing values were median-imputed, then stored as integer because age is a whole-year field and observed ages were valid (18–65).
- Product category: whitespace/case variants were standardized (e.g. `electronics`, `ELECTRONICS`, `Electronics `). Missing brand (20) was set to `Unknown` rather than dropping products.
- Orders: 30 invalid dates, 45 non-positive quantities and 35 non-positive prices were excluded from analytical/modeling rows because they cannot represent valid purchases. 40 missing delivery-day values were median-imputed; 55 missing payment methods became `Unknown`.
- Reviews: 16 invalid dates, 48 missing texts, and 25 ratings outside 1–5 were excluded from NLP training because they cannot support the specified sentiment labels.
- Revenue definition: `quantity × unit_price × (1-discount) × (1-returned)`. Returned orders contribute zero realized revenue.

## Key results
- Valid orders: **64,890**; customers represented: **7,187**; total net revenue: **PKR 865,169,922.03**; return rate: **6.69%**.
- Churn dataset: 6,535 customers who purchased by 31-May-2026; churn rate **49.06%** in the Jun–Aug target window.
- Logistic Regression: Accuracy **0.715**, Precision **0.661**, Recall **0.860**, F1 **0.748**, ROC-AUC **0.787**.
- Random Forest: Accuracy **0.713**, Precision **0.676**, Recall **0.797**, F1 **0.732**, ROC-AUC **0.773**.
- Neural network (32→16→1): Accuracy **0.711**, Precision **0.676**, Recall **0.788**, F1 **0.728**, ROC-AUC **0.785**.
- Selected churn model: **Logistic Regression**, because it has the strongest F1 and ROC-AUC here and the highest churn recall, while remaining simpler and easier to explain.
- Sentiment Logistic Regression + TF-IDF achieved **1.000 weighted F1** on the held-out set. This unusually perfect score is a limitation signal: reviews appear strongly templated and labels are derived directly from ratings, so real-world generalization may be much weaker.

## Business insights
1. **Electronics dominates net revenue (~PKR 604.5M)**, far above other categories. This makes electronics commercially critical but also creates concentration risk; inventory, pricing and supplier reliability in this category deserve close monitoring.
2. **Karachi contributes the most revenue (~PKR 224.3M), followed by Lahore (~PKR 155.1M)**. Marketing and fulfillment capacity should reflect this demand concentration while growth campaigns can target lower-revenue cities.
3. **Fashion has the highest return rate (~11.25%)**, above electronics (~7.98%). Size/fit guidance, product imagery and description quality are likely high-value areas to investigate because returns directly reduce realized revenue.
4. Monthly revenue rises strongly through 2026, from about **PKR 38.8M in January to PKR 76.6M in July**, before easing to **PKR 67.7M in August**. Capacity planning should account for this recent higher run rate, while the August decline should be monitored before treating it as a trend.

## Run
```bash
pip install -r requirements.txt
python analysis.py
python deep_learning.py
streamlit run app.py
```

`business_queries.sql` contains all five required SQL queries. `analysis.py` creates cleaned analytical datasets and saved ML/NLP models. `deep_learning.py` trains/evaluates the neural network. The Streamlit app loads saved models using relative paths and executes dashboard SQL directly against SQLite.

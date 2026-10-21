import pandas as pd
import streamlit as st
from textblob import TextBlob
from pathlib import Path

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Customer Experience Intelligence",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# 2. PROFESSIONAL COLOURFUL DESIGN
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #f7f4ff 0%, #f0f6ff 55%, #edfffb 100%);
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #25145f 0%, #5031b5 55%, #167c96 100%);
}
[data-testid="stSidebar"] * {
    color: white;
}
h1 {
    color: #352078 !important;
    font-weight: 800 !important;
}
h2, h3 {
    color: #44318b !important;
    font-weight: 700 !important;
}
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff, #f0edff);
    border: 1px solid #e4ddff;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 6px 20px rgba(72, 53, 150, 0.09);
}
[data-testid="stMetricValue"] {
    color: #5938c5;
    font-weight: 800;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #713de2, #2878ed);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 700;
}
[data-testid="stAlert"] {
    border-radius: 12px;
}
hr {
    border-color: #ddd6fe;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. HEADER
# =====================================================

st.title("Customer Experience Intelligence Platform")

st.write(
    "Understand customer feedback, discover recurring issues, "
    "and turn customer reviews into practical business insights."
)

st.caption("CAPACITI | Week 4 Individual AI Project | E-commerce")


# =====================================================
# 4. SENTIMENT ANALYSIS
# =====================================================

def analyse_review(review):
    """Estimate sentiment using TextBlob and simple phrase rules."""

    if not isinstance(review, str) or not review.strip():
        return {
            "Sentiment_Polarity": None,
            "Sentiment_Predicted": "Unknown",
            "Needs_Follow_Up": False
        }

    text = review.strip().lower()
    polarity = TextBlob(review).sentiment.polarity

    negative_phrases = [
        "don't love", "do not love", "doesn't love",
        "does not love", "don't like", "do not like",
        "not happy", "not satisfied", "not good",
        "not worth", "never buy", "would not recommend",
        "wouldn't recommend", "not working", "doesn't work",
        "does not work", "did not work", "didn't work",
        "poor quality", "terrible", "disappointing",
        "damaged", "broken", "late delivery"
    ]

    if any(phrase in text for phrase in negative_phrases):
        sentiment = "Negative"
        polarity = min(polarity, -0.1)
    elif polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "Sentiment_Polarity": polarity,
        "Sentiment_Predicted": sentiment,
        "Needs_Follow_Up": sentiment == "Negative"
    }


# =====================================================
# 5. CUSTOMER FEEDBACK THEMES
# =====================================================

THEMES = {
    "Product Quality": [
        "quality", "durable", "durability", "broken",
        "damaged", "defect", "defective", "material",
        "poor quality", "well made", "well-made"
    ],
    "Delivery": [
        "delivery", "delivered", "shipping", "shipped",
        "late", "delayed", "arrived", "courier",
        "package", "packaging"
    ],
    "Price and Value": [
        "price", "expensive", "cheap", "cost",
        "value for money", "affordable", "overpriced",
        "worth the money"
    ],
    "Customer Service": [
        "customer service", "support", "staff",
        "refund", "return", "response", "helpful",
        "rude", "service", "complaint"
    ],
    "Product Performance": [
        "works", "working", "performance", "easy to use",
        "difficult to use", "battery", "speed",
        "features", "function", "stopped working"
    ],
    "Positive Experience": [
        "excellent", "amazing", "love it", "great",
        "wonderful", "satisfied", "recommend",
        "happy", "fantastic", "perfect"
    ]
}


def detect_themes(review):
    """Return all keyword themes found in a review."""

    if not isinstance(review, str) or not review.strip():
        return ["Other / General Feedback"]

    text = review.lower()
    found = []

    for theme, keywords in THEMES.items():
        if any(keyword in text for keyword in keywords):
            found.append(theme)

    if not found:
        found.append("Other / General Feedback")

    return found


# =====================================================
# 6. LOAD THE PROJECT DATASET
# =====================================================

@st.cache_data
def load_project_data():
    folder = Path(__file__).parent
    expected = folder / "customer_reviews_powerbi_v2 (2).csv"

    if expected.exists():
        file_path = expected
    else:
        csv_files = [
            p for p in folder.glob("*.csv")
            if "customer" in p.name.lower()
            or "review" in p.name.lower()
        ]

        if not csv_files:
            raise FileNotFoundError(
                "No customer review CSV found beside app.py. "
                "Check that your dataset is in your GitHub repository."
            )

        file_path = csv_files[0]

    data = pd.read_csv(file_path, sep=None, engine="python")
    data.columns = data.columns.str.strip()

    if "Customer_Review" not in data.columns:
        raise ValueError(
            "The dataset must contain a Customer_Review column."
        )

    results = data["Customer_Review"].apply(
        analyse_review
    ).apply(pd.Series)

    data["Sentiment_Polarity"] = results["Sentiment_Polarity"]
    data["Sentiment_Predicted"] = results["Sentiment_Predicted"]
    data["Needs_Follow_Up"] = results["Needs_Follow_Up"]
    data["Feedback_Themes"] = data["Customer_Review"].apply(
        detect_themes
    )

    return data


try:
    project_data = load_project_data()
    dataset_error = None
except Exception as error:
    project_data = None
    dataset_error = str(error)


# =====================================================
# 7. NAVIGATION
# =====================================================

page = st.sidebar.radio(
    "Choose a feature",
    [
        "📊 Dashboard",
        "💬 Customer Voice",
        "🚨 Issue Monitor",
        "💡 Business Action Plan",
        "📈 Business Impact Tracking",
        "🧪 AI Evaluation",
        "🔍 Analyse a Review",
        "📁 Analyse a CSV Dataset"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Customer Experience Intelligence")
st.sidebar.caption(
    "Sentiment and theme results are estimates. "
    "Review the evidence before taking action."
)


# =====================================================
# 8. DASHBOARD
# =====================================================

if page == "📊 Dashboard":

    st.header("📊 Customer Review Insights")

    st.write(
        "Explore review volume, sentiment, product performance "
        "and customer feedback that may need attention."
    )

    if project_data is None:
        st.error("The project dataset could not be loaded.")
        st.code(dataset_error or "Unknown loading error")

    else:
        data = project_data.copy()

        total = len(data)
        positive = int(
            (data["Sentiment_Predicted"] == "Positive").sum()
        )
        negative = int(
            (data["Sentiment_Predicted"] == "Negative").sum()
        )
        neutral = int(
            (data["Sentiment_Predicted"] == "Neutral").sum()
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🧾 Total Reviews", total)
        c2.metric("😊 Positive", positive)
        c3.metric("⚠️ Negative", negative)
        c4.metric("😐 Neutral", neutral)

        if total:
            st.caption(
                f"Positive: {positive / total:.1%} | "
                f"Negative: {negative / total:.1%} | "
                f"Neutral: {neutral / total:.1%}"
            )

        st.divider()

        left, right = st.columns(2)

        with left:
            st.subheader("🏆 Most Reviewed Products")

            if "Product" in data.columns:
                product_counts = (
                    data["Product"].fillna("Unknown")
                    .astype(str).value_counts().head(10)
                )

                st.bar_chart(product_counts)

                st.dataframe(
                    product_counts.rename("Number of Reviews")
                    .rename_axis("Product").reset_index(),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No Product column is available.")

        with right:
            st.subheader("💬 Sentiment Breakdown")

            sentiment_counts = (
                data["Sentiment_Predicted"].value_counts()
                .reindex(
                    ["Positive", "Neutral", "Negative"],
                    fill_value=0
                )
            )

            st.bar_chart(sentiment_counts)

        st.divider()
        st.subheader("⭐ Average Rating by Product")

        if "Product" in data.columns and "Rating" in data.columns:
            data["Rating_Numeric"] = pd.to_numeric(
                data["Rating"], errors="coerce"
            )

            rating_summary = (
                data.dropna(subset=["Rating_Numeric"])
                .groupby("Product")["Rating_Numeric"]
                .mean().sort_values(ascending=False).round(2)
            )

            st.dataframe(
                rating_summary.rename("Average Rating")
                .rename_axis("Product").reset_index(),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Product or Rating information is unavailable.")

        st.divider()

        st.download_button(
            "⬇️ Download Analysed Dataset",
            data=data.to_csv(index=False).encode("utf-8"),
            file_name="customer_reviews_analysed.csv",
            mime="text/csv"
        )


# =====================================================
# 9. CUSTOMER VOICE
# =====================================================

elif page == "💬 Customer Voice":

    st.header("💬 Customer Voice")

    st.write(
        "Explore the topics customers mention and read their actual "
        "comments to understand their experiences."
    )

    if project_data is None:
        st.error("The project dataset could not be loaded.")
        st.code(dataset_error or "Unknown loading error")

    else:
        data = project_data.copy()

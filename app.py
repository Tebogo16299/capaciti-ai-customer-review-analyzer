
import pandas as pd
import streamlit as st
from textblob import TextBlob
from pathlib import Path

# ----------------------------------------
# 1. PAGE CONFIGURATION
# ----------------------------------------

st.set_page_config(
    page_title="AI Customer Review Analyzer",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------
# 2. COLOURFUL PROFESSIONAL DESIGN
# ----------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(
            135deg, #f7f4ff 0%, #f0f6ff 55%, #edfffb 100%
        );
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(
            180deg, #25145f 0%, #5031b5 55%, #167c96 100%
        );
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
        padding: 20px;
        border-radius: 18px;
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
        padding: 0.65rem 1.2rem;
        font-weight: 700;
        box-shadow: 0 5px 15px rgba(85, 66, 200, 0.2);
    }

    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(90deg, #5728c5, #145fce);
        color: white;
        border: none;
    }

    [data-testid="stTextArea"] textarea,
    [data-testid="stFileUploader"] {
        background-color: white;
        border-radius: 12px;
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    hr {
        border-color: #ddd6fe;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------
# 3. PAGE HEADER
# ----------------------------------------

st.title("AI Customer Review Analyzer")

st.write(
    "Analyse customer feedback using Natural Language Processing (NLP). "
    "Explore product review counts, understand sentiment, and highlight "
    "reviews that may need attention."
)

st.caption(
    "CAPACITI | Week 4 Individual AI Project | E-commerce"
)

# ----------------------------------------
# 4. SENTIMENT ANALYSIS FUNCTION
# ----------------------------------------

def analyse_review(review):
    """Estimate sentiment using TextBlob and simple phrase rules."""

    if not isinstance(review, str) or not review.strip():
        return {
            "Sentiment_Polarity": None,
            "Sentiment_Predicted": "Unknown",
            "Needs_Follow_Up": False
        }

    review = review.strip()
    blob = TextBlob(review)
    polarity = blob.sentiment.polarity
    text = review.lower()

    negative_phrases = [
        "don't love",
        "do not love",
        "doesn't love",
        "does not love",
        "don't like",
        "do not like",
        "not happy",
        "not satisfied",
        "not good",
        "not worth",
        "never buy",
        "would not recommend",
        "wouldn't recommend",
        "not working",
        "doesn't work",
        "does not work",
        "did not work",
        "didn't work",
        "poor quality",
        "terrible",
        "disappointing",
        "damaged",
        "broken",
        "late delivery"
    ]

    has_negative_phrase = any(
        phrase in text for phrase in negative_phrases
    )

    if has_negative_phrase:
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


# ----------------------------------------
# 5. LOAD THE PROJECT DATASET
# ----------------------------------------

@st.cache_data
def load_project_data():
    """Load the CSV and calculate sentiment for every review."""

    project_folder = Path(__file__).parent

    expected_file = (
        project_folder / "customer_reviews_powerbi_v2 (2).csv"
    )

    if expected_file.exists():
        file_path = expected_file
    else:
        csv_files = [
            path for path in project_folder.glob("*.csv")
            if "customer" in path.name.lower()
            or "review" in path.name.lower()
        ]

        if not csv_files:
            raise FileNotFoundError(
                "No customer review CSV was found beside app.py. "
                "Check the CSV filename in your GitHub repository."
            )

        file_path = csv_files[0]

    data = pd.read_csv(file_path, sep=None, engine="python")
    data.columns = data.columns.str.strip()

    if "Customer_Review" not in data.columns:
        raise ValueError(
            "The dataset must contain a Customer_Review column. "
            f"Columns found: {', '.join(data.columns.astype(str))}"
        )

    results = (
        data["Customer_Review"]
        .apply(analyse_review)
        .apply(pd.Series)
    )

    data["Sentiment_Polarity"] = results["Sentiment_Polarity"]
    data["Sentiment_Predicted"] = results["Sentiment_Predicted"]
    data["Needs_Follow_Up"] = results["Needs_Follow_Up"]

    return data


try:
    project_data = load_project_data()
    dataset_error = None
except Exception as error:
    project_data = None
    dataset_error = str(error)


# ----------------------------------------
# 6. NAVIGATION
# ----------------------------------------

page = st.sidebar.radio(
    "Choose a feature",
    [
        "📊 Dashboard",
        "🔍 Analyse a Review",
        "📁 Analyse a CSV Dataset"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("CAPACITI | AI Customer Review Analyzer")
st.sidebar.caption(
    "Sentiment predictions are estimates and should be reviewed."
)


# ----------------------------------------
# 7. CUSTOMER REVIEW DASHBOARD
# ----------------------------------------

if page == "📊 Dashboard":

    st.header("📊 Customer Review Insights")

    st.write(
        "Explore the dataset, compare products, and find customer "
        "feedback that may need attention."
    )

    if project_data is None:

        st.error("The project dataset could not be loaded.")
        st.code(dataset_error or "Unknown dataset loading error")

        st.info(
            "Check that your customer review CSV is committed "
            "to the same GitHub repository as app.py."
        )

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

        # KPI CARDS

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("🧾 Total Reviews", total)
        col2.metric("😊 Positive Reviews", positive)
        col3.metric("⚠️ Negative Reviews", negative)
        col4.metric("😐 Neutral Reviews", neutral)

        if total:
            st.caption(
                f"Positive: {positive / total:.1%}  |  "
                f"Negative: {negative / total:.1%}  |  "
                f"Neutral: {neutral / total:.1%}"
            )

        st.divider()

        # MOST-REVIEWED PRODUCTS AND SENTIMENT

        left, right = st.columns(2)

        with left:

            st.subheader("🏆 Most Reviewed Products")

            if "Product" in data.columns:

                product_counts = (
                    data["Product"]
                    .fillna("Unknown product")
                    .astype(str)
                    .value_counts()
                    .head(10)
                )

                st.bar_chart(product_counts)

                st.caption(
                    "Top 10 products ranked by number of reviews."
                )

                st.dataframe(
                    product_counts
                    .rename("Number of Reviews")
                    .rename_axis("Product")
                    .reset_index(),
                    use_container_width=True,
                    hide_index=True
                )

            else:
                st.info(
                    "The dataset does not contain a Product column."
                )

        with right:

            st.subheader("💬 Sentiment Breakdown")

            sentiment_counts = (
                data["Sentiment_Predicted"]
                .value_counts()
                .reindex(
                    ["Positive", "Neutral", "Negative"],
                    fill_value=0
                )
            )

            st.bar_chart(sentiment_counts)

            st.caption(
                "Number of reviews in each sentiment category."
            )

        st.divider()

        # AVERAGE PRODUCT RATINGS

        st.subheader("⭐ Average Rating by Product")

        if "Product" in data.columns and "Rating" in data.columns:

            data["Rating_Numeric"] = pd.to_numeric(
                data["Rating"],
                errors="coerce"
            )

            rating_summary = (
                data.dropna(subset=["Rating_Numeric"])
                .groupby("Product")["Rating_Numeric"]
                .mean()
                .sort_values(ascending=False)
                .round(2)
            )

            st.dataframe(
                rating_summary
                .rename("Average Rating")
                .rename_axis("Product")
                .reset_index(),
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info(
                "Product and/or Rating columns are not available."
            )

        st.divider()

        # NEGATIVE REVIEWS

        st.subheader("🚨 Customer Reviews Requiring Attention")

        complaints = data[
            data["Needs_Follow_Up"]
        ].copy()

        display_columns = [
            column for column in [
                "Review_ID",
                "Product",
                "Rating",
                "Customer_Review",
                "Sentiment_Predicted",
                "Needs_Follow_Up"
            ]
            if column in complaints.columns
        ]

        if complaints.empty:

            st.success(
                "No negative reviews were flagged in this dataset."
            )

        else:

            st.write(
                f"**{len(complaints)}** reviews were flagged for follow-up."
            )

            st.dataframe(
                complaints[display_columns],
                use_container_width=True,
                hide_index=True
            )

        st.divider()

        # SEARCH CUSTOMER REVIEWS

        st.subheader("🔎 Search Customer Reviews")

        search = st.text_input(
            "Search by product name or words in a review",
            key="dashboard_review_search"
        )

        searchable_columns = [
            column for column in [
                "Product",
                "Customer_Review"
            ]
            if column in data.columns
        ]

        if search:

            mask = pd.Series(False, index=data.index)

            for column in searchable_columns:

                mask = mask | data[column].astype(str).str.contains(
                    search,
                    case=False,
                    na=False,
                    regex=False
                )

            search_columns = [
                column for column in [
                    "Review_ID",
                    "Product",
                    "Rating",
                    "Customer_Review",
                    "Sentiment_Predicted"
                ]
                if column in data.columns
            ]

            st.dataframe(
                data.loc[mask, search_columns],
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                f"Matching reviews: {int(mask.sum())}"
            )

        # DOWNLOAD ANALYSED DATA

        st.download_button(
            label="⬇️ Download Full Analysed Dataset",
            data=data.to_csv(index=False).encode("utf-8"),
            file_name="customer_reviews_analysed.csv",
            mime="text/csv"
        )


# ----------------------------------------
# 8. ANALYSE AN INDIVIDUAL REVIEW
# ----------------------------------------

elif page == "🔍 Analyse a Review":

    st.header("🔍 Analyse an Individual Review")

    st.write(
        "Enter a customer comment to estimate its sentiment "
        "and check whether it may need follow-up."
    )

    review = st.text_area(
        "Enter the customer's review",
        placeholder=(
            "Example: The delivery was late and the product was damaged."
        ),
        height=150
    )

    if st.button("Analyse Sentiment", type="primary"):

        if not review.strip():

            st.warning(
                "Please enter a customer review first."
            )

        else:

            result = analyse_review(review)

            st.subheader("Analysis Results")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Predicted Sentiment",
                result["Sentiment_Predicted"]
            )

            col2.metric(
                "Sentiment Polarity",
                f'{result["Sentiment_Polarity"]:.3f}'
            )

            col3.metric(
                "Needs Follow-up",
                "Yes" if result["Needs_Follow_Up"] else "No"
            )

            st.write("**Customer's comment:**")
            st.info(review)

            if result["Sentiment_Predicted"] == "Negative":

                st.warning(
                    "This review may need attention. "
                    "Investigate the customer's concern."
                )

            elif result["Sentiment_Predicted"] == "Positive":

                st.success(
                    "This review expresses positive sentiment."
                )

            else:

                st.info(
                    "This review was classified as neutral."
                )


# ----------------------------------------
# 9. ANALYSE AN UPLOADED CSV DATASET
# ----------------------------------------

else:

    st.header("📁 Analyse a Customer Review Dataset")

    st.write(
        "Upload a CSV file containing a column named Customer_Review. "
        "You can upload your existing e-commerce dataset."
    )

    uploaded_file = st.file_uploader(
        "Upload customer reviews CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            data = pd.read_csv(uploaded_file)
            data.columns = data.columns.str.strip()

            if "Customer_Review" not in data.columns:

                st.error(
                    "The CSV must contain a Customer_Review column."
                )

            else:

                st.success(
                    f"Dataset loaded: {len(data)} records."
                )

                results = (
                    data["Customer_Review"]
                    .apply(analyse_review)
                    .apply(pd.Series)
                )

                analysed_data = data.copy()

                analysed_data["Sentiment_Polarity"] = (
                    results["Sentiment_Polarity"]
                )

                analysed_data["Sentiment_Predicted"] = (
                    results["Sentiment_Predicted"]
                )

                analysed_data["Needs_Follow_Up"] = (
                    results["Needs_Follow_Up"]
                )

                sentiment_counts = (
                    analysed_data["Sentiment_Predicted"]
                    .value_counts()
                    .reindex(
                        ["Positive", "Neutral", "Negative"],
                        fill_value=0
                    )
                )

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Total Reviews",
                    len(analysed_data)
                )

                col2.metric(
                    "Positive Reviews",
                    int(sentiment_counts["Positive"])
                )

                col3.metric(
                    "Negative Reviews",
                    int(sentiment_counts["Negative"])
                )

                col4.metric(
                    "Neutral Reviews",
                    int(sentiment_counts["Neutral"])
                )

                st.subheader("Sentiment Distribution")
                st.bar_chart(sentiment_counts)

                if "Product" in analysed_data.columns:

                    st.subheader("Most Reviewed Products")

                    st.bar_chart(
                        analysed_data["Product"]
                        .fillna("Unknown product")
                        .astype(str)
                        .value_counts()
                        .head(10)
                    )

                st.subheader("Analysed Customer Reviews")

                st.dataframe(
                    analysed_data,
                    use_container_width=True,
                    hide_index=True
                )

                negative_reviews = analysed_data[
                    analysed_data["Needs_Follow_Up"]
                ]

                st.subheader("Reviews Flagged for Follow-up")

                st.write(
                    f"{len(negative_reviews)} reviews were "
                    "classified as negative."
                )

                st.dataframe(
                    negative_reviews,
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    label="⬇️ Download Analysed CSV for Power BI",
                    data=analysed_data.to_csv(
                        index=False
                    ).encode("utf-8"),
                    file_name="customer_reviews_analysed.csv",
                    mime="text/csv"
                )

        except Exception as error:

            st.error(
                f"Unable to process the dataset: {error}"
            )


# ----------------------------------------
# 10. FOOTER
# ----------------------------------------

st.divider()

st.caption(
    "Developed for the CAPACITI Week 4 Individual AI Project. "
    "Sentiment estimates use TextBlob polarity plus simple phrase rules; "
    "they are not a trained machine-learning classifier and should be "
    "validated before business decisions."
)


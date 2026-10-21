
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
# COLOURFUL PROFESSIONAL DESIGN
# ----------------------------------------

st.markdown("""
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
""", unsafe_allow_html=True)

st.title("AI Customer Review Analyzer")
st.write(
    "Analyse customer feedback using Natural Language Processing (NLP). "
    "Identify sentiment and highlight reviews that may need attention."
)

st.caption("CAPACITI | Individual AI Project | E-commerce")

# ----------------------------------------
# 2. SENTIMENT ANALYSIS FUNCTION
# ----------------------------------------


def analyse_review(review):
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

    # Handle common negation patterns that basic
    # sentiment analysis may misunderstand.
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

    # Adjust for known negative phrases.
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
# 3. NAVIGATION
# ----------------------------------------

page = st.sidebar.radio(
    "Choose a feature",
    ["Analyse a Review", "Analyse a CSV Dataset"]
)

# ----------------------------------------
# 4. SINGLE REVIEW ANALYSIS
# ----------------------------------------

if page == "Analyse a Review":

    st.header("Analyse an Individual Review")

    review = st.text_area(
        "Enter the customer's review",
        placeholder="Example: The delivery was late and the product was damaged."
    )

    if st.button("Analyse Sentiment", type="primary"):
        if not review.strip():
            st.warning("Please enter a customer review first.")
        else:
            result = analyse_review(review)

            st.subheader("Analysis Result")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Predicted Sentiment",
                    result["Sentiment_Predicted"]
                )

            with col2:
                st.metric(
                    "Polarity Score",
                    f'{result["Sentiment_Polarity"]:.3f}'
                )

            if result["Sentiment_Predicted"] == "Positive":
                st.success("The review expresses positive sentiment.")
            elif result["Sentiment_Predicted"] == "Negative":
                st.warning(
                    "Potential customer dissatisfaction detected. "
                    "Consider reviewing the complaint."
                )
            else:
                st.info("The review is classified as neutral.")

            st.caption(
                "Polarity ranges from -1 (negative) to +1 (positive). "
                "This is an automated prediction, not a guarantee "
                "of the customer's true sentiment."
            )

# ----------------------------------------
# 5. CSV DATASET ANALYSIS
# ----------------------------------------

else:

    st.header("Analyse a Customer Review Dataset")

    st.write(
        "Upload a CSV containing a column named Customer_Review. "
        "You can use your existing e-commerce dataset."
    )

    uploaded_file = st.file_uploader(
        "Upload customer reviews CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:
            data = pd.read_csv(uploaded_file)

            if "Customer_Review" not in data.columns:
                st.error(
                    "The CSV must contain a Customer_Review column."
                )
            else:
                st.success(
                    f"Dataset loaded: {len(data)} records."
                )

                results = data["Customer_Review"].apply(
                    analyse_review
                ).apply(pd.Series)

                # Keep the original data and add predictions.
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
                analysed_data["Sentiment"] = (
                    results["Sentiment_Predicted"]
                )

                # Summary metrics
                sentiment_counts = (
                    analysed_data["Sentiment_Predicted"]
                    .value_counts()
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Total Reviews",
                    len(analysed_data)
                )
                col2.metric(
                    "Positive Reviews",
                    int(sentiment_counts.get("Positive", 0))
                )
                col3.metric(
                    "Negative Reviews",
                    int(sentiment_counts.get("Negative", 0))
                )

                st.subheader("Sentiment Distribution")

                chart_data = sentiment_counts.rename_axis(
                    "Sentiment"
                ).reset_index(name="Review Count")

                st.bar_chart(
                    chart_data.set_index("Sentiment")
                )

                st.subheader("Analysed Reviews")

                st.dataframe(
                    analysed_data,
                    use_container_width=True
                )

                # Show complaints needing attention.
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
                    use_container_width=True
                )

                # Download results for Power BI.
                csv_data = analysed_data.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label="Download Analysed CSV for Power BI",
                    data=csv_data,
                    file_name="customer_reviews_powerbi_v2.csv",
                    mime="text/csv"
                )

        except Exception as error:
            st.error(f"Unable to process the dataset: {error}")

# ----------------------------------------
# 6. FOOTER
# ----------------------------------------

st.divider()

st.caption(
    "Developed for the CAPACITI Week 4 Individual AI Project. "
    "Predictions use TextBlob polarity and should be validated "
    "before being used for business decisions."
)

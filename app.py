
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
        theme_rows = []

        for _, row in data.iterrows():
            for theme in row["Feedback_Themes"]:
                theme_rows.append({
                    "Theme": theme,
                    "Sentiment": row["Sentiment_Predicted"],
                    "Review": row["Customer_Review"],
                    "Product": row.get("Product", "Not provided"),
                    "Rating": row.get("Rating", "Not provided")
                })

        theme_data = pd.DataFrame(theme_rows)

        st.subheader("Feedback Themes")

        theme_counts = (
            theme_data["Theme"].value_counts()
            .sort_values(ascending=False)
        )

        st.bar_chart(theme_counts)

        st.caption(
            "A review may match multiple themes, so theme counts can "
            "exceed the total number of reviews."
        )

        chosen_theme = st.selectbox(
            "Choose a theme",
            theme_counts.index.tolist()
        )

        matching = theme_data[
            theme_data["Theme"] == chosen_theme
        ].copy()

        c1, c2, c3 = st.columns(3)
        c1.metric("Matching Comments", len(matching))
        c2.metric(
            "Positive Comments",
            int((matching["Sentiment"] == "Positive").sum())
        )
        c3.metric(
            "Negative Comments",
            int((matching["Sentiment"] == "Negative").sum())
        )

        sentiment_filter = st.selectbox(
            "Filter by sentiment",
            ["All", "Positive", "Negative", "Neutral"]
        )

        if sentiment_filter != "All":
            matching = matching[
                matching["Sentiment"] == sentiment_filter
            ]

        st.subheader(f"Customer Comments: {chosen_theme}")

        st.dataframe(
            matching,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "Themes are identified using keywords. A topic mention "
            "does not necessarily indicate a complaint. Read the "
            "original comment for context."
        )


# =====================================================
# 10. ISSUE MONITOR
# =====================================================

elif page == "🚨 Issue Monitor":

    st.header("🚨 Customer Issue Monitor")

    st.write(
        "Identify products with negative feedback and investigate "
        "the reviews that may need attention."
    )

    if project_data is None:
        st.error("The project dataset could not be loaded.")
        st.code(dataset_error or "Unknown loading error")

    else:
        data = project_data.copy()

        if "Product" in data.columns:
            data["Product_Display"] = (
                data["Product"].fillna("Unknown").astype(str)
            )
        else:
            data["Product_Display"] = "Product not provided"

        summary = data.groupby("Product_Display").agg(
            Total_Reviews=("Sentiment_Predicted", "size"),
            Negative_Reviews=(
                "Sentiment_Predicted",
                lambda values: (values == "Negative").sum()
            )
        )

        summary["Negative_Rate_Percent"] = (
            summary["Negative_Reviews"]
            / summary["Total_Reviews"] * 100
        ).round(1)

        summary = summary.sort_values(
            ["Negative_Rate_Percent", "Negative_Reviews"],
            ascending=False
        )

        st.subheader("Products by Negative-Review Rate")

        st.dataframe(
            summary.reset_index().rename(
                columns={"Product_Display": "Product"}
            ),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "A high negative-review rate is a signal to investigate, "
            "not proof that a product is defective. Products with few "
            "reviews should be interpreted cautiously."
        )

        st.divider()
        st.subheader("Reviews Flagged for Follow-up")

        complaints = data[data["Needs_Follow_Up"]].copy()

        columns = [
            c for c in [
                "Review_ID", "Product", "Rating",
                "Customer_Review", "Sentiment_Predicted"
            ] if c in complaints.columns
        ]

        st.write(f"Reviews flagged: **{len(complaints)}**")

        st.dataframe(
            complaints[columns],
            use_container_width=True,
            hide_index=True
        )


# =====================================================
# 11. BUSINESS ACTION PLAN
# =====================================================

elif page == "💡 Business Action Plan":

    st.header("💡 Business Action Plan")

    st.write(
        "Turn customer feedback into practical actions. "
        "The findings below are calculated from the loaded dataset. "
        "Suggested actions are starting points for business investigation."
    )

    if project_data is None:
        st.error("The project dataset could not be loaded.")
        st.code(dataset_error or "Unknown loading error")

    else:
        data = project_data.copy()

        # -------------------------------------------------
        # OVERALL BUSINESS SUMMARY
        # -------------------------------------------------

        total_reviews = len(data)

        negative_reviews = int(
            (data["Sentiment_Predicted"] == "Negative").sum()
        )

        positive_reviews = int(
            (data["Sentiment_Predicted"] == "Positive").sum()
        )

        negative_rate = (
            negative_reviews / total_reviews * 100
            if total_reviews else 0
        )

        st.subheader("Business Overview")

        c1, c2, c3 = st.columns(3)

        c1.metric("Reviews Analysed", total_reviews)
        c2.metric("Negative Reviews", negative_reviews)
        c3.metric("Negative Review Rate", f"{negative_rate:.1f}%")

        st.divider()

        # -------------------------------------------------
        # THEME-LEVEL EVIDENCE
        # -------------------------------------------------

        st.subheader("1. What Customers Are Talking About")

        theme_rows = []

        for _, row in data.iterrows():
            for theme in row["Feedback_Themes"]:
                theme_rows.append({
                    "Theme": theme,
                    "Sentiment": row["Sentiment_Predicted"],
                    "Review": row["Customer_Review"],
                    "Product": row.get("Product", "Not provided"),
                    "Rating": row.get("Rating", "Not provided")
                })

        theme_data = pd.DataFrame(theme_rows)

        if theme_data.empty:

            st.info("No feedback themes were found.")

        else:

            theme_summary = theme_data.groupby("Theme").agg(
                Matching_Comments=("Review", "size"),
                Negative_Comments=(
                    "Sentiment",
                    lambda s: (s == "Negative").sum()
                ),
                Positive_Comments=(
                    "Sentiment",
                    lambda s: (s == "Positive").sum()
                )
            )

            theme_summary["Negative_Rate_Percent"] = (
                theme_summary["Negative_Comments"]
                / theme_summary["Matching_Comments"] * 100
            ).round(1)

            theme_summary = theme_summary.sort_values(
                ["Negative_Comments", "Matching_Comments"],
                ascending=False
            )

            st.dataframe(
                theme_summary.reset_index(),
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "A review can contain multiple themes. Theme percentages "
                "describe comments assigned to that theme, not all reviews."
            )

        st.divider()

        # -------------------------------------------------
        # RULE-BASED RECOMMENDATIONS
        # -------------------------------------------------

        st.subheader("2. Recommended Business Actions")

        st.write(
            "Recommendations are generated from observed review themes "
            "and predicted sentiment. They should be checked by a person."
        )

        action_guidance = {
            "Product Quality": {
                "action": (
                    "Review quality-control procedures, inspect reported "
                    "defects, and investigate recurring damage or durability "
                    "concerns."
                ),
                "owner": "Quality or product team"
            },
            "Delivery": {
                "action": (
                    "Investigate delivery delays, compare expected and "
                    "actual delivery times, and review packaging or courier "
                    "handling where relevant."
                ),
                "owner": "Logistics or fulfilment team"
            },
            "Price and Value": {
                "action": (
                    "Review customer comments about value, explain product "
                    "benefits clearly, and assess whether the product meets "
                    "customer expectations for its price."
                ),
                "owner": "Product or commercial team"
            },
            "Customer Service": {
                "action": (
                    "Review support-related feedback, examine response "
                    "times and complaint handling, and investigate recurring "
                    "refund or service concerns."
                ),
                "owner": "Customer service team"
            },
            "Product Performance": {
                "action": (
                    "Investigate recurring performance issues, review "
                    "product instructions, and refer suspected defects to "
                    "the appropriate technical team."
                ),
                "owner": "Product or technical team"
            },
            "Positive Experience": {
                "action": (
                    "Review positive comments to identify what customers "
                    "value and consider how to maintain those strengths."
                ),
                "owner": "Product or customer experience team"
            },
            "Other / General Feedback": {
                "action": (
                    "Read a sample of these comments and identify whether "
                    "additional feedback themes should be added."
                ),
                "owner": "Customer insights team"
            }
        }

        recommendations = []

        for theme, counts in theme_summary.iterrows():

            matching_count = int(counts["Matching_Comments"])
            negative_count = int(counts["Negative_Comments"])
            positive_count = int(counts["Positive_Comments"])

            negative_percentage = (
                negative_count / matching_count * 100
                if matching_count else 0
            )

            # Only suggest investigating a problem if negative comments
            # actually exist for this theme.
            if negative_count > 0:

                guidance = action_guidance[theme]

                recommendations.append({
                    "Theme": theme,
                    "Matching_Comments": matching_count,
                    "Negative_Comments": negative_count,
                    "Negative_Rate_Percent": round(
                        negative_percentage, 1
                    ),
                    "Business_Action": guidance["action"],
                    "Suggested_Team": guidance["owner"],
                    "Action_Type": "Investigate negative feedback"
                })

            # Positive feedback can also guide business improvements.
            if positive_count > 0 and theme == "Positive Experience":

                guidance = action_guidance[theme]

                recommendations.append({
                    "Theme": theme,
                    "Matching_Comments": matching_count,
                    "Negative_Comments": negative_count,
                    "Negative_Rate_Percent": round(
                        negative_percentage, 1
                    ),
                    "Business_Action": guidance["action"],
                    "Suggested_Team": guidance["owner"],
                    "Action_Type": "Maintain strengths"
                })

        if recommendations:

            recommendation_data = pd.DataFrame(recommendations)

            recommendation_data = recommendation_data.sort_values(
                ["Negative_Comments", "Matching_Comments"],
                ascending=False
            )

            for _, recommendation in recommendation_data.iterrows():

                if recommendation["Action_Type"] == "Maintain strengths":
                    heading_icon = "✅"
                else:
                    heading_icon = "🔎"

                with st.expander(
                    f"{heading_icon} {recommendation['Theme']} — "
                    f"{recommendation['Action_Type']}"
                ):

                    st.write(
                        f"**Matching comments:** "
                        f"{int(recommendation['Matching_Comments'])}"
                    )

                    st.write(
                        f"**Negative comments:** "
                        f"{int(recommendation['Negative_Comments'])}"
                    )

                    st.write(
                        f"**Negative rate within this theme:** "
                        f"{recommendation['Negative_Rate_Percent']:.1f}%"
                    )

                    st.write("**Suggested action:**")
                    st.write(recommendation["Business_Action"])

                    st.write(
                        f"**Suggested team:** "
                        f"{recommendation['Suggested_Team']}"
                    )

                    evidence = theme_data[
                        theme_data["Theme"] == recommendation["Theme"]
                    ]

                    if recommendation["Action_Type"] == (
                        "Investigate negative feedback"
                    ):
                        evidence = evidence[
                            evidence["Sentiment"] == "Negative"
                        ]
                    else:
                        evidence = evidence[
                            evidence["Sentiment"] == "Positive"
                        ]

                    st.write("**Example customer comments:**")

                    if evidence.empty:
                        st.write("No matching comments are available.")
                    else:
                        for _, example in evidence.head(3).iterrows():
                            product_name = example["Product"]

                            st.markdown(
                                f"- “{example['Review']}” "
                                f"*(Product: {product_name})*"
                            )

            st.caption(
                "These are suggested investigations, not confirmed root "
                "causes. Keyword matching and sentiment predictions may "
                "be wrong; review the original comments before acting."
            )

        else:

            st.info(
                "No actionable themes with negative comments were found "
                "by the current rules. Review the comments manually and "
                "consider improving the theme keywords."
            )

        st.divider()

        # -------------------------------------------------
        # PRODUCT-SPECIFIC BUSINESS FINDINGS
        # -------------------------------------------------

        st.subheader("3. Products to Investigate")

        if "Product" in data.columns:

            data["Product_Display"] = (
                data["Product"].fillna("Unknown").astype(str)
            )

            product_summary = data.groupby("Product_Display").agg(
                Total_Reviews=("Sentiment_Predicted", "size"),
                Negative_Reviews=(
                    "Sentiment_Predicted",
                    lambda s: (s == "Negative").sum()
                ),
                Positive_Reviews=(
                    "Sentiment_Predicted",
                    lambda s: (s == "Positive").sum()
                )
            )

            product_summary["Negative_Rate_Percent"] = (
                product_summary["Negative_Reviews"]
                / product_summary["Total_Reviews"] * 100
            ).round(1)

            product_summary = product_summary.sort_values(
                ["Negative_Reviews", "Negative_Rate_Percent"],
                ascending=False
            )

            st.write(
                "Products are listed by negative-review count first. "
                "Consider the total number of reviews when comparing rates."
            )

            st.dataframe(
                product_summary.reset_index().rename(
                    columns={"Product_Display": "Product"}
                ),
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "A high negative-review rate does not prove that a product "
                "is defective. Use the results to prioritise investigation."
            )

        else:

            st.info(
                "The dataset has no Product column, so product-level "
                "recommendations cannot be generated."
            )

        st.divider()

        # -------------------------------------------------
        # EXPORT ACTION PLAN
        # -------------------------------------------------

        st.subheader("4. Download Business Action Plan")

        if recommendations:

            report = pd.DataFrame(recommendations)

            st.download_button(
                "⬇️ Download Business Action Plan (CSV)",
                data=report.to_csv(index=False).encode("utf-8"),
                file_name="customer_experience_action_plan.csv",
                mime="text/csv"
            )

        else:

            st.info(
                "There are no recommendations to export from the current "
                "rules. Review the dataset or adjust the theme keywords."
            )


# =====================================================
# 12. INDIVIDUAL REVIEW ANALYSIS
# =====================================================

elif page == "🔍 Analyse a Review":

    st.header("🔍 Analyse an Individual Review")

    st.write(
        "Enter a customer comment to estimate its sentiment "
        "and identify possible feedback themes."
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

            st.warning("Please enter a customer review first.")

        else:

            result = analyse_review(review)

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Predicted Sentiment",
                result["Sentiment_Predicted"]
            )

            c2.metric(
                "Sentiment Polarity",
                f'{result["Sentiment_Polarity"]:.3f}'
            )

            c3.metric(
                "Needs Follow-up",
                "Yes" if result["Needs_Follow_Up"] else "No"
            )

            st.subheader("Customer Comment")
            st.info(review)

            st.write(
                "**Possible feedback themes:** "
                + ", ".join(detect_themes(review))
            )

            if result["Sentiment_Predicted"] == "Negative":

                st.warning(
                    "This review may need attention. Investigate "
                    "the customer's concern."
                )

            elif result["Sentiment_Predicted"] == "Positive":

                st.success(
                    "This review expresses positive sentiment."
                )

            else:

                st.info("This review was classified as neutral.")


# =====================================================
# 13. UPLOAD AND ANALYSE CSV
# =====================================================

else:

    st.header("📁 Analyse a Customer Review Dataset")

    st.write(
        "Upload a CSV file containing a column named Customer_Review."
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

                results = data["Customer_Review"].apply(
                    analyse_review
                ).apply(pd.Series)

                analysed = data.copy()

                analysed["Sentiment_Polarity"] = (
                    results["Sentiment_Polarity"]
                )

                analysed["Sentiment_Predicted"] = (
                    results["Sentiment_Predicted"]
                )

                analysed["Needs_Follow_Up"] = (
                    results["Needs_Follow_Up"]
                )

                analysed["Feedback_Themes"] = (
                    analysed["Customer_Review"].apply(detect_themes)
                )

                st.success(
                    f"Successfully analysed {len(analysed)} reviews."
                )

                counts = (
                    analysed["Sentiment_Predicted"].value_counts()
                    .reindex(
                        ["Positive", "Neutral", "Negative"],
                        fill_value=0
                    )
                )

                c1, c2, c3, c4 = st.columns(4)

                c1.metric("Total Reviews", len(analysed))
                c2.metric("Positive", int(counts["Positive"]))
                c3.metric("Negative", int(counts["Negative"]))
                c4.metric("Neutral", int(counts["Neutral"]))

                st.subheader("Sentiment Distribution")
                st.bar_chart(counts)

                st.subheader("Analysed Reviews")

                st.dataframe(
                    analysed,
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    "⬇️ Download Analysed CSV for Power BI",
                    data=analysed.to_csv(index=False).encode("utf-8"),
                    file_name="customer_reviews_analysed.csv",
                    mime="text/csv"
                )

        except Exception as error:

            st.error(f"Unable to process the dataset: {error}")


# =====================================================
# 14. FOOTER
# =====================================================

st.divider()

st.caption(
    "CAPACITI Week 4 Individual AI Project. Sentiment uses TextBlob "
    "polarity and simple phrase rules. Feedback themes use keywords. "
    "These are estimates, not a trained machine-learning classifier. "
    "Validate findings before making business decisions."
)



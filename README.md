# AI Customer Review Analyzer

## CAPACITI Week 4 Individual AI Project

**Industry: ** E-commerce  
**Technologies: ** Python, Streamlit, TextBlob, Pandas, Power BI

## Project Overview
The AI Customer Review Analyzer is a prototype that analyses customer feedback and classifies reviews as positive, negative, or neutral. It helps identify negative reviews that may require follow-up and presents customer sentiment insights through a Power BI dashboard.

## Features
- Analyze individual customer reviews.
- Upload and analyze a CSV dataset.
- Classify reviews by sentiment.
- Display sentiment distribution and customer review summaries.
- Flag negative reviews for follow-up.
- Export analysed results for Power BI reporting.

## Project Files
- `app.py` — Streamlit application source code.
- `AI_Customer_Review_Analyzer_v2.pbix` — Power BI dashboard.
- `customer_reviews_powerbi_v2 (2).csv` — analysed customer review dataset.
- `CAPACITI Week 4 Individual Project.docx` — project report.

## Dataset
The prototype was tested using an e-commerce customer review dataset containing 400 records.

## How to Run the Application
1. Install Python.
2. Install the required packages: `pip install streamlit pandas textblob`
3. Open a terminal in the project folder.
4. Run: `python -m streamlit run app.py`

## Limitations
Sentiment predictions use TextBlob polarity and additional phrase-based rules. This is a prototype, so predictions may be incorrect, especially for mixed, sarcastic, or context-dependent reviews. Results should be validated before business decisions are made.

## Author
Developed as a CAPACITI Week 4 Individual AI Project.

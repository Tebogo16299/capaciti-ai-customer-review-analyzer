I Customer Review Analyzer
CAPACITI Week 4 Individual AI Project
Project type: E-commerce customer-experience analytics prototype
Live demo
https://capaciti-ai-customer-review-analyzer-dwykm7tru8bvmhgcyvbohw.streamlit.app/
Project overview
The AI Customer Review Analyzer helps users review customer feedback more efficiently. It analyses a single customer review or a CSV dataset, assigns a sentiment label, highlights negative reviews for possible follow-up, and exports analysed results for further exploration in Power BI.

The goal is to turn unstructured customer feedback into a clearer view of customer sentiment and potential service or product issues.
Problem statement
E-commerce businesses can receive large numbers of customer reviews. Reading every review manually can take time, and negative experiences may be difficult to identify quickly. This prototype provides an initial sentiment summary and helps teams find reviews that may need human attention.
Main features
- Individual review analysis: enter a review and receive a predicted sentiment and polarity score.
- CSV analysis: upload a CSV file containing a Customer_Review column and analyse multiple reviews.
- Sentiment classification: labels reviews as Positive, Negative, or Neutral.
- Follow-up flagging: highlights negative classifications for human review.
- Results export: download analysed records as a CSV file.
- Power BI reporting: explore sentiment distribution and patterns by product category, customer rating, and purchase channel using the prepared dataset/dashboard.
How it works
1. The user enters a review or uploads a CSV file.
2. Python and Pandas prepare and process the text and tabular data.
3. TextBlob estimates text polarity; selected phrase-based rules adjust some expressions that polarity alone may misread.
4. The application assigns a sentiment label and, for dataset analysis, adds fields that support follow-up and reporting.
5. The user downloads the analysed CSV and can use it in Power BI.
Tools and technologies
- Python
- Streamlit
- Pandas
- TextBlob
- CSV data
- Microsoft Power BI
- GitHub for project documentation and version control
Dataset and dashboard snapshot
The current dashboard snapshot reports 400 reviews classified as:
- Positive: 290
- Negative: 87
- Neutral: 23
These are the prototype's current classifications for the dataset, not verified ground-truth results or a measure of model accuracy. Dashboard totals should be checked against the exact CSV version used for the analysis.
Limitations
This is a rule-assisted sentiment prototype, not a machine-learning classifier trained on a labelled training dataset. TextBlob polarity and phrase rules can misinterpret context, sarcasm, negation, or mixed opinions. Negative classifications should therefore be treated as candidates for human follow-up, not automatically confirmed complaints. The prototype is not connected to a live e-commerce platform and does not automatically contact customers.
Run the application locally
1. Install Python and the required packages in your environment.
2. Install the packages used by the app, including Streamlit, Pandas, and TextBlob.
3. Open a terminal in the project folder.
4. Run:
   streamlit run app.py
If your environment reports a missing package, install that package in the same Python environment and run the command again.

Project outcome
The project demonstrates an end-to-end prototype workflow: customer review input, rule-assisted sentiment analysis, CSV processing, negative-review triage, downloadable results, and dashboard-based exploration. Its outputs are intended to support human investigation and decision-making rather than replace it.

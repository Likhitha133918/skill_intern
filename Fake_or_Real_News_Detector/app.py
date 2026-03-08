import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Page Config
st.set_page_config(page_title="Veritas: Fake News Detector", page_icon="🛡️")

st.title("🛡️ Veritas: Fake News Detector")
st.markdown("Analyze news headlines for authenticity using Machine Learning.")

# 1. Load and Train Model (Cached for speed)
@st.cache_resource
def train_model():
    try:
        true_df = pd.read_csv('archive/True.csv')
        fake_df = pd.read_csv('archive/Fake.csv')
        
        true_df['label'] = 1
        fake_df['label'] = 0
        
        df = pd.concat([true_df, fake_df]).reset_index(drop=True)
        X = df['title']
        y = df['label']
        
        vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
        X_tfidf = vectorizer.fit_transform(X)
        
        model = LogisticRegression()
        model.fit(X_tfidf, y)
        
        return vectorizer, model
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

vectorizer, model = train_model()

# Sidebar
st.sidebar.header("About")
st.sidebar.info("This app uses a Logistic Regression model trained on your True/Fake news dataset.")

# Main UI
if vectorizer and model:
    headline = st.text_input("Enter a news headline to analyze:", placeholder="e.g., NASA discovers water on Mars...")
    
    if st.button("Analyze Headline"):
        if headline:
            # Predict
            tfidf_input = vectorizer.transform([headline])
            prediction = model.predict(tfidf_input)
            prob = model.predict_proba(tfidf_input)
            
            label = "REAL" if prediction[0] == 1 else "FAKE"
            confidence = prob[0][prediction[0]] * 100
            
            # Show Result
            if label == "REAL":
                st.success(f"### Result: {label}")
            else:
                st.error(f"### Result: {label}")
                
            st.write(f"**Confidence Score:** {confidence:.2f}%")
        else:
            st.warning("Please enter a headline first.")

    # Batch Processing
    st.divider()
    st.subheader("📁 Batch Processing")
    uploaded_file = st.file_uploader("Upload a CSV for batch analysis", type="csv")
    
    if uploaded_file:
        batch_df = pd.read_csv(uploaded_file)
        if 'title' in batch_df.columns or 'headline' in batch_df.columns:
            col_name = 'title' if 'title' in batch_df.columns else 'headline'
            
            with st.spinner("Analyzing batch..."):
                tfidf_batch = vectorizer.transform(batch_df[col_name].astype(str))
                batch_df['Prediction'] = ["REAL" if p == 1 else "FAKE" for p in model.predict(tfidf_batch)]
                
            st.write(batch_df.head())
            st.download_button("Download Results", batch_df.to_csv(index=False), "results.csv", "text/csv")
        else:
            st.error("CSV must have a 'title' or 'headline' column.")
else:
    st.warning("Please ensure your 'archive' folder with True.csv and Fake.csv is present.")
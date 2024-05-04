import streamlit as st
import os
import requests
import pandas as pd
from utils import st_def

st.set_page_config(page_title='👋 AI', page_icon="🚀")
st.title('🔍 AI')
st_def.st_logo()

st.markdown("🚀) 📄Rule Extraction📚: Python Libraries  Approaches🍨 ")

# Input box for URL
tab1, tab2 = st.tabs(["🍨CSV", "📰SingleStore"])
with tab1:
    default_url = 'https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/data/AG_news_samples.csv'
    url = st.text_input("Enter URL", default_url)

    # File path
    file_path = './data/AG_news_samples.csv'

    # Check if file exists
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.success("File loaded successfully.")
    else:
        df = None

    # Download button
    if st.button("Download"):
        if not os.path.exists(file_path):
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                df = pd.read_csv(file_path)
                st.success("File downloaded successfully.")
            else:
                st.error(f"Failed to download file: {response.status_code}")
        else:
            st.info("File already exists in the system.")
            df = pd.read_csv(file_path)
            st.text(df.head())

with tab2:
    if df is not None:
        data = df.to_dict(orient='records')
        st.write(data[0])

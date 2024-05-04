import streamlit as st
from streamlit_extras.stateful_button import button
from utils import st_def

st.set_page_config(page_title='👋 AI',  page_icon="🚀",)
st.title('🔍 AI')
st_def.st_logo()
#------------------------------------------------------------------------------------------------
st.markdown("We use **hybrid search**, a classic RAG approach. Through this method, we aim to mitigate instances of hallucination, ensuring precise and relevant results.")

if button("Button 1", key="button1"):
    st.markdown("🚀) 🍨📄Rule Extraction📚: Python Libraries  Approaches📰🍨 ")

    if button("Button 2", key="button2"):
        st.image("./images/zhang.gif")

        if button("Button 3", key="button3"):
            st.write("All 3 buttons are pressed")



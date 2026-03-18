import streamlit as st
import google.genai as genai
import sys
from io import StringIO
import contextlib

# 1. Page Config
st.set_page_config(page_title="VibeCoder Pro", page_icon="🚀", layout="wide")

# --- UPDATE: GET THE SECRET KEY ---
# This line grabs the key you just saved in the Streamlit Settings
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Missing API Key! Please add GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)
# ----------------------------------

st.title("🚀 VibeCoder Pro")
st.subheader("Describe your app, and I'll build & run it instantly.")

# 2. Simplified Sidebar (No more API key box!)
with st.sidebar:
    st.success("API Key Connected ✅")
    model_choice = st.selectbox("Choose Brain", ["gemini-3-flash-preview", "gemini-2.0-flash"])
    st.info("Now anyone can use your app without needing their own key!")

# 3. The Main Interface
vibe = st.text_area("What's the vibe today?", placeholder="e.g. A unit converter for kitchen recipes...")

if st.button("Build & Run App"):
    with st.spinner("✨ Vibe coding in progress..."):
        # Requesting code
        response = client.models.generate_content(
            model=model_choice,
            contents=f"Write a Python script for: {vibe}. Output ONLY raw code. No talk, no markdown."
        )
        code = response.text.replace("```python", "").replace("```", "").strip()

        # Displaying the generated code
        st.code(code, language="python")

        # Execute and show output
        st.info("🏃 Running Output:")
        output_buffer = StringIO()
        try:
            with contextlib.redirect_stdout(output_buffer):
                exec(code)
            st.success(output_buffer.getvalue())
        except Exception as e:
            st.error(f"Error running app: {e}")

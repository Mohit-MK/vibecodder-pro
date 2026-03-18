import streamlit as st
import google.genai as genai
import sys
from io import StringIO
import contextlib

# 1. Page Config (The "Professional" look)
st.set_page_config(page_title="VibeCoder Pro", page_icon="🚀", layout="wide")

st.title("🚀 VibeCoder Pro")
st.subheader("Describe your app, and I'll build & run it instantly.")

# 2. Sidebar for settings
with st.sidebar:
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    model_choice = st.selectbox("Choose Brain", ["gemini-3-flash-preview", "gemini-2.0-flash"])

# 3. The Main Interface
vibe = st.text_area("What's the vibe today?", placeholder="e.g. A unit converter for kitchen recipes...")

if st.button("Build & Run App"):
    if not api_key:
        st.error("Please enter an API Key in the sidebar!")
    else:
        client = genai.Client(api_key=api_key)
        
        with st.spinner("✨ Vibe coding in progress..."):
            # Requesting code
            response = client.models.generate_content(
                model=model_choice,
                contents=f"Write a Python script for: {vibe}. Output ONLY raw code. No talk."
            )
            code = response.text.replace("```python", "").replace("```", "").strip()

            # Displaying the generated code
            st.code(code, language="python")

            # SAFETY & RUN: We execute the code and capture the output
            st.info("🏃 Running Output:")
            output_buffer = StringIO()
            try:
                with contextlib.redirect_stdout(output_buffer):
                    exec(code)
                st.success(output_buffer.getvalue())
            except Exception as e:
                st.error(f"Error running app: {e}")

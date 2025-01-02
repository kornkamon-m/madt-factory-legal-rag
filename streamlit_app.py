import streamlit as st
import google.generativeai as genai

with st.sidebar:
    # Capture Gemini API Key 
    gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password") 

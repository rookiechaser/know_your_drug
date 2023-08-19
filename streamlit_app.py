import streamlit as st
import requests

st.title('Streamlit App')

# Fetch data from the Flask API
response = requests.get('http://localhost:5000/')
data = response.json()

st.write('Data from Flask API:', data)

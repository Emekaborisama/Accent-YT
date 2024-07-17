import requests
import streamlit as st
from st_btn_select import st_btn_select

# Fetch voice data from the API
url = "https://api.elevenlabs.io/v1/voices"
response = requests.get(url)
result = response.json()

# Filter the relevant data


# Streamlit app
st.title('YouTube Accent Switch')

st.write("Enter YouTube link:")
youtube_link = st.text_input("YouTube Link", placeholder="Enter YouTube link")



st.write("Choose a voice:")
option = st_btn_select(('option1', 'option2', 'option3', 'option4'), index=2)
st.write(f'Selected option: {option}')

st.button("Fetch Video")

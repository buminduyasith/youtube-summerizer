from services.processVideo import processVideo
import streamlit as st


st.title("Educational Video Summarizer App")

youtube_link = st.text_input("Enter a YouTube link:")

if st.button("Submit"):
    if youtube_link:
        x = processVideo(youtube_link)
        st.markdown(f"[Click here to open the video]({youtube_link})")
        st.markdown(x)
        
    else:
        st.warning("Please enter a valid YouTube link.")
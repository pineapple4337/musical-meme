import streamlit as st
import yt_dlp
import os
import glob

# Set up clean page configuration
st.set_page_config(page_title="TikTok Downloader", page_icon="🎬", layout="centered")
st.title("🎬 Personal TikTok Downloader")
st.write("Tap the input field to paste your TikTok link.")

# Initialize session state for the URL input if it doesn't exist
if "tiktok_url" not in st.session_state:
    st.session_state.tiktok_url = ""

# Callback function to clear the input
def clear_text():
    st.session_state.tiktok_url = ""

# Main text input field linked to session state
url = st.text_input(
    "Paste TikTok URL here:", 
    value=st.session_state.tiktok_url,
    placeholder="https://www.tiktok.com/...", 
    key="url_input"
)

# If the text input changes, update our tracking state
if url != st.session_state.tiktok_url:
    st.session_state.tiktok_url = url

# Clear button to easily reset for the next link
if st.session_state.tiktok_url:
    st.button("🗑️ Clear Link & Start Over", on_click=clear_text, use_container_width=True)

# Download Logic
if st.session_state.tiktok_url:
    with st.spinner("Processing video from TikTok CDN... Please wait."):
        outtmpl = 'downloaded_video_tmp_%(id)s.%(ext)s'
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': outtmpl,
            'restrictfilenames': True,
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([st.session_state.tiktok_url])
            
            target_files = glob.glob("downloaded_video_tmp_*")
            
            if target_files:
                video_file_path = target_files[0]
                
                with open(video_file_path, "rb") as video_file:
                    video_bytes = video_file.read()
                
                st.success("Video fetched successfully!")
                
                st.download_button(
                    label="📥 Save Video to Device",
                    data=video_bytes,
                    file_name="tiktok_clean.mp4",
                    mime="video/mp4"
                )
                
                os.remove(video_file_path)
            else:
                st.error("Could not locate downloaded file.")
        except Exception as e:
            st.error(f"Error fetching video: {e}")

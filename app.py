import streamlit as st
import yt_dlp
import os
import glob

# Set up clean page configuration
st.set_page_config(page_title="TikTok Downloader", page_icon="🎬", layout="centered")
st.title("🎬 Personal TikTok Downloader")
st.write("Paste a TikTok link below to fetch a watermark-free video.")

# Initialize session state for tracking the active URL
if "tiktok_url" not in st.session_state:
    st.session_state.tiktok_url = ""

# Callback function to clear the input field completely
def clear_text():
    st.session_state.tiktok_url = ""

# Main link input bar - stretching full width for easier pasting on mobile
url_input = st.text_input(
    "TikTok URL:", 
    value=st.session_state.tiktok_url,
    placeholder="https://www.tiktok.com/...", 
    key="url_field"
)

# 🚀 The prominent physical button you wanted to tap!
fetch_button = st.button("🚀 Fetch Video", type="primary", use_container_width=True)

# 🗑️ Separate Clear button positioned safely below to prevent accidental misclicks
st.write("")
if url_input:
    st.button("🗑️ Clear Input Line", on_click=clear_text, use_container_width=True)

# Run the download logic ONLY if the user explicitly hits the physical Fetch Button
if fetch_button and url_input:
    st.session_state.tiktok_url = url_input
    
    with st.spinner("Processing video from TikTok CDN... Please wait."):
        # Unique matching ensures zero cross-device multi-user download interference
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
            
            # Find the specific temporary file that was just created
            target_files = glob.glob("downloaded_video_tmp_*")
            
            if target_files:
                video_file_path = target_files[0]
                
                # Stream file straight via local runtime memory buffers
                with open(video_file_path, "rb") as video_file:
                    video_bytes = video_file.read()
                
                st.success("Video fetched successfully!")
                
                # Direct browser stream hook for native iOS downloading storage rules
                st.download_button(
                    label="📥 Save Video to Device",
                    data=video_bytes,
                    file_name="tiktok_clean.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )
                
                # Purge local block storage cache immediately
                os.remove(video_file_path)
            else:
                st.error("Could not locate downloaded file.")
        except Exception as e:
            st.error(f"Error fetching video: {e}")

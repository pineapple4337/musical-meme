import streamlit as st
import yt_dlp
import os
import glob

# Set up clean page configuration
st.set_page_config(page_title="TikTok Downloader", page_icon="🎬", layout="centered")
st.title("🎬 TikTok Downloader")
st.write("Paste a TikTok link below to fetch a watermark-free video.")

# Callback function to clear the text input natively using its state key
def clear_text():
    st.session_state["url_field"] = ""

# Main link input bar - stretching full width for easier pasting on mobile
# We use the key "url_field" to track its value directly
url_input = st.text_input(
    "TikTok URL:", 
    placeholder="https://www.tiktok.com/...", 
    key="url_field"
)

# 🚀 The prominent physical button to trigger download
fetch_button = st.button("Fetch Video", type="primary", use_container_width=True)

# 🗑️ Separate Clear button positioned safely below
st.write("")
if url_input:
    st.button("🗑️ Clear Input Line", on_click=clear_text, use_container_width=True)

# Run the download logic ONLY if the user explicitly hits the physical Fetch Button
if fetch_button and url_input:
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
                ydl.download([url_input])
            
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

import streamlit as st
import yt_dlp
import os
import glob

st.set_page_config(page_title="TikTok Downloader", page_icon="🎬", layout="centered")
st.title("🎬 Personal TikTok Downloader")
st.write("Paste a TikTok link below to fetch a watermark-free video.")

# Input field for the URL
url = st.text_input("TikTok URL:", placeholder="https://www.tiktok.com/...")

if url:
    with st.spinner("Processing video from TikTok CDN... Please wait."):
        # Unique template name to avoid file collision
        outtmpl = 'downloaded_video_tmp_%.(ext)s'
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': outtmpl,
            'restrictfilenames': True,
            'quiet': True,
        }
        
        try:
            # 1. Download video from TikTok to your server/computer local disk
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Find the downloaded file (handles extension differences like .mp4 or .mkv)
            target_files = glob.glob("downloaded_video_tmp_*")
            
            if target_files:
                video_file_path = target_files[0]
                
                # 2. Read the file bytes to serve them to the web browser
                with open(video_file_path, "rb") as video_file:
                    video_bytes = video_file.read()
                
                st.success("Video fetched successfully!")
                
                # 3. Create a native browser download button
                st.download_button(
                    label="📥 Save Video to Device",
                    data=video_bytes,
                    file_name="tiktok_clean.mp4",
                    mime="video/mp4"
                )
                
                # Clean up the server file afterward
                os.remove(video_file_path)
            else:
                st.error("Could not locate downloaded file.")
                
        except Exception as e:
            st.error(f"Error fetching video: {e}")


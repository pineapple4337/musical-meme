import streamlit as st
import yt_dlp
import os
import glob

# Set up clean page configuration
st.set_page_config(page_title="TikTok Downloader", page_icon="🎬", layout="centered")
st.title("🎬 Personal TikTok Downloader")
st.write("Paste a TikTok link below to fetch a watermark-free video.")

url = st.text_input("TikTok URL:", placeholder="https://www.tiktok.com/...")

if url:
    with st.spinner("Processing video from TikTok CDN... Please wait."):
        # Using %(id)s prevents file conflicts if multiple devices use the cloud app simultaneously
        outtmpl = 'downloaded_video_tmp_%(id)s.%(ext)s'
        
        ydl_opts = {
            # Force standard MP4 format container so iOS Safari can play and save it natively
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': outtmpl,
            'restrictfilenames': True,
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Find the specific temporary file that was just created
            target_files = glob.glob("downloaded_video_tmp_*")
            
            if target_files:
                video_file_path = target_files[0]
                
                # Read the file bytes directly into memory
                with open(video_file_path, "rb") as video_file:
                    video_bytes = video_file.read()
                
                st.success("Video fetched successfully!")
                
                # Stream the file directly to your browser download manager
                st.download_button(
                    label="📥 Save Video to Device",
                    data=video_bytes,
                    file_name="tiktok_clean.mp4",
                    mime="video/mp4"
                )
                
                # Clean up the cloud server storage instantly after memory transfer
                os.remove(video_file_path)
            else:
                st.error("Could not locate downloaded file.")
        except Exception as e:
            st.error(f"Error fetching video: {e}")

import streamlit as st
import streamlit.components.v1 as components
import yt_dlp
import os
import glob

# Set up clean page configuration
st.set_page_config(page_title="TikTok Downloader", page_icon="🎬", layout="centered")
st.title("🎬 Personal TikTok Downloader")
st.write("Paste a TikTok link below to fetch a watermark-free video.")

# Initialize session state for the URL input if it doesn't exist
if "tiktok_url" not in st.session_state:
    st.session_state.tiktok_url = ""

# Check for a URL passed from our custom JavaScript paste button
query_params = st.query_params
if "pasted_url" in query_params:
    st.session_state.tiktok_url = query_params["pasted_url"]
    # Clear the query param immediately so it doesn't get stuck on reload
    st.query_params.clear()

# Callback function to clear the input
def clear_text():
    st.session_state.tiktok_url = ""

# Main layout
url = st.text_input(
    "TikTok URL:", 
    placeholder="https://www.tiktok.com/...", 
    key="tiktok_url"
)

# Control buttons layout side-by-side
col1, col2 = st.columns(2)

with col1:
    # 📋 JavaScript Clipboard Paste Button
    # This securely requests clipboard text via your mobile browser and sends it to Streamlit
    paste_html = """
    <button id="paste-btn" style="
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border: none;
        padding: 0.5rem;
        border-radius: 0.5rem;
        cursor: pointer;
        font-weight: 500;
        font-family: sans-serif;
    ">📋 Paste from Clipboard</button>

    <script>
    document.getElementById('paste-btn').addEventListener('click', async () => {
        try {
            const text = await navigator.clipboard.readText();
            if (text) {
                // Send the text back to Streamlit via URL parameters
                const url = new URL(window.parent.location.href);
                url.searchParams.set('pasted_url', text);
                window.parent.location.href = url.href;
            }
        } catch (err) {
            alert("Allow clipboard access or paste manually. Browser blocked clipboard access: " + err);
        }
    });
    </script>
    """
    components.html(paste_html, height=45)

with col2:
    st.button("🗑️ Clear Link", on_click=clear_text, use_container_width=True)

# Download Logic
if url:
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
                ydl.download([url])
            
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

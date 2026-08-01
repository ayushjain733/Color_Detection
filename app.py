import streamlit as st
import cv2
import numpy as np
from PIL import Image
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode

# --- Helper Functions ---
def get_limits(color, tolerance):
    """
    Takes a BGR color and a tolerance to generate lower and upper HSV limits.
    """
    c = np.uint8([[color]])
    hsv_c = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    hue = hsv_c[0][0][0]
    
    # OpenCV Hue ranges from 0 to 179. We clamp the values to prevent errors.
    lower_hue = max(0, hue - tolerance)
    upper_hue = min(179, hue + tolerance)
    
    # We maintain 100-255 for Saturation and Value to avoid detecting black/white/gray
    lower_limit = np.array([lower_hue, 100, 100], dtype=np.uint8)
    upper_limit = np.array([upper_hue, 255, 255], dtype=np.uint8)
    
    return lower_limit, upper_limit


# --- WebRTC Video Processor ---
class ColorTracker(VideoProcessorBase):
    def __init__(self):
        # Default tracking color (Yellow in BGR) and tolerance
        self.target_color_bgr = [0, 255, 255]
        self.tolerance = 10

    def recv(self, frame):
        # Convert incoming browser frame to a numpy array (BGR format)
        img = frame.to_ndarray(format="bgr24")
        
        # Apply your exact tracking logic
        hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower, upper = get_limits(self.target_color_bgr, self.tolerance)
        mask = cv2.inRange(hsvImage, lower, upper)
        
        # Find bounding box using PIL (as per your original code)
        mask_ = Image.fromarray(mask)
        bbox = mask_.getbbox()
        
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 5)

        # Return the processed frame back to the browser
        return av.VideoFrame.from_ndarray(img, format="bgr24")


# --- Streamlit UI ---
st.set_page_config(page_title="Real-Time Color Tracker", layout="wide")
st.title("📷 Real-Time Color Tracker")
st.write("Allow webcam access, pick a color using the sliders below, and watch the app track it in real time!")

# Create a UI layout with columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Select Color (RGB)")
    # RGB inputs (sliders also act as manual number inputs)
    r = st.slider("Red", 0, 255, 255)
    g = st.slider("Green", 0, 255, 255)
    b = st.slider("Blue", 0, 255, 0)
    
    st.subheader("2. Detection Intensity")
    # The 4th parameter for intensity (Hue tolerance)
    tolerance = st.slider("Tolerance (Hue Range)", 1, 50, 10, help="Higher values detect a broader range of similar shades.")
    
    # Show a visual preview of the selected color
    st.markdown(f"""
        <div style="background-color: rgb({r}, {g}, {b}); 
                    width: 100%; height: 50px; 
                    border-radius: 5px; border: 1px solid #ccc;">
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Google's public STUN server ensures WebRTC connects properly over different networks
    RTC_CONFIGURATION = {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    
    # Initialize the WebRTC streamer
    ctx = webrtc_streamer(
        key="color-tracker",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=ColorTracker,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True
    )

    # Pass the Streamlit UI values dynamically into the running WebRTC video thread
    if ctx.video_processor:
        # Note: Streamlit UI uses RGB, but OpenCV uses BGR. We reverse it here!
        ctx.video_processor.target_color_bgr = [b, g, r]
        ctx.video_processor.tolerance = tolerance
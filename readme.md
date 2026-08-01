# 📷 Real-Time Color Tracker (Streamlit + OpenCV)

A local web application built with Streamlit and OpenCV that uses your webcam to track custom colors in real-time. 

## ✨ Features
- **Live Video Processing**: Uses `streamlit-webrtc` to stream and process your webcam feed frame-by-frame securely in your browser.
- **Custom Color Selection**: Interactive RGB sliders allow you to pick the exact color you want to track.
- **Adjustable Tolerance**: Control the Hue range intensity to detect broader or narrower shades of your chosen target color.
- **Real-Time Tracking**: Instantly computes masks and draws a green bounding box around the detected object in the live video stream.

## 🛠️ Prerequisites
- Python 3.8 or higher
- A working webcam attached to your local machine

## 🚀 Installation & Setup

1. **Clone or download this repository** to your local machine.
2. **Navigate to the project directory** in your terminal:
   ```bash
   cd path/to/your/project
   ```
3. **Create a virtual environment** (Highly Recommended):
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate  
   
   # On Windows:
   venv\Scripts\activate
   ```
4. **Install the required dependencies**:
   Ensure you have your `requirements.txt` file saved in the directory, then run:
   ```bash
   pip install -r requirements.txt
   ```

## 📋 Required `requirements.txt`
```text
streamlit==1.32.0
opencv-python-headless==4.9.0.80
streamlit-webrtc==0.47.0
numpy==1.26.4
Pillow==10.2.0
av==11.0.0
```
*(Note: `opencv-python-headless` is used instead of the standard OpenCV package to prevent conflicts with Streamlit environments.)*

## 🎮 How to Run

Start the Streamlit development server locally by running the following command in your terminal:

```bash
streamlit run app.py
```

The application will automatically open in your default web browser (typically at `http://localhost:8501`). 

1. Grant the browser permission to access your webcam.
2. Click **Start** on the WebRTC video player.
3. Adjust the RGB sliders and Tolerance to start tracking objects of that color!

## ⚠️ Note on Cloud Deployment
This project is currently configured for **local execution only**. 

Because it uses WebRTC for real-time video streaming, deploying this app to a cloud platform (like Streamlit Community Cloud) without further configuration will result in connection timeouts. 

To deploy this publicly, you must configure a **TURN server** (using a provider like Metered.ca or Twilio) and pass the `iceServers` configuration into the `webrtc_streamer` function to bypass public network firewalls and NATs.

## Author

**Ayush Jain**

[LinkedIn](https://linkedin.com/in/ayush-jain-ba1050253)

[Github](https://github.com/ayushjain733)
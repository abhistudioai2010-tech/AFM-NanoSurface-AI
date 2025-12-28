import streamlit as st
import numpy as np
import plotly.graph_objects as go
from PIL import Image
import google.generativeai as genai

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="AFM NanoSurface AI Lab", layout="wide")

# This makes the UI look like a high-tech lab dashboard
st.markdown("""
<style>
    .main {background-color: #0b0f19;}
    h1, h2, h3 {color: #00f7ff !important; font-family: 'Courier New', Courier, monospace;}
    .stMarkdown {color: #e0e0e0;}
    div.stButton>button {
        background: linear-gradient(45deg, #00f7ff, #0080ff);
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧬 AFM NanoSurface AI Lab — IIT Madras")
st.write("Professional Nano-Scale Topography & AI-Driven Analysis")

# ---------------- SIDEBAR ----------------
st.sidebar.header("🤖 Gemini AI Scientist")
API_KEY = st.sidebar.text_input("Enter Gemini API Key", type="password")

if API_KEY:
    genai.configure(api_key=API_KEY)
    # UPDATED: Using 1.5-flash for faster, better image vision
    model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- MAIN PANEL ----------------
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("Upload AFM Height Image (PNG/JPG)", type=["png","jpg","jpeg"])

if uploaded_file:
    # Process Image
    img = Image.open(uploaded_file)
    # Convert to grayscale for height data
    gray_img = img.convert("L")
    data = np.array(gray_img)

    with col1:
        st.image(img, caption="Original AFM Scan", use_container_width=True)

    with col2:
        # 3D Surface Reconstruction
        X = np.arange(data.shape[1])
        Y = np.arange(data.shape[0])
        X, Y = np.meshgrid(X, Y)

        fig = go.Figure(data=[go.Surface(z=data, x=X, y=Y, colorscale="Viridis")])
        fig.update_layout(
            title="3D Interactive Topography",
            template="plotly_dark",
            scene=dict(bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- ANALYSIS SECTION ----------------
    st.divider()
    
    # Calculate Real Science Parameters
    Ra = np.mean(np.abs(data - np.mean(data)))
    Rq = np.sqrt(np.mean((data - np.mean(data))**2))

    c1, c2, c3 = st.columns(3)
    c1.metric("Average Roughness (Ra)", f"{Ra:.2f} nm")
    c2.metric("RMS Roughness (Rq)", f"{Rq:.2f} nm")
    c3.metric("Peak-to-Valley", f"{np.ptp(data)} nm")

    # ---------------- GEMINI REPORT ----------------
    if API_KEY:
        if st.button("Generate Detailed AI Scientific Report"):
            with st.spinner("Gemini is analyzing the nanostructure..."):
                # SYSTEM PROMPT: Tells Gemini how to behave
                scientific_prompt = f"""
                You are a Senior Scientist at IIT Madras specializing in Nanotechnology.
                Analyze this AFM (Atomic Force Microscopy) image and the following data:
                - Average Roughness (Ra): {Ra:.2f} nm
                - RMS Roughness (Rq): {Rq:.2f} nm
                
                Please provide:
                1. A morphological description of the surface.
                2. Identification of any visible grains, pores, or artifacts.
                3. A professional conclusion on the sample quality for research purposes.
                Keep the tone academic and precise.
                """
                
                # UPDATED: Sending both the TEXT and the IMAGE to Gemini
                response = model.generate_content([scientific_prompt, img])
                
                st.markdown("### 🧠 AI Research Insights")
                st.info(response.text)
    else:
        st.warning("Please enter your API Key in the sidebar to enable AI analysis.")

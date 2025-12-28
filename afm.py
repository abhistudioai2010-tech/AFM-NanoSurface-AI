import streamlit as st
import google.generativeai as genai
from PIL import Image
import numpy as np
import plotly.graph_objects as go

# 1. API SETUP
# Use st.secrets["GEMINI_API_KEY"] for deployment or sidebar input for testing
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter Google AI Studio Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Define System Instruction to "train" the AI behavior
    system_instruction = (
        "You are an AFM specialist at IIT Madras. Analyze height maps. "
        "Ra is average roughness, Rq is RMS. If Rq > Ra by ~7%, it is a standard Gaussian surface."
    )
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )

# 2. UI LAYOUT
st.title("🔬 AFM NanoSurface AI Lab")

uploaded_file = st.file_uploader("Upload AFM Image", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    img = Image.open(uploaded_file)
    data = np.array(img.convert("L")) # Convert to height data

    col1, col2 = st.columns(2)
    
    with col1:
        st.image(img, caption="AFM Scan", use_container_width=True)
    
    with col2:
        # Create 3D Graph
        fig = go.Figure(data=[go.Surface(z=data, colorscale='Viridis')])
        fig.update_layout(title='3D Topography', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # 3. ANALYSIS & API INTEGRATION
    Ra = np.mean(np.abs(data - np.mean(data)))
    Rq = np.sqrt(np.mean((data - np.mean(data))**2))

    st.metric("Ra (Roughness)", f"{Ra:.3f} nm")
    st.metric("Rq (RMS)", f"{Rq:.3f} nm")

    if st.button("Generate AI Research Report"):
        prompt = f"The calculated roughness is Ra: {Ra:.3f} nm and Rq: {Rq:.3f} nm. Analyze the morphology."
        # Sending BOTH text and image to the API
        response = model.generate_content([prompt, img])
        st.markdown("### 📄 AI Scientific Report")
        st.write(response.text)
        
elif not api_key:
    st.warning("Please enter your API Key in the sidebar to start.")

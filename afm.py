import streamlit as st
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AFM Nano Research Lab", layout="wide")

st.markdown("""
<style>
body{background:#050a14;color:#00f7ff}
h1,h2,h3{color:#00f7ff}
.stButton>button{background:#00f7ff;color:black;border-radius:8px}
</style>
""", unsafe_allow_html=True)

st.title("🧬 AFM Nano Research Lab — Gemini Powered")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Gemini AI Scientist")
mode = st.sidebar.selectbox("AFM Mode", ["Contact","Tapping","Non-Contact","STM"])
api_key = st.sidebar.text_input("Gemini API Key", type="password")
report_goal = st.sidebar.text_area("Scientific Goal",
    "Write a complete AFM morphology and roughness research report.")

# ---------------- MAIN ----------------
file = st.file_uploader("Upload AFM Height Map", ["png","jpg","tif"])

if file:
    img = Image.open(file).convert("L")
    Z = np.array(img)

    st.image(img, caption="AFM Height Map", use_column_width=True)

    # Roughness
    Ra = np.mean(np.abs(Z - Z.mean()))
    Rq = np.sqrt(np.mean((Z - Z.mean())**2))

    st.markdown(f"""
    ### Surface Parameters  
    **Mode:** {mode}  
    **Ra:** {Ra:.3f} nm  
    **Rq:** {Rq:.3f} nm
    """)

    # 3D Surface
    X, Y = np.meshgrid(np.arange(Z.shape[1]), np.arange(Z.shape[0]))
    fig = go.Figure(go.Surface(z=Z, x=X, y=Y, colorscale="Turbo"))
    fig.update_layout(title="3D AFM Nano Topography",
        paper_bgcolor="black",
        scene=dict(xaxis_title="X nm", yaxis_title="Y nm", zaxis_title="Height (nm)"))
    st.plotly_chart(fig, use_container_width=True)

    # Gemini Report
    if api_key and st.button("Generate Gemini Research Report"):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")
        prompt = f"""
        AFM Mode: {mode}
        Ra={Ra:.3f} nm, Rq={Rq:.3f} nm.
        {report_goal}
        """
        response = model.generate_content(prompt)
        st.markdown("## Gemini AI Generated Research Report")
        st.write(response.text)

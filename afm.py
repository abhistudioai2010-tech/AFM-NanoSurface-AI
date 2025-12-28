import streamlit as st
import numpy as np
from PIL import Image

# Safe Plotly Import
try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except:
    PLOTLY_OK = False

# Safe Gemini Import
try:
    import google.generativeai as genai
    GEMINI_OK = True
except:
    GEMINI_OK = False

st.set_page_config(page_title="Universal AFM Nano Lab", layout="wide")

st.markdown("""
<style>
body{background:#050a14;color:#00f7ff}
h1,h2,h3{color:#00f7ff}
.stButton>button{background:#00f7ff;color:black;border-radius:8px}
</style>
""", unsafe_allow_html=True)

st.title("🧬 Universal AFM Nano Research Dashboard")

# ---------------- Sidebar ----------------
st.sidebar.header("AFM Settings")
mode = st.sidebar.selectbox("AFM Mode", ["Contact", "Tapping", "Non-Contact", "STM"])

if GEMINI_OK:
    api_key = st.sidebar.text_input("Gemini API Key", type="password")
    report_goal = st.sidebar.text_area("Report Objective",
        "Write a scientific AFM morphology & roughness report.")
else:
    st.sidebar.warning("Gemini not installed.")

# ---------------- Upload ----------------
file = st.file_uploader("Upload AFM Height Map", ["png","jpg","tif"])

if file:
    img = Image.open(file).convert("L")
    Z = np.array(img)

    st.image(img, caption="AFM Height Map", use_column_width=True)

    # Roughness
    Ra = np.mean(np.abs(Z - Z.mean()))
    Rq = np.sqrt(np.mean((Z - Z.mean())**2))

    st.markdown(f"""
    ### Surface Roughness
    **Mode:** {mode}  
    **Ra:** {Ra:.3f} nm  
    **Rq:** {Rq:.3f} nm
    """)

    # 3D Plot
    if PLOTLY_OK:
        X, Y = np.meshgrid(np.arange(Z.shape[1]), np.arange(Z.shape[0]))
        fig = go.Figure(go.Surface(z=Z, x=X, y=Y, colorscale="Turbo"))
        fig.update_layout(title="3D AFM Nano Surface",
            paper_bgcolor="black",
            scene=dict(
                xaxis_title="X (nm)",
                yaxis_title="Y (nm)",
                zaxis_title="Height (nm)"
            ))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Plotly missing. Install plotly to enable 3D surface.")

    # Gemini Report
    if GEMINI_OK and api_key and st.button("Generate AI Scientific Report"):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"AFM Mode: {mode}, Ra={Ra:.3f}, Rq={Rq:.3f}. {report_goal}"
        report = model.generate_content(prompt)
        st.markdown("## AI Generated Report")
        st.write(report.text)

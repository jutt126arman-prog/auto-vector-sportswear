import streamlit as st
from rembg import remove
from PIL import Image
import vtracer
import io
import os

# Page ki setting aur Title
st.set_page_config(page_title="Auto Vector Sportswear", page_icon="👕", layout="centered")

# CSS Styling (Design behtar karne ke liye)
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { 
        width: 100%; 
        border-radius: 15px; 
        height: 3.5em; 
        background-color: #FF4B4B; 
        color: white; 
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👕 Auto Vector Sportswear")
st.markdown("### AI Texture Extractor & Vectorizer")
st.write("Apne design ki photo upload karein, AI uska texture nikal kar Vector (SVG) file bana dega.")

# File Uploader
uploaded_file = st.file_uploader("Yahan image upload karein (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Screen ko do hisson mein divide karna
    col1, col2 = st.columns(2)
    
    image = Image.open(uploaded_file)
    with col1:
        st.info("Original Design")
        st.image(image, use_container_width=True)
    
    # Processing Button
    if st.button('Vector Texture Generate Karein'):
        with st.spinner('AI kaam kar raha hai... thoda intezar karein...'):
            try:
                # 1. Background Removal
                input_data = uploaded_file.getvalue()
                output_rembg = remove(input_data)
                
                # 2. Temporary save for Vectorization
                temp_png = "temp_process.png"
                with open(temp_png, "wb") as f:
                    f.write(output_rembg)
                
                # 3. Vtracer (Converting to SVG)
                output_svg = "Auto_Vector_Design.svg"
                # 'spline' mode curves ko smooth rakhta hai
                vtracer.convert(temp_png, output_svg, mode='spline', iteration=2, precision=2)
                
                # Result dikhana
                with col2:
                    st.success("Extracted Texture")
                    st.image(output_rembg, use_container_width=True)
                
                st.balloons()
                
                # 4. Download Button
                with open(output_svg, "rb") as f:
                    st.download_button(
                        label="📥 Download Vector (SVG) File",
                        data=f,
                        file_name="Auto_Vector_Sportswear.svg",
                        mime="image/svg+xml"
                    )
                
                # Purani files delete karna
                if os.path.exists(temp_png): os.remove(temp_png)

            except Exception as e:
                st.error(f"Ek error aaya hai: {e}")

st.markdown("---")
st.caption("Design & Vectorized by Auto Vector Sportswear AI")

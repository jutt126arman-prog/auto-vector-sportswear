import streamlit as st
from rembg import remove
from PIL import Image
import vtracer
import io
import os

# Page Settings
st.set_page_config(page_title="Auto Vector Sportswear", page_icon="👕")

# UI Styling
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("👕 Auto Vector Sportswear")
st.write("Apne design se texture nikalne aur vector banane ke liye image upload karein.")

# File Uploader
uploaded_file = st.file_uploader("Upload Shirt Design (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Do hisson mein screen divide karein
    col1, col2 = st.columns(2)
    
    img = Image.open(uploaded_file)
    with col1:
        st.image(img, caption="Original Image", use_container_width=True)

    if st.button("Texture Nikalo aur Vector Banao"):
        with st.spinner("AI Processing shuru hai..."):
            # 1. Background Removal (Texture Extraction)
            input_bytes = uploaded_file.getvalue()
            no_bg_bytes = remove(input_bytes)
            
            # 2. Temporary save for Vectorization
            temp_path = "temp_texture.png"
            with open(temp_path, "wb") as f:
                f.write(no_bg_bytes)
            
            # 3. Vectorization (SVG Generation)
            output_svg = "design_texture.svg"
            # Spline mode lines ko smooth banata hai
            vtracer.convert(temp_path, output_svg, mode='spline', precision=2)
            
            # Results Display
            with col2:
                st.image(no_bg_bytes, caption="Extracted Texture", use_container_width=True)
            
            st.success("✅ Kaam mukammal ho gaya!")
            
            # 4. Download Button
            with open(output_svg, "rb") as svg_file:
                st.download_button(
                    label="📥 Download Vector (SVG) File",
                    data=svg_file,
                    file_name="Auto_Vector_Texture.svg",
                    mime="image/svg+xml"
                )
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)

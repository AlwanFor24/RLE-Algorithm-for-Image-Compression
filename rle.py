import streamlit as st
from PIL import Image
import numpy as np
import io
import os

st.title("🗜️ RLE Compression Images (JPG, PNG, BMP, GIF)")

def rle_encode(data):
    encoded = []
    prev = data[0]
    count = 1
    for item in data[1:]:
        if item == prev:
            count += 1
        else:
            encoded.append((prev, count))
            prev = item
            count = 1
    encoded.append((prev, count))
    return encoded

def rle_decode(encoded):
    decoded = []
    for value, count in encoded:
        decoded.extend([value] * count)
    return decoded

def image_to_pixel_list(img):
    img = img.convert("RGB")
    return list(img.getdata())

def pixel_list_to_image(pixel_list, size):
    img = Image.new("RGB", size)
    img.putdata(pixel_list)
    return img

def get_encoded_size(encoded):
    # 3 byte warna + 1 byte count
    return len(encoded) * 4

def image_to_bytes(img, format):
    buf = io.BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()

# Buat folder output jika belum ada
output_dir = "(nama folder menyesuaikan) "
os.makedirs(output_dir, exist_ok=True)

uploaded_files = st.file_uploader(
    "Upload images (JPG, PNG, BMP, GIF)", 
    type=["jpg", "png", "bmp", "gif"], 
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.subheader(f"📄 File: {uploaded_file.name}")

        original_bytes = uploaded_file.getvalue()
        original_size = len(original_bytes)

        image = Image.open(io.BytesIO(original_bytes))
        st.image(image, caption="Original Image", use_column_width=True)

        pixels = image_to_pixel_list(image)

        rle_encoded = rle_encode(pixels)
        rle_decoded = rle_decode(rle_encoded)

        decompressed_img = pixel_list_to_image(rle_decoded, image.size)
        st.image(decompressed_img, caption="Decompressed Image (from RLE)", use_column_width=True)

        encoded_size = get_encoded_size(rle_encoded)
        compression_ratio = original_size / encoded_size if encoded_size > 0 else 0

        st.markdown(f"""
        **📦 Compression Info**
        - Original File Size: `{original_size} byte`
        - RLE Encoded Size (est.): `{encoded_size} byte`
        - Compression Ratio: `{compression_ratio:.2f}`
        """)

        original_format = image.format or "PNG"
        ext = uploaded_file.name.split('.')[-1]

        base_name = os.path.splitext(uploaded_file.name)[0]
        new_file_name = f"{base_name}_1.{ext}"

        # Simpan otomatis hasil dekompresi ke folder output
        save_path = os.path.join(output_dir, new_file_name)
        decompressed_img.save(save_path)

        st.success(f"✅ File hasil dekompresi sudah disimpan otomatis di: `{save_path}`")

import streamlit as st
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# Load the pre-trained model
# Sesuaikan dengan path model Anda (model terbaik yang di dump dalam format .h5)
model = load_model("D:\Semester 5\Pembelajaran mesin dan Pembelajaran Mendalam\Modul Convolutional Neural Network\Tugas6_B_11683\model_mobilenet.h5")
class_names = ["Matang", "Mentah"]

# Function to preprocess and classify image
def classify_image(image_path):
    try:
        # Load and preprocess the image
        input_image = tf.keras.utils.load_img(image_path, target_size=(180, 180))
        input_image_array = tf.keras.utils.img_to_array(input_image)
        input_image_exp_dim = tf.expand_dims(input_image_array, 0)
        
        # Predict using the model
        predictions = model.predict(input_image_exp_dim)
        result = tf.nn.softmax(predictions[0])  # Apply softmax for probability

        # Return the label with highest confidence
        class_idx = np.argmax(result)
        return class_names[class_idx], float(result[class_idx]), result
    except Exception as e:
        return "Error", str(e), None

# Function to display progress bar and confidence
def custom_progress_bar(confidence, color1, color2):
    st.markdown(
        f"""
        <div style="border-radius: 5px; overflow: hidden; width: 100%; font-size: 14px;">
            <div style="width:{int(confidence*100)}%; background:{color1}; color: white; text-align: center; height: 24px; float: left;">
                {int(confidence*100)}%
            </div>
            <div style="width:{100-int(confidence*100)}%; background: {color2}; color: white; text-align: center; height: 24px; float: left;">
                {100-int(confidence*100)}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Streamlit UI
st.title("Prediksi Kematangan Buah Naga - 1683")  # 4 digit npm terakhir

# Upload multiple files in the main page
uploaded_files = st.file_uploader("Unggah Gambar (Beberapa diperbolehkan)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# Sidebar for prediction button and results
if st.sidebar.button("Prediksi"):
    if uploaded_files:
        st.sidebar.write("Hasil Prediksi")
        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Perform prediction
            label, confidence, scores = classify_image(uploaded_file.name)
            if label != "Error":
                # Define colors for the bar and label
                primary_color = "#00BFFF"  # Blue for "Matang"
                secondary_color = "#FF4136"  # Red for "Mentah"
                label_color = primary_color if label == "Matang" else secondary_color

                # Display prediction results
                st.sidebar.markdown(f"<h4 style='color: {label_color};'>Prediksi: {label}</h4>", unsafe_allow_html=True)
                st.sidebar.write("Confidence scores:")
                for i, (class_name, confidence) in enumerate(zip(class_names, scores)):
                    st.sidebar.write(f"{class_name}: {confidence * 100:.2f}%")
                
                # Progress bar
                custom_progress_bar(confidence, primary_color, secondary_color)
            else:
                st.sidebar.error(f"Kesalahan saat memproses gambar {uploaded_file.name}: {confidence}")
    else:
        st.sidebar.error("Silakan unggah setidaknya satu gambar untuk diprediksi.")

# Preview images in the main page
if uploaded_files:
    st.write("Preview:")
    for uploaded_file in uploaded_files:
        st.image(uploaded_file, caption=f"{uploaded_file.name}", use_column_width=True)
import streamlit as st
!pip install opencv-python
import cv2
import numpy as np
import subprocess  # For opening files on Mac

# Function to embed message into image
def encrypt_image(img, msg, password):
    d = {chr(i): i for i in range(255)}
    c = {i: chr(i) for i in range(255)}

    n = m = z = 0
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]  # Embed message into pixels
        n += 1
        m += 1
        z = (z + 1) % 3  # Change RGB channel

    return img, password

# Function to extract message from image
def decrypt_image(img, password, input_password):
    d = {chr(i): i for i in range(255)}
    c = {i: chr(i) for i in range(255)}

    if input_password != password:
        return "Wrong password", None

    message = ""
    n = m = z = 0
    while True:
        try:
            message += c[img[n, m, z]]  # Extract message from pixels
            n += 1
            m += 1
            z = (z + 1) % 3  # Change RGB channel
        except IndexError:
            break

    return message, img

# Streamlit UI
st.title("Image Encryption and Decryption")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the uploaded image
    img = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    st.image(img, channels="BGR", caption="Uploaded Image")

    msg = st.text_input("Enter secret message")
    password = st.text_input("Enter a passcode", type="password")

    if st.button("Encrypt"):
        if msg and password:
            encrypted_img, password = encrypt_image(img.copy(), msg, password)
            cv2.imwrite("encryptedImage.jpg", encrypted_img)
            st.image(encrypted_img, channels="BGR", caption="Encrypted Image")
            st.success("Image Encrypted Successfully!")
            # Optionally save or display image in Streamlit
            st.download_button(
                label="Download Encrypted Image",
                data=open("encryptedImage.jpg", "rb").read(),
                file_name="encryptedImage.jpg",
                mime="image/jpeg"
            )

    input_password = st.text_input("Enter password for decryption", type="password")

    if st.button("Decrypt"):
        if input_password:
            decrypted_message, decrypted_img = decrypt_image(
                img.copy(), password, input_password)
            if decrypted_message != "Wrong password":
                st.write(f"Decrypted message: {decrypted_message}")
                st.image(decrypted_img, channels="BGR", caption="Decrypted Image")
            else:
                st.error(decrypted_message)

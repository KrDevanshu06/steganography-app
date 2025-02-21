import streamlit as st
from PIL import Image
import io
from utils.steganography import encode_image, decode_image

def main():
    st.title("Secure Image Steganography")
    st.sidebar.title("Navigation")
    option = st.sidebar.radio("Choose an option:", ["Encode Message", "Decode Message", "About"])

    if option == "Encode Message":
        st.header("Encode a Secret Message into an Image")
        uploaded_image = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
        secret_message = st.text_area("Enter your secret message")
        if st.button("Encode") and uploaded_image and secret_message:
            try:
                encoded_image_buffer = encode_image(uploaded_image, secret_message.encode('utf-8'))
                st.success("Message encoded successfully!")
                st.image(encoded_image_buffer, caption="Encoded Image", use_column_width=True)
                st.download_button(
                    label="Download Encoded Image",
                    data=encoded_image_buffer,
                    file_name="encoded.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Error: {e}")

    elif option == "Decode Message":
        st.header("Decode a Hidden Message from an Image")
        uploaded_image = st.file_uploader("Upload the Encoded Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
        if st.button("Decode") and uploaded_image:
            try:
                decoded_bytes = decode_image(uploaded_image)
                decoded_message = decoded_bytes.decode('utf-8')
                st.success("Message decoded successfully!")
                st.write("Decoded Message:")
                st.info(decoded_message)
            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.header("About")
        st.write("""
        **Secure Image Steganography** is an app that hides secret messages within images using LSB (Least Significant Bit) steganography.
        
        **Encode Message:**  
        Upload an image and type your secret message. The app embeds your message into the image and provides a download link for the modified image.
        
        **Decode Message:**  
        Upload an encoded image to retrieve the hidden secret message.
        """)

if __name__ == "__main__":
    main()

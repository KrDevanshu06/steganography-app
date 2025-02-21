import streamlit as st
from PIL import Image
import io
from utils.steganography import encode_image, decode_image

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "Encode"

def set_page(page_name):
    st.session_state.page = page_name

def main():
    st.title("🔐 Secure Image Steganography")

    # Sidebar navigation buttons
    st.sidebar.title("Navigation")
    if st.sidebar.button("📤 Encode Message in Image"):
        set_page("Encode")
    if st.sidebar.button("📥 Decode Message in Image"):
        set_page("Decode")

    # Always Visible About Section (No Expander)
    st.sidebar.markdown("---")  # Separator
    st.sidebar.subheader("ℹ️ About")
    st.sidebar.write("""
    **Secure Image Steganography** is a tool for hiding messages inside images using LSB (Least Significant Bit) encoding.
    
    - **Encoding:** Upload an image, enter a secret message, and set a password to embed the data.
    - **Decoding:** Provide the correct password to retrieve the hidden message from an encoded image.
    """)

    # Change UI screen based on button click
    if st.session_state.page == "Encode":
        st.header("📤 Encode a Secret Message into an Image")
        uploaded_image = st.file_uploader("Upload an Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
        secret_message = st.text_area("Enter your secret message")
        password = st.text_input("Enter a password", type="password")

        if st.button("🔒 Encode"):
            if uploaded_image and secret_message and password:
                try:
                    encoded_image_buffer = encode_image(uploaded_image, secret_message, password)
                    st.success("Message encoded successfully!")
                    st.image(encoded_image_buffer, caption="Encoded Image", use_column_width=True)
                    st.download_button(
                        label="📥 Download Encoded Image",
                        data=encoded_image_buffer,
                        file_name="encoded.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("⚠️ Please upload an image, enter a message, and set a password.")

    elif st.session_state.page == "Decode":
        st.header("📥 Decode a Hidden Message from an Image")
        uploaded_image = st.file_uploader("Upload the Encoded Image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
        password = st.text_input("Enter the password", type="password")

        if st.button("🔓 Decode"):
            if uploaded_image and password:
                try:
                    decoded_message = decode_image(uploaded_image, password)
                    st.success("Message decoded successfully!")
                    st.write("**Decoded Message:**")
                    st.info(decoded_message)
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("⚠️ Please upload an encoded image and enter the correct password.")

if __name__ == "__main__":
    main()

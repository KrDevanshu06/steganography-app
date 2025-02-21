# Secure Image Steganography App

This is a simple Streamlit app that allows you to encode secret messages into images using LSB (Least Significant Bit) steganography and decode hidden messages from images.

## Features

- **Encode Message:** 
  - Upload an image.
  - Enter your secret message.
  - The app encodes the message into the image and provides a download link for the modified image.
  
- **Decode Message:**
  - Upload an image with a hidden message.
  - The app decodes and displays the secret message.

## Directory Structure

```
steganography_app/
│── app.py                     # Main Streamlit application
│── requirements.txt           # List of dependencies
│── README.md                  # Project documentation
│
├── images/                    # Contains sample images for testing
│   ├── sample_input.png       # Sample input image (add your own image)
│   ├── encoded_sample.png     # Example of an encoded image (optional)
│
├── utils/
│   └── steganography.py       # Module with encoding/decoding functions
│
└── saved_images/              # Folder to store user-uploaded/processed images (optional)
```

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd steganography_app
   ```

2. **Create a Virtual Environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit App:**
   ```bash
   streamlit run app.py
   ```

## Usage

- Navigate to the **Encode Message** or **Decode Message** section from the sidebar.
- Follow the on-screen instructions to upload images and encode or decode messages.

## License

This project is licensed under the MIT License.
```

---

#### `images/` Folder

Place your sample images (e.g., `sample_input.png` and optionally `encoded_sample.png`) in this folder. These images are used for testing and demonstration purposes.

---

#### `saved_images/` Folder

This folder is intended for storing user-uploaded or processed images if needed. It can remain empty initially.

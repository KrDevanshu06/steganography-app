import struct
from PIL import Image
import io
import json

def encode_image(image_file, secret_message, password):
    """
    Encodes a secret message and a password into an image using LSB steganography.
    The input image is provided as a file-like object.
    Returns a BytesIO object with the encoded image.
    """
    # Combine password and message into a JSON object
    data_dict = {
        "password": password,
        "message": secret_message
    }
    combined_data = json.dumps(data_dict).encode('utf-8')

    image = Image.open(image_file)
    image = image.convert("RGB")
    width, height = image.size
    pixels = list(image.getdata())

    message_length = len(combined_data) * 8  # Length in bits
    header = struct.pack('>I', message_length)  # 4-byte header (big-endian)
    data = header + combined_data

    # Convert data to list of bits (MSB first)
    data_bits = []
    for byte in data:
        for i in range(7, -1, -1):
            data_bits.append((byte >> i) & 1)

    total_bits = len(data_bits)
    max_bits = len(pixels) * 3  # Each pixel has 3 channels (RGB)
    if total_bits > max_bits:
        raise ValueError(f"Message too large. Max: {max_bits} bits, Needed: {total_bits} bits.")

    data_index = 0
    new_pixels = []
    for r, g, b in pixels:
        if data_index < total_bits:
            r = (r & 0xFE) | data_bits[data_index]
            data_index += 1
        if data_index < total_bits:
            g = (g & 0xFE) | data_bits[data_index]
            data_index += 1
        if data_index < total_bits:
            b = (b & 0xFE) | data_bits[data_index]
            data_index += 1
        new_pixels.append((r, g, b))

    encoded_image = Image.new("RGB", (width, height))
    encoded_image.putdata(new_pixels)

    # Save the encoded image to a BytesIO buffer
    buffer = io.BytesIO()
    encoded_image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def decode_image(image_file, password):
    """
    Decodes a hidden message from an image using LSB steganography.
    The input image is provided as a file-like object.
    Validates the password before returning the hidden message.
    """
    image = Image.open(image_file)
    image = image.convert("RGB")
    pixels = list(image.getdata())

    # Extract all LSBs
    data_bits = []
    for r, g, b in pixels:
        data_bits.extend([r & 1, g & 1, b & 1])

    # Extract header (first 32 bits)
    if len(data_bits) < 32:
        raise ValueError("Insufficient data for header")
    header_bits = data_bits[:32]

    # Convert header bits to bytes
    header_bytes = bytearray()
    for i in range(0, 32, 8):
        byte = 0
        for bit in header_bits[i:i+8]:
            byte = (byte << 1) | bit
        header_bytes.append(byte)
    message_length = struct.unpack('>I', header_bytes)[0]

    # Extract message bits
    total_bits_needed = 32 + message_length
    if len(data_bits) < total_bits_needed:
        raise ValueError("Insufficient data for message")
    message_bits = data_bits[32:total_bits_needed]

    # Convert message bits to bytes
    message_bytes = bytearray()
    for i in range(0, len(message_bits), 8):
        byte = 0
        for bit in message_bits[i:i+8]:
            byte = (byte << 1) | bit
        message_bytes.append(byte)

    # Parse the JSON data
    try:
        data_str = message_bytes.decode('utf-8')
        data_dict = json.loads(data_str)
    except Exception:
        raise ValueError("Failed to decode message. The image may not contain a valid encoded message.")

    # Validate password
    if data_dict.get("password") != password:
        raise ValueError("Incorrect password. Unable to decode the message.")

    return data_dict.get("message", "")

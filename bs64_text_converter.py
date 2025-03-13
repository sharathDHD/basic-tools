# file_path/base64_converter.py
import base64

class Base64Converter:
    """A class for encoding and decoding Base64 strings."""

    @staticmethod
    def encode(text: str) -> dict:
        """
        Encodes a plain text string into a Base64-encoded string.

        :param text: Plain text to encode.
        :return: Dictionary containing the encoded string or an error message.
        """
        try:
            encoded_bytes = base64.b64encode(text.encode('utf-8'))
            return {"success": True, "encoded": encoded_bytes.decode('utf-8')}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def decode(encoded_str: str) -> dict:
        """
        Decodes a Base64-encoded string into plain text.

        :param encoded_str: Base64-encoded string.
        :return: Dictionary containing the decoded text or an error message.
        """
        try:
            decoded_bytes = base64.b64decode(encoded_str, validate=True)
            return {"success": True, "decoded": decoded_bytes.decode('utf-8')}
        except (base64.binascii.Error, UnicodeDecodeError) as e:
            return {"success": False, "error": "Invalid Base64-encoded input."}

if __name__ == "__main__":
    converter = Base64Converter()

    # Example encoding
    text = "Hello, Base64!"
    encoded_result = converter.encode(text)
    print("Encoding Result:", encoded_result)

    # Example decoding
    if encoded_result["success"]:
        decoded_result = converter.decode(encoded_result["encoded"])
        print("Decoding Result:", decoded_result)
    else:
        print("Encoding Failed:", encoded_result["error"])

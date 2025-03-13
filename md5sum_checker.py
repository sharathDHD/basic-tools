# file_path/md5_validator.py
import hashlib

class MD5Validator:
    """A class for computing and validating MD5 checksums."""

    @staticmethod
    def compute_md5(text: str) -> dict:
        """
        Computes the MD5 hash of a given text.

        :param text: The input text.
        :return: Dictionary containing the MD5 hash or an error message.
        """
        try:
            md5_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
            return {"success": True, "md5": md5_hash}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def compute_md5_file(file_path: str) -> dict:
        """
        Computes the MD5 hash of a file.

        :param file_path: The path to the file.
        :return: Dictionary containing the MD5 hash or an error message.
        """
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return {"success": True, "md5": hash_md5.hexdigest()}
        except FileNotFoundError:
            return {"success": False, "error": "File not found."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def validate_md5(md5_1: str, md5_2: str) -> dict:
        """
        Validates if two given MD5 hashes match.

        :param md5_1: First MD5 hash.
        :param md5_2: Second MD5 hash.
        :return: Dictionary with validation result.
        """
        match = md5_1 == md5_2
        return {"success": True, "match": match, "message": "Hashes match!" if match else "Hashes do not match."}

if __name__ == "__main__":
    validator = MD5Validator()

    # Example 1: Text-based validation
    text_1 = "Hello, world!"
    text_2 = "Hello, world!"  # Identical text for validation

    md5_result_1 = validator.compute_md5(text_1)
    md5_result_2 = validator.compute_md5(text_2)

    if md5_result_1["success"] and md5_result_2["success"]:
        validation_result = validator.validate_md5(md5_result_1["md5"], md5_result_2["md5"])
        print("Text MD5 Validation:", validation_result)
    else:
        print("Error in MD5 computation:", md5_result_1.get("error") or md5_result_2.get("error"))

    # Example 2: File-based validation
    file_path_1 = "example1.txt"
    file_path_2 = "example2.txt"

    file_md5_1 = validator.compute_md5_file(file_path_1)
    file_md5_2 = validator.compute_md5_file(file_path_2)

    if file_md5_1["success"] and file_md5_2["success"]:
        validation_result = validator.validate_md5(file_md5_1["md5"], file_md5_2["md5"])
        print("File MD5 Validation:", validation_result)
    else:
        print("Error in file MD5 computation:", file_md5_1.get("error") or file_md5_2.get("error"))

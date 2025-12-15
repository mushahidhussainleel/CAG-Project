import re
import os

def sanitize_filename(filename: str) -> str:
    """
    Sanitize the filename to prevent:
    - Path traversal attacks
    - Invalid filesystem characters
    - Unexpected user inputs
    """

    if not filename:
        return "file"

    # Extract only the name (remove directory parts if user sends something like "../../notes.pdf")
    filename = os.path.basename(filename)

    # Replace invalid characters with underscore
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)

    # Replace consecutive spaces and underscores with a single underscore
    filename = re.sub(r'[\s_]+', '_', filename)

    # Trim leftover leading/trailing underscores
    filename = filename.strip('_')

    # If filename is still empty, fallback
    if not filename:
        filename = "file"

    return filename

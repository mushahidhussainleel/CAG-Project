from pydantic import BaseModel, Field, validator
from datetime import datetime

# -------------------------------------------------------
# This is a Pydantic model representing a POST request.
# It is used to validate and structure incoming data
# such as username, user_id, optional file_name, and date.
# Validators are added to ensure data is clean and consistent.
# -------------------------------------------------------
class PostRequest(BaseModel):

    # Optional file name (string, can be None)
    # If input is empty, "string", or None, it will be normalized to None
    file_name: str | None = None

    # Optional date field (string in "YYYY-MM-DD" format)
    # Defaults to today's date if not provided
    date: str | None = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

    # -------------------------------------------------------
    # Validator for "date" field
    # -------------------------------------------------------
    @validator("date", pre=True, always=True)
    def normalize_or_fill_date(cls, v):
        """
        Ensures the 'date' field is always in "YYYY-MM-DD" format.
        - If value is None or empty, it fills with today's date.
        - If value is invalid, it replaces it with today's date.
        - If value is valid, it keeps it as is.
        """
        if v is None or v == "":
            return datetime.now().strftime("%Y-%m-%d")  # Fill empty with today
        try:
            # Check if the given date string is valid
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            # Replace invalid date formats with today
            return datetime.now().strftime("%Y-%m-%d")

    # -------------------------------------------------------
    # Validator for "file_name" field
    # -------------------------------------------------------
    @validator("file_name", pre=True)
    def clean_file_name(cls, v):
        """
        Normalizes the file_name field.
        - If value is None, empty string, or literal "string", it becomes None.
        - Otherwise, returns the original value.
        This helps to avoid storing meaningless or placeholder file names.
        """
        if v is None or v == "" or v == "string":
            return None
        return v

import os

from dotenv import load_dotenv

# ---------------------------------------------------------
# Load environment variables from the .env file.
# This makes the variables defined in .env available through
# os.getenv().
# ---------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------
# Read the Groq API key from the environment.
# ---------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ---------------------------------------------------------
# Validate that the API key exists.
# Stop execution immediately if it is missing.
# ---------------------------------------------------------
if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY was not found. "
        "Please define it in the project's .env file."
    )
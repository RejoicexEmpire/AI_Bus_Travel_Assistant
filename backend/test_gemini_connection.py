import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found.")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Reply with exactly: Gemini connection successful",
    )

    print("Gemini API request successful.")
    print("Response:", response.text)

except Exception as error:
    print("Gemini API request failed.")
    print("Error:", error)

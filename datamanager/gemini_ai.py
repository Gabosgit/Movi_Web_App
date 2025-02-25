from google import genai
import os
from dotenv import load_dotenv


#loads variables from the .env file into the environment
load_dotenv()
# os.getenv() to access the environment variables loaded from the .env file
API_KEY = os.getenv('API_KEY_GEMINI')

client = genai.Client(api_key=API_KEY)


def fetch_from_gemini(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents={prompt}
    )
    return response

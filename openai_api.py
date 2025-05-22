import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate a study plan
def generate_study_plan(user_input):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an IELTS expert who creates tailored 4-week study plans."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.replace("**", "")

import os
from openai import OpenAI
from dotenv import load_dotenv

# Set OpenAI API key
load_dotenv(override=True)
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

MODEL = "gpt-3.5-turbo"

# Define function to classify user input as a greeting or question
def classify_input(user_input: str) -> str:
    """Classifies user input as a greeting or question."""
    try:
        prompt = [
                {"role": "system", "content": f"classify these input: {user_input} as one of these label 'question' or 'greeting', or 'absurd_question'"},
            ]
        response = ""
        for chunk in client.chat.completions.create(
                model="gpt-3.5-turbo", messages=prompt, stream=True, temperature=0.2, max_tokens=20
        ):
            text = chunk.choices[0].delta.content
            if text is not None:
                response += text
        return response.strip()
    except Exception:
        return "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"
    
# Define function to generate response to user greeting
def answer_greeting(greeting: str) -> str:
    try:
        prompt = [
            {"role": "system", "content": "Answer using Bahasa Indonesia or English with appropriate greeting."},
            {"role": "user", "content": f"Please respond to the user's greeting with the context: {greeting}, and add 'Ada yang bisa saya bantu?'"},
            ]
        response = ""
        for chunk in client.chat.completions.create(
                model="gpt-3.5-turbo", messages=prompt, stream=True, temperature=0.8, max_tokens=100
        ):
            text = chunk.choices[0].delta.content
            if text is not None:
                response += text
        return response.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"
    
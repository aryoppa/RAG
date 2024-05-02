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

# Define function to generate response to user greeting
def answer_greeting(greeting: str) -> str:
    try:
        prompt = [
            {"role": "system", "content": "Please provide your answer in either Bahasa Indonesia or English, accompanied by a suitable greeting. If you're uncertain, feel free to ask for clarification to user if you need more information."},
            {"role": "user", "content": f"Respond to the user's greeting by acknowledging it with the appropriate context, such as '{greeting}', and then add the phrase 'Ada yang bisa saya bantu?'"},
            ]
        response = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=prompt, stream=True, temperature=0.8, max_tokens=100
        )
        greeting = response.choices[0].message.content
        return greeting.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"
    
import os
from utils import load_data, search_notebook
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def classify_input(user_input: str) -> str:
    """Classifies user input as a greeting or question."""
    try:
        if "external data" in user_input.lower():
            return "Maaf, tetapi Anda tidak memiliki akses ke data eksternal."
        else:
            prompt = [
                 {"role": "system", "content": f"classify user input {user_input} as label 'question' or 'greeting'"}
            ]
            response = ""
            for chunk in client.chat.completions.create(
                    model="gpt-3.5-turbo", messages=prompt, stream=True, temperature=0.5, max_tokens=10
            ):
                text = chunk.choices[0].delta.content
                if text is not None:
                    response += text
            return response.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"

# Example usage:
user_input = "dimana alamat lnsw?"
classification = classify_input(user_input)
print("Classification:", classification)

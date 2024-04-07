import os
import logging
from utils import load_data, search_notebook
from openai import OpenAI
from dotenv import load_dotenv

# Set OpenAI API key
load_dotenv(override=True)
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo-0125")
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def get_openai_response(prompt, model="gpt-3.5-turbo-0125", temperature=0.5, max_tokens=100, stream=True):
    """Sends a prompt to the OpenAI API and returns the response."""
    try:
        response = ""
        for chunk in client.chat.completions.create(
                model=model, messages=prompt, stream=stream, temperature=temperature, max_tokens=max_tokens
        ):
            text = chunk.choices[0].delta.content
            if text is not None:
                response += text
        return response.strip()
    except Exception as e:
        logging.error(f"An error occurred while calling OpenAI API: {e}")
        return "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"

# Define function to classify user input as a greeting or question
def classify_input(user_input: str) -> str:
    """Classifies user input as a greeting or question."""
    if "external data" in user_input.lower():
        return "Maaf, tetapi Anda tidak memiliki akses ke data eksternal."
    else:
        prompt = [
             {"role": "system", "content": f"classify user input {user_input} as one of these label 'question' or 'greeting', or 'absurd_question'"},
        ]
        return get_openai_response(prompt, model=OPENAI_MODEL, temperature=0.8, max_tokens=15, stream=True)
    
# Define function to generate response to user greeting and return a hardcoded label
def answer_greeting(greeting: str) -> tuple:
    # AI persona name
    persona_name = "Naura"
    
    # Load data for each question
    df = load_data()
    
    if "external data" in greeting.lower():
        return ("Maaf, tetapi Anda tidak memiliki akses ke data eksternal.", "access_denied")
    else:
        prompt = [
            {"role": "system", "content": f"Sapaan pengguna: {greeting}\nApa yang bisa saya bantu hari ini"}
        ]
        response = get_openai_response(prompt, model=OPENAI_MODEL, temperature=0.5, max_tokens=100, stream=True)
        label = "greeting_response"
        return {"message":response, "label":label}
    
# Define function to process the question and generate response from data
def process_question(question: str,) -> str:
    try:
        # Load data for each question
        df = load_data()

        search_results = search_notebook(df, question, top_n=1)
        if search_results:
            summaries = []
            for result in search_results:
                if result is not None:
                    csv_extract = result['konten']
                    prompt = [
                        {"role": "system", "content": f"Summarize: {csv_extract}\nBerdasarkan pertanyan berikut: {question}\nMohon jangan mengada-ada atau menambahkan informasi lebih lanjut.\nHanya ambil informasi yang relevan."},
                    ]
                    response = get_openai_response(prompt, model=OPENAI_MODEL, temperature=0.1, max_tokens=1000, stream=True)
                    summaries.append(response.strip())
            responses =f"\n".join(summaries)
            label = "question_response"
            return {"message":responses, "label":label}
        else:
            return "Maaf, saya tidak bisa menemukan informasi yang sesuai dengan pertanyaan Anda."
    except TypeError as e:
        logging.error(f"An error occurred: {e}")
        return "Data diluar konteks yang ada, mohon masukan pertanyaan lainnya"


import os
from utils import load_data, search_notebook
from openai import OpenAI
from dotenv import load_dotenv

# Set OpenAI API key
load_dotenv(override=True)
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Define function to classify user input as a greeting or question
def classify_input(user_input: str) -> str:
    """Classifies user input as a greeting or question."""
    try:
        if "external data" in user_input.lower():
            return "Maaf, tetapi Anda tidak memiliki akses ke data eksternal."
        else:
            prompt = [
                 {"role": "system", "content": f"classify user input {user_input} as one of these label 'question' or 'greeting', or 'absurd_question'"},
            ]
            response = ""
            for chunk in client.chat.completions.create(
                    model="gpt-3.5-turbo-0125", messages=prompt, stream=True, temperature=0.8, max_tokens=15
            ):
                text = chunk.choices[0].delta.content
                if text is not None:
                    response += text
            return response.strip()
    except Exception as e:
        return "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"
    
# Define function to generate response to user greeting
def answer_greeting(greeting: str) -> str:

    #AI persona name
    persona_name = "Naura"
    
    # Load data for each question
    df = load_data()
    
    try:
        if "external data" in greeting.lower():
            return "Maaf, tetapi Anda tidak memiliki akses ke data eksternal."
        else:
            prompt = [
                {"role": "system", "content": f"Sapaan pengguna: {greeting}\nApa yang bisa saya bantu hari ini"}
            ]
            response = ""
            for chunk in client.chat.completions.create(
                    model="gpt-3.5-turbo-0125", messages=prompt, stream=True, temperature=0.5, max_tokens=100
            ):
                text = chunk.choices[0].delta.content
                if text is not None:
                    response += text
            return response.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"
    
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
                    response = ""
                    for chunk in client.chat.completions.create(
                            model="gpt-3.5-turbo-0125", messages=prompt, stream=True, temperature=0.1, max_tokens=1000
                    ):
                        text = chunk.choices[0].delta.content
                        if text is not None:
                            response += text
                    summaries.append(response.strip())
            return f"\n".join(summaries)
        else:
            return "Maaf, saya tidak bisa menemukan informasi yang sesuai dengan pertanyaan Anda."
    except TypeError as e:
        return "Data diluar konteks yang ada, mohon masukan pertanyaan lainnya"


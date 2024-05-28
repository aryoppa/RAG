import os
import time
from question.utils import load_data, search_notebook
from openai import OpenAI
from dotenv import load_dotenv

# Set OpenAI API key
load_dotenv(override=True)
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

TOP_N = 5
MODEL = "gpt-3.5-turbo"
# MODEL = "gpt-4o"

def process_question(question: str) -> str:
    try:
        # Load data for each question
        df = load_data()
        search_results = search_notebook(df, question, top_n=TOP_N)
        if search_results:
            prompt = [
                {"role": "system", "content": "You answer user questions with the information provided in the context. Answer using Bahasa Indonesia. Don't make up the answer. If the answer cannot be found, write 'I don't know.' Only use relevan data from context base on user question."},
                {"role": "user", "content": f"using the following context that consist of frequently asked questions (FAQ): {search_results['konten']}. Answer base on this question: {question}"},
            ]

            response = client.chat.completions.create(
                model=MODEL, messages=prompt, temperature=0.0, max_tokens=1000
            )

            final_response = response.choices[0].message.content
            indexes = str(search_results["index"])
            return {"message":final_response, "index":indexes}
        else: 
            return "Maaf, saya tidak bisa menemukan informasi yang sesuai dengan pertanyaan Anda. Mohon berikan detail pertanyaannya agar saya dapat memberikan bantuan yang lebih spesifik"  
    except TypeError:
        return "Data diluar konteks yang ada, mohon masukan pertanyaan lainnya"




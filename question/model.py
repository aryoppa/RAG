import os
from question.utils import load_data, search_notebook
from openai import OpenAI
from dotenv import load_dotenv

# Memuat kunci API OpenAI dari file .env
load_dotenv(override=True)

# Inisialisasi klien OpenAI dengan kunci API
client = OpenAI(
    # Ini adalah default dan bisa diabaikan
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Menentukan jumlah hasil pencarian teratas dan model yang akan digunakan
TOP_N = 5
MODEL = "gpt-3.5-turbo"
# MODEL = "gpt-4o"

# Mendefinisikan fungsi untuk memproses pertanyaan pengguna
def process_question(question: str) -> str:
    try:
        # Memuat data yang dibutuhkan untuk setiap pertanyaan
        df = load_data()
        
        # Mencari hasil yang relevan dalam notebook berdasarkan pertanyaan pengguna
        search_results = search_notebook(df, question, top_n=TOP_N)
        
        # Jika hasil pencarian ditemukan
        if search_results:
            prompt = [
                {
                    # Pesan sistem memberikan instruksi kepada model tentang bagaimana menjawab pertanyaan
                    "role": "system",
                    "content": "You answer user questions with the information provided in the context. Answer using Bahasa Indonesia. Don't make up the answer. If the answer cannot be found, write 'Maaf saya tidak tahu'. Only provide relevant and correct answers, you are strictly prohibited from providing irrelevant and incorrect answers, It's better to say you don't know the answer, than to give the wrong answer"
                },
                {
                    # Pesan pengguna berisi hasil pencarian dan pertanyaan pengguna
                    "role": "user",
                    "content": f"using the following context that consist of frequently asked questions (FAQ) data: {search_results['konten']}. Answer this question: {question}. Only give relevant and correct answers"
                }
            ]

            # Mengirimkan permintaan ke API OpenAI untuk menghasilkan respons
            response = client.chat.completions.create(
                model=MODEL,  # Model yang digunakan untuk menghasilkan respons
                messages=prompt,  # Pesan yang diberikan ke model
                temperature=0.0,  # Mengatur randomisasi output menjadi deterministik
                max_tokens=1000  # Jumlah maksimum token dalam respons
            )

            # Mengambil respons dari hasil yang dihasilkan oleh model
            final_response = response.choices[0].message.content
            indexes = str(search_results["index"])
            return {"message": final_response, "index": indexes}
        else:
            # Jika tidak ada hasil pencarian yang ditemukan
            no_result = "Maaf, saya tidak bisa menemukan informasi yang sesuai dengan pertanyaan Anda. Mohon berikan detail pertanyaannya agar saya dapat memberikan bantuan yang lebih spesifik"
            return {"message": no_result, "index": ""}
    except TypeError:
        # Menangani pengecualian jika terjadi TypeError
        error = "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"
        return {"message": error, "index": ""}
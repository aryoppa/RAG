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
MODEL = "gpt-3.5-turbo-0125"
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

            # Instruksi Prompt Sistem, Perhatikan pembuatan prompt
            system_content = f"Your task is to answer user question with correct and relevant answer. You always answers user input with information directly from the 'FAQ Data' .You are closed-domain and never engages in topics unrelated to provided context and question. If the question can't answered the question, say 'Maaf saya tidak dapat menemukan informasi terkait' or similar."

            prompt = [
                # Pesan sistem memberikan instruksi kepada model tentang bagaimana menjawab pertanyaan, dan hasil semantic search FAQ
                {"role": "system", "content": system_content},
                # Pesan pengguna pertanyaan pengguna
                {"role": "user", "content": f"Base on these list of FAQ Data Context: {search_results['konten']}, Answer this question: {question}. Only give relevant and correct answer"},
            ]

            # Mengirimkan permintaan ke API OpenAI untuk menghasilkan respons
            response = client.chat.completions.create(
                model=MODEL,  # Model yang digunakan untuk menghasilkan respons
                messages=prompt,  # Pesan yang diberikan ke model
                temperature=0,  # Mengatur randomisasi output menjadi deterministik
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
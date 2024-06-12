import os
from openai import OpenAI
from dotenv import load_dotenv

# Memuat kunci API OpenAI dari file .env
load_dotenv(override=True)

# Inisialisasi klien OpenAI dengan kunci API
client = OpenAI(
    # Ini adalah default dan bisa diabaikan
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Menentukan model yang akan digunakan
MODEL = "gpt-3.5-turbo"

# Mendefinisikan fungsi untuk menghasilkan respons terhadap salam pengguna
def answer_greeting(greeting: str) -> str:
    try:
        # Membuat prompt untuk diberikan ke model
        prompt = [
            {
                # Pesan sistem memberikan instruksi kepada model tentang bagaimana merespons
                "role": "system",
                "content": "Please provide your answer in either Bahasa Indonesia or English, accompanied by a suitable greeting with the appropriate context, and then add the phrase 'Ada yang bisa saya bantu?' . If you're uncertain, feel free to ask for clarification to user if you need more information."
            },
            {
                # Pesan pengguna berisi salam pengguna yang harus direspon
                "role": "user",
                "content": f"{greeting}"
            }
        ]

        # Mengirimkan permintaan ke API OpenAI untuk menghasilkan respons
        response = client.chat.completions.create(
            model=MODEL,  # Model yang digunakan untuk menghasilkan respons
            messages=prompt,  # Pesan yang diberikan ke model
            temperature=0.8,  # Mengatur randomisasi output
            max_tokens=100  # Jumlah maksimum token dalam respons
        )

        # Mengambil respons dari hasil yang dihasilkan oleh model
        greeting_response = response.choices[0].message.content
        
        # Mengembalikan respons yang sudah di-strip untuk menghilangkan spasi di awal dan akhir
        return {"message": greeting_response.strip(), "index": ""}
    
    except Exception as e:
        # Menangani pengecualian dan mengembalikan pesan kesalahan default
        error = "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"
        return {"message": error, "index": ""}
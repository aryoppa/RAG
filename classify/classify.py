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
MODEL = "gpt-3.5-turbo-0125"
# MODEL = "gpt-4o"

# Mendefinisikan fungsi untuk mengklasifikasikan input pengguna sebagai salam atau pertanyaan
def classify_input(user_input: str, tag=None) -> str:
    try:
        # Pesan sistem yang memberikan instruksi kepada model
        system_message =  f"""
            You are a virtual assistant that helps to classify user input as a label. \n
            You will be provided with user queries. \n
            You are required to classify the user input into one of the labels: 'greeting', 'absurd_question', 'faq_question', 'tracking_question'. \n

            Here is an example of a user query with category: \n

            A. Example 'absurd_question':\n
                1. Example Question: "p" \n
                2. Example Question: "jdjnc8e" \n

            B. Example category 'greeting':\n
                1. Example Question: "Halo mas" \n
                2. Example Question: "Hi" \n
                3. Example Question: "siang" \n
                4. Example Question: "malam" \n
                5. Example Question: "selamat malam" \n

            C. Example category 'faq_question':\n
                1. Example Question: "PIB itu apa" \n
                2. Example Question: "Alamat Lnsw" \n
                3. Example Question: "Apa itu ecoo" \n
                4. Example Question: "cara tracking registrasi insw" \n
                5. Example Question: "saya menemukan bug" \n

            D. Category 'tracking_question': Queries must include a 26-digit number. If no Aju 26-digit number is present, or only include "pengajuan" or "aju" sentence , then its not tracking_question:\n

            Example category 'tracking_question': \n
            Example of Valid and Correct Format: \n
            1. 'SSM QC [13 digit angka]' \n
            2. 'SSM PERIZINAN [13 digit angka]' \n
            3. 'NOMOR AJU [24 digit angka dan huruf]' \n
            Contoh Input: \n
            1. SSM QC 1234567890123 \n
            2. SSM PERIZINAN 1234567890123 \n
            3. NOMOR AJU A23456789123456789123456\n

            You Should only return the label without any additional sentences\n
        """
        
        # Membuat prompt dengan dua pesan: sistem dan pengguna
        prompt = [
            {
                "role": "system",
                "content": f"{system_message}"
            },
            {
                "role": "user",
                "content": f"{user_input}"
            }
        ]
        
        # Mengirimkan permintaan ke API OpenAI untuk menghasilkan respons
        response = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            temperature=0.0,  # Mengatur randomisasi output menjadi deterministik
            max_tokens=10,    # Jumlah maksimum token dalam respons
            stop=["\n"],      # Menghentikan respons di karakter newline
        )
        
        # Ekstrak label yang dihasilkan dari respons
        label = response.choices[0].message.content
        # print(f"Label : {label}")
        return label
    except Exception as e:
        # Menangani pengecualian dan mengembalikan pesan kesalahan default
        error = "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"
        return {"message": error, "index": "", "tag": ""}

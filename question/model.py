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
TOP_N = 3
MODEL = "gpt-3.5-turbo-0125"
# MODEL = "gpt-4o"

# Mendefinisikan fungsi untuk mendapatkan inti pertanyaan dari user
def understanding_question(question: str) -> str:
    # Instruksi Prompt Sistem, Perhatikan pembuatan prompt
    system_content = f"""
        You are a virtual assistant that helps find the core essence of user questions. \n
        You will be provided with user queries or questions. \n
        Review and understand the context of the user's question, and return it in the same language based on the core essence of the question. \n
        Give the results in a neutral language format which is not in the form of a question sentence.\n
        Never paraphrase or explain abbreviations or words you do not understand. \n
        You are a closed-domain assistant and never engage in topics unrelated to the provided context and question. \n

        #EXAMPLE 1: \n
        Input: "SSM qc apa?" \n
        Response: "penjelasan tentang ssm qc" \n

        #EXAMPLE 2: \n
        Input: "pelabuhan yang sudah implementasi ssm pengangkut" \n
        Response: "list pelabuhan yang sudah mengimplementasikan ssm pengangkut" \n

        #EXAMPLE 3: \n
        Input: "Lapor bug" \n
        Response: "Cara melakukan pelaporan bug" \n
    """

    prompt = [
        # Pesan sistem memberikan instruksi kepada model tentang bagaimana menjawab pertanyaan, dan hasil semantic search FAQ
        {"role": "system", "content": system_content},
        # Pesan pengguna pertanyaan pengguna
        {"role": "user", "content": question},
    ]

    try:
        # Mengirimkan permintaan ke API OpenAI untuk menghasilkan respons
        response = client.chat.completions.create(
            model=MODEL,  # Model yang digunakan untuk menghasilkan respons
            messages=prompt,  # Pesan yang diberikan ke model
            temperature=0,  # Mengatur randomisasi output menjadi deterministik
            max_tokens=150  # Jumlah maksimum token dalam respons
        )

        # Mengambil respons dari hasil yang dihasilkan oleh model
        final_response = response.choices[0].message.content.strip()
        return final_response

    except Exception as e:
        # Menangani pengecualian jika terjadi kesalahan pada API call
        error = "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"
        return {"message": error, "index": "", "tag": ""}

# Mendefinisikan fungsi untuk memproses pertanyaan pengguna
def process_question(question: str, tag) -> str:
    try:
        # Memuat data yang dibutuhkan untuk setiap pertanyaan
        df = load_data(tag=tag)
        # Mencari hasil yang relevan dalam notebook berdasarkan pertanyaan pengguna
        search_results = search_notebook(df, question, top_n=TOP_N)
        # Jika hasil pencarian ditemukan
        if search_results:
            # Instruksi Prompt Sistem, Perhatikan pembuatan prompt
            system_content = f"""
            You are a virtual assistant that helps to answer user question\n
            You will be provided with user queries and 'FAQ Data' A frequently asked questions (FAQ) list. \n
            You are required to answers user queries with information directly from the 'FAQ Data' that provided to you. \n  
            You are closed-domain and never engages in topics unrelated to provided context and question. \n
            If you dont know the answer, say you don't know\n  
            You are require to answer user question in formal bahasa indonesia.\n
            You are required to review again your answer, make sure give correct response base on clear instruction above. \n
            """

            prompt = [
                # Pesan sistem memberikan instruksi kepada model tentang bagaimana menjawab pertanyaan, dan hasil semantic search FAQ
                {"role": "system", "content": system_content},
                # Pesan pengguna pertanyaan pengguna
                {"role": "user", "content": f"""
                User Question/Queries: {question}. \n
                A frequently asked questions (FAQ) list: {search_results['konten']}. \n
                """},
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
            
            tags = search_results['tag']
            return {"message": final_response, "index": indexes, "tag": tags}
        else:
            # Jika tidak ada hasil pencarian yang ditemukan
            no_result = "Maaf, saya tidak bisa menemukan informasi yang sesuai dengan pertanyaan Anda. Mohon berikan detail pertanyaannya agar saya dapat memberikan bantuan yang lebih spesifik"
            return {"message": no_result, "index": "", "tag":""}
    except TypeError:
        # Menangani pengecualian jika terjadi TypeError
        error = "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"
        return {"message": error, "index": "", "tag":""}


# Mendefinisikan fungsi untuk melakukan validasi apakah jawaban dari "process_question" sesuai dengan pertanyaan 'question' dari user dan referensi 'search_results['konten']' yang diberikan
def validate_question(question: str, tag) -> str:
    try:
        # Memuat data yang dibutuhkan untuk setiap pertanyaan berdasarkan tag/kategori
        df = load_data(tag=tag)
        # Mencari hasil yang relevan dalam notebook berdasarkan pertanyaan pengguna
        search_results = search_notebook(df, question, top_n=TOP_N)
        # Jika hasil pencarian ditemukan
        if search_results:
            # Memanggil fungsi untuk mendapatkan inti dari pertanyaan user
            core_question = understanding_question(question)
            # Memanggil fungsi untuk memberikan jawaban dari inti pertanyaan user berdasarkan FAQ
            processed_response = process_question(question,tag=tag)
            # Mengambil hasil jawaban dalam bentuk json, hanya mengambil hasil response 'message'
            processed_message = processed_response.get("message")

            # Prompt untuk melakukan validasi jawaban berdasarkan pertanyaan original user, inti pertanyaan user, dan referensi hasil dari FAQ
            system_content = """
            You are a virtual assistant that validates responses to user questions. \n
            You will be provided with the user's original question, the core essence of the question, the response generated for the question, and the reference data.\n
            Your task is to validate whether the generated response correctly answers the core essence of the user's question based on the reference data.\n
            Please note that not all information in the reference data may be correct. Your goal is to check if any part of the reference data includes the correct answer.\n
            If the response is correct and answers the user's question, label it as TRUE. If not, label it as FALSE.
            """

            prompt = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": f"Original Question: {question}\nCore Essence of Question: {core_question}\nGenerated Response: {processed_message}\nReference Data: {search_results['konten']}"}
            ]

            response = client.chat.completions.create(
                model=MODEL,
                messages=prompt,
                temperature=0,
                max_tokens=20,
            )

            validation_response = response.choices[0].message.content
            # Jika Jawaban yang diberikan telah sesuai dengan pertanyaan user serta referensi, maka langsung berikan jawaban sebelumnya
            if "TRUE" in validation_response:
                return processed_response
            else:
                return {"message": "Maaf, saya tidak bisa menemukan informasi yang sesuai dengan pertanyaan Anda. Mohon berikan detail pertanyaannya agar saya dapat memberikan bantuan yang lebih spesifik", "index": "", "tag":""}

        else:
            return {"message": "Maaf, saya tidak bisa menemukan informasi yang sesuai dengan pertanyaan Anda. Mohon berikan detail pertanyaannya agar saya dapat memberikan bantuan yang lebih spesifik", "index": "", "tag":""}
        
    except TypeError:
        return {"message": "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?", "index": "", "tag":""}
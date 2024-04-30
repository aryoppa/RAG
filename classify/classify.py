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

# Define function to classify user input as a greeting or question
def classify_input(user_input: str) -> str:
    try:
        system_message =  f"""
            You are virtual assisstant that help to classify user input as label. \n
            You will be provided with user queries. \n
            You are required to classify the user input into one of the label: 'greeting', 'absurd_question', 'faq_question', 'tracking_question'. \n
            Only one label should be assigned to each user_input. and oly return label \n

            Here is an example of a user query for each category: \n
            A. example 'absurd_question':\n
                1. Contoh Pertanyaaan: "p" \n
                2. Contoh Pertanyaaan: "jdjnc8e" \n

            B. example category 'greeting':\n
                1. Contoh Pertanyaan: "Halo mas" \n
                2. Contoh Pertanyaan: "Hi" \n
                3. Contoh Pertanyaan: "siang" \n
                4. Contoh Pertanyaan: "malam" \n
                5. Contoh Pertanyaan: "selamat malam" \n

            C. example category 'faq_question':\n
                1. Contoh Pertanyaan: "PIB itu apa" \n
                2. Contoh Pertanyaan: "Alamat Lnsw" \n
                3. Contoh Pertanyaan: "Apa itu ecoo" \n
                4. Contoh Pertanyaan: "cara tracking registrasi insw" \n
                5. Contoh Pertanyaan: "saya menemukan bug" \n

            D. example category 'tracking_question':\n
                    1. Cek Aju: \n
                    - Format: "Status aju aju / Respon aju [Aju 26 digit]" \n
                    - Contoh Pertanyaan: "Status aju 00009001061720231212991201" \n

                    2. Cek NPE/SPPB/SPTNP: \n
                    - Format: "Cek sptnp/npw/sppb aju [Aju 26 digit]" \n
                    - Contoh Pertanyaan: "sptnp aju 00009001061720231212991201" \n
                    - Contoh Pertanyaan: "sppb aju 00009001061720231212991201" \n
                    - Contoh Pertanyaan: "npe aju 00009001061720231212991201" \n

                    3. Cek Tiket BCare: \n
                    - Format: "Status tiket / Tracking tiket [nomor tiket]" \n
                    - Contoh Pertanyaan: "Status tiket 300001" \n     
        """
        prompt = [  
                    {'role':'system', 
                    'content': system_message}, 
                    {'role':'user',
                    'content': f"Classify what label is this :{user_input}"}

                ] 
        response = ""
        for chunk in client.chat.completions.create(
                model="gpt-3.5-turbo", messages=prompt, stream=True, temperature=0.2, max_tokens=20
        ):
            text = chunk.choices[0].delta.content
            if text is not None:
                response += text
        print(response)
        return response.strip()
    except Exception:
        return "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"
    
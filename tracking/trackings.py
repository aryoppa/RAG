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

data = f"""

Data Aju 00003002604120231229000013 dengan status berikut:

No Daftar: 600045
Daftar: 23-01-2024

2023-12-29 23:49:08.547
Perekaman Dokumen

2024-01-05 14:52:20.859
Payment Verification

2024-01-05 16:48:01.14
Siap Jalur

2024-01-05 16:48:30.182
Penjaluran

2024-01-05 16:49:00.287
Pemeriksaan Dokumen

2024-01-05 16:49:00.291
Gate In TPS

2024-01-17 12:29:05.887
Perekaman Perbaikan Portal

2024-01-17 12:36:59.969
Validasi Perbaikan

"""
def process_tracking(tracking: str) -> str:
    try:
        system_message =  f"""
        You will be provided with user queries. \n
        Answer using Bahasa Indonesia. Don't make up the answer. If the answer cannot be found, write 'Maaf saya tidak memiliki data terkait di dalam databse saya' \n
        """
        prompt = [  
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"Answer user tracking questions:{tracking} based on the information provided in {data}, Give Detail information about the tracking status."},  
        ] 
        response = client.chat.completions.create(
            model=MODEL, messages=prompt, temperature=0.2, max_tokens=1000
        )

        final_response = response.choices[0].message.content
        return final_response  
    except TypeError:
        return "Data diluar konteks yang ada, mohon masukan pertanyaan lainnya"
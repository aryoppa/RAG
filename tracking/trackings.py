import os
from openai import OpenAI
from dotenv import load_dotenv
import requests  

# Set OpenAI API key
load_dotenv(override=True)
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

MODEL = "gpt-3.5-turbo"

def extract_information_as_string(data_raw):
    # Extracting HEADER information
    header_info = data_raw["HEADER"][0]
    nomor_aju = header_info["NOMOR_AJU"]
    nomor_daftar = header_info["NOMOR_DAFTAR"]
    tanggal_daftar = header_info["TANGGAL_DAFTAR"]
    kode_dokumen = header_info["KODE_DOKUMEN"]
    kode_kantor = header_info["KODE_KANTOR"]
    nama_perusahaan = header_info["NAMA_PERUSAHAAN"]

    # Extracting DETIL_PROSES information
    detil_proses = "\n".join([f"{detil['KODE_PROSES']}: {detil['NAMA_PROSES']} - {detil['WAKTU_PROSES']}" for detil in data_raw["DETIL_PROSES"]])

    # Extracting DETIL_RESPON information
    detil_respon = "\n".join([f"{respon['KODE_RESPON']}: {respon['NAMA_RESPON']} - {respon['NOMOR_RESPON']}, {respon['TANGGAL_RESPON']}, {respon['WAKTU_RESPON']}" for respon in data_raw["DETIL_RESPON"]])

    # Returning extracted information as string
    return f"NOMOR_AJU: {nomor_aju}\nNOMOR_DAFTAR: {nomor_daftar}\nTANGGAL_DAFTAR: {tanggal_daftar}\nKODE_DOKUMEN: {kode_dokumen}\nKODE_KANTOR: {kode_kantor}\nNAMA_PERUSAHAAN: {nama_perusahaan}\n\nDETIL_PROSES:\n{detil_proses}\n\nDETIL_RESPON:\n{detil_respon}"

def process_tracking(tracking: str) -> str:
    try:
        system_message =  f"""
        Your task is to extract Nomor Aju (26 digit number consisting of number and alphabet) from the tracking number from user input. \n
        Please only return the Nomor Aju value (26 digit number consisting of number and alphabet) from the tracking number. \n
        example: \n
        30101A0B50EA2013042900003B \n

        so in this case, your task is to only return '30101A0B50EA2013042900003B' from the tracking number.
        dont include the 'Nomor Aju' or any sentence other than value in  word in the response.
        """
        prompt = [  
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"Extract: {tracking}."}  
        ] 
        response = client.chat.completions.create(
            model=MODEL, messages=prompt, temperature=0.0, max_tokens=500
        )

        nomor_aju = response.choices[0].message.content.strip().upper()
        # print(nomor_aju)
        # Make API call using the extracted "No Aju" value
        api_url = f"http://10.239.13.192/TrackingCeisaService/getStatus?noAju={nomor_aju}"
        # # Make the API call using the api_url
        data_raw = requests.get(api_url)
        data_raw = data_raw.json()
        
        if "HEADER" not in data_raw or not data_raw["HEADER"]:
            return "Data tidak ditemukan, mohon masukan nomor aju yang benar"
        else:
            # Extracting required fields
            extracted_info_str = extract_information_as_string(data_raw)
            return extracted_info_str
        # return api_url
    except TypeError:
        return "Data diluar konteks yang ada, mohon masukan pertanyaan lainnya"

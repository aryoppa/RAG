import os
from openai import OpenAI
from dotenv import load_dotenv
import requests  

# Memuat kunci API OpenAI dari file .env
load_dotenv(override=True)

# Inisialisasi klien OpenAI dengan kunci API yang dimuat dari variabel lingkungan
client = OpenAI(
    # Ini adalah default dan bisa diabaikan
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Menentukan model yang akan digunakan untuk interaksi dengan OpenAI API
MODEL = "gpt-3.5-turbo-0125"

# Fungsi untuk mengekstrak informasi dari data mentah dari Ceaisa menjadi string terformat, dan hanya mengambil beberapa bagian informasi saja
def extract_information_as_string(data_raw):
    # Ekstraksi informasi HEADER
    header_info = data_raw["HEADER"][0]
    nomor_aju = header_info["NOMOR_AJU"]
    nomor_daftar = header_info["NOMOR_DAFTAR"]
    tanggal_daftar = header_info["TANGGAL_DAFTAR"]
    kode_dokumen = header_info["KODE_DOKUMEN"]
    kode_kantor = header_info["KODE_KANTOR"]
    nama_perusahaan = header_info["NAMA_PERUSAHAAN"]

    # Ekstraksi informasi DETIL_PROSES
    detil_proses = "\n".join([f"{detil['KODE_PROSES']}: {detil['NAMA_PROSES']} - {detil['WAKTU_PROSES']}" for detil in data_raw["DETIL_PROSES"]])

    # Ekstraksi informasi DETIL_RESPON
    detil_respon = "\n".join([f"{respon['KODE_RESPON']}: {respon['NAMA_RESPON']} - {respon['NOMOR_RESPON']}, {respon['TANGGAL_RESPON']}, {respon['WAKTU_RESPON']}" for respon in data_raw["DETIL_RESPON"]])

    # Mengembalikan informasi yang diekstrak sebagai string terformat
    return f"NOMOR_AJU: {nomor_aju}\nNOMOR_DAFTAR: {nomor_daftar}\nTANGGAL_DAFTAR: {tanggal_daftar}\nKODE_DOKUMEN: {kode_dokumen}\nKODE_KANTOR: {kode_kantor}\nNAMA_PERUSAHAAN: {nama_perusahaan}\n\nDETIL_PROSES:\n{detil_proses}\n\nDETIL_RESPON:\n{detil_respon}"

# Fungsi untuk memproses tracking berdasarkan nomor aju yang diberikan pengguna
def process_tracking(tracking: str) -> str:
    try:
        # Pesan sistem yang menjelaskan tugas untuk mengekstrak nomor aju dari input pengguna
        system_message =  f"""
        Your task is to extract Nomor Aju (26 digit number consisting of number and alphabet) from the tracking number from user input. \n
        Please only return the Nomor Aju or Nomor Pengajuan value (26 digit number consisting of number and alphabet) from the tracking number. \n
        example: 30101A0B50EA2013042900003B \n

        so in this case, your task is to only return '30101A0B50EA2013042900003B' from the tracking number.
        dont include the 'Nomor Aju', 'Nomor Pengajuan' or any sentence other than value in  word in the response.
        """
        # Membuat prompt untuk dikirim ke OpenAI API
        prompt = [  
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"Extract: {tracking}."}  
        ] 
        # Mengirim prompt ke OpenAI API dan mendapatkan respons
        response = client.chat.completions.create(
            model=MODEL, messages=prompt, temperature=0.0, max_tokens=500
        )

        # Mengekstrak nomor aju dari respons API
        nomor_aju = response.choices[0].message.content.strip().upper()
        
        # Membuat panggilan API menggunakan nomor aju yang diekstrak
        api_url = f"http://10.239.13.192/TrackingCeisaService/getStatus?noAju={nomor_aju}"
        data_raw = requests.get(api_url)
        data_raw = data_raw.json()
        
        # Memeriksa apakah data ditemukan dalam respons API
        if "HEADER" not in data_raw or not data_raw["HEADER"]:
            no_aju_invalid = "Data tidak ditemukan, mohon masukan nomor aju yang benar"
            return {"message": no_aju_invalid, "index":""}
        else:
            # Mengekstrak informasi yang diperlukan dan mengembalikannya sebagai string terformat
            extracted_info_str = extract_information_as_string(data_raw)
            return {"message":extracted_info_str, "index":""}
        
    except TypeError:
        error = "Maaf, saya tidak bisa menghasilkan respons saat ini. Bagaimana saya bisa membantu Anda?"
        return {"message": error, "index": "", "tag": ""}

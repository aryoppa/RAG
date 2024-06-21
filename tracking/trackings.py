import requests

FORMAT_INPUT = """
Format input tidak dikenali. \n
Contoh format yang valid: \n
1. 'QC [24 digit angka]' \n
2. 'PERIZINAN [24 digit angka]' \n
3. 'STATUS AJU [minimal 20 karakter alfanumerik]' \n
Contoh Input: \n
1. QC 123456789012345678901234 \n
2. PERIZINAN 123456789012345678901234 \n
3. STATUSAJU 123456789012345678901234 \n
"""

DATA_NOT_FOUND = f"""
Mohon Maaf data terkait tidak dapat ditemukan.
"""

#Minimum jumlah digit Number Tracking
LENGTH_NUM = 24

# Bagian yang ingin diambil dari 'STATUS AJU'
def DATA_NO_AJU(data_raw):
    header_info = data_raw["HEADER"][0]
    nomor_aju = header_info["NOMOR_AJU"]
    nomor_daftar = header_info["NOMOR_DAFTAR"]
    tanggal_daftar = header_info["TANGGAL_DAFTAR"]
    kode_dokumen = header_info["KODE_DOKUMEN"]
    kode_kantor = header_info["KODE_KANTOR"]
    nama_perusahaan = header_info["NAMA_PERUSAHAAN"]

    detil_proses = "\n".join([f"{detil['KODE_PROSES']}: {detil['NAMA_PROSES']} - {detil['WAKTU_PROSES']}" for detil in data_raw.get("DETIL_PROSES", [])])
    detil_respon = "\n".join([f"{respon['KODE_RESPON']}: {respon['NAMA_RESPON']} - {respon['NOMOR_RESPON']}, {respon['TANGGAL_RESPON']}, {respon['WAKTU_RESPON']}" for respon in data_raw.get("DETIL_RESPON", [])])

    return f"NOMOR_AJU: {nomor_aju}\nNOMOR_DAFTAR: {nomor_daftar}\nTANGGAL_DAFTAR: {tanggal_daftar}\nKODE_DOKUMEN: {kode_dokumen}\nKODE_KANTOR: {kode_kantor}\nNAMA_PERUSAHAAN: {nama_perusahaan}\n\nDETIL_PROSES:\n{detil_proses}\n\nDETIL_RESPON:\n{detil_respon}"

# FUNGSI MULTI API TRACKING
def process_tracking(tracking: str) -> dict:
    try:
        # Membagi input user menjadi keyword, action, dan number
        parts = tracking.split(maxsplit=1)
        
        if len(parts) != 2:
            return {"message": FORMAT_INPUT, "index": "", "tag": ""}
        
        keyword = parts[0].upper()
        number = parts[1]

        # Nomor aju dengan panjang lebih dari 20 karakter
        if keyword == "STATUSAJU" and len(number) >= LENGTH_NUM:
            api_url = f"http://10.239.13.192/TrackingCeisaService/getStatus?noAju={number}"
            response = requests.get(api_url)
            data_raw = response.json()
            if "HEADER" not in data_raw or not data_raw["HEADER"]:
                return {"message": DATA_NOT_FOUND, "index": "", "tag": ""}
            else:
                extracted_info_str = DATA_NO_AJU(data_raw)
                return {"message": extracted_info_str, "index": "", "tag": ""}
        # Parameter 13 digit number
        elif keyword == "QC" and len(number) >= LENGTH_NUM and number.isdigit():
            api_url = f"http://127.0.0.1:8001/api/ssmQC?no={number}"
            response = requests.get(api_url)
            data_raw = response.json()
            return {"message": data_raw.get("details", DATA_NOT_FOUND), "index": ""}
        
        # Parameter 13 digit number
        elif keyword == "PERIZINAN" and len(number) >= LENGTH_NUM and number.isdigit():
            api_url = f"http://127.0.0.1:8001/api/ssmPerizinan?no={number}"
            response = requests.get(api_url)
            data_raw = response.json()
            return {"message": data_raw.get("details", DATA_NOT_FOUND), "index": ""}
        else:
            return {"message": FORMAT_INPUT, "index": "", "tag": ""}
    
    except Exception as e:
        return {"message": f"Error: {str(e)}", "index": "", "tag": ""}

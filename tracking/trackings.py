import requests

FORMAT_INPUT = """
Format input tidak dikenali. \n
Contoh format yang valid: \n
1. 'SSM QC [13 digit angka]' \n
2. 'SSM PERIZINAN [13 digit angka]' \n
3. 'STATUS AJU [minimal 20 karakter alfanumerik]' \n
Contoh Input: \n
1. SSM QC 1234567890123 \n
2. SSM PERIZINAN 1234567890123 \n
3. STATUS AJU A23456789123456789123456\n
"""

DATA_NOT_FOUND = f"""
Mohon Maaf data terkait tidak dapat ditemukan
"""

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

def process_tracking(tracking: str) -> dict:
    try:
        # Membagi input user menjadi keyword, action, dan number
        parts = tracking.split(maxsplit=2)
        
        if len(parts) != 3:
            return {"message": FORMAT_INPUT, "index": "", "tag": ""}
        
        keyword = parts[0].upper()
        action = parts[1].upper()
        number = parts[2]

        # Nomor ajun dengan panjang lebih dari 20 karakter
        if keyword == "STATUS" and action == "AJU" and len(number) > 20:
            api_url = f"http://10.239.13.192/TrackingCeisaService/getStatus?noAju={number}"
            response = requests.get(api_url)
            data_raw = response.json()
            if "HEADER" not in data_raw or not data_raw["HEADER"]:
                return {"message": DATA_NOT_FOUND, "index": "", "tag": ""}
            else:
                extracted_info_str = DATA_NO_AJU(data_raw)
                return {"message": extracted_info_str, "index": "", "tag": ""}
        
        elif keyword == "SSM" and action == "QC" and len(number) == 13 and number.isdigit():
            api_url = f"http://127.0.0.1:8001/api/ssmQC?no={number}"
            response = requests.get(api_url)
            data_raw = response.json()
            return {"message": data_raw.get("details", DATA_NOT_FOUND), "index": ""}
        
        elif keyword == "SSM" and action == "PERIZINAN" and len(number) == 13 and number.isdigit():
            api_url = f"http://127.0.0.1:8001/api/ssmPerizinan?no={number}"
            response = requests.get(api_url)
            data_raw = response.json()
            return {"message": data_raw.get("details", DATA_NOT_FOUND), "index": ""}
        
        else:
            return {"message": FORMAT_INPUT, "index": "", "tag": ""}
    
    except Exception as e:
        return {"message": f"Error: {str(e)}", "index": "", "tag": ""}

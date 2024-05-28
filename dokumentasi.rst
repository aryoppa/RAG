```
LLM API Chatbot
===============

API ini menyediakan layanan chatbot menggunakan model bahasa berbasis OpenAI, dengan kemampuan untuk mengklasifikasikan input pengguna, menjawab pertanyaan, dan melacak status pengajuan.

Struktur Proyek
---------------

1. **classify.py**: Mendefinisikan fungsi untuk mengklasifikasikan input pengguna sebagai salam atau pertanyaan, serta memberikan respons sesuai dengan klasifikasi.

2. **greeting.py**: Berisi fungsi untuk merespons salam pengguna dengan pesan yang sesuai.

3. **model.py**: Memproses pertanyaan pengguna dan memberikan respons berdasarkan konteks data yang diberikan.

4. **tracking.py**: Menangani permintaan untuk melacak status pengajuan dengan mengekstrak nomor aju dari input pengguna dan mengambil informasi terkait dari sumber data eksternal.Menggunakan nomor aju yang diekstrak, permintaan API dibuat ke layanan API Ceisa
   - `http://10.239.13.192/TrackingCeisaService/getStatus?noAju={nomor_aju}`
   
5. **utils.py**: Berisi fungsi utilitas untuk memuat data, menghasilkan embedding teks, menghitung kemiripan kosinus, dan melakukan pencarian dalam dataset.
   - `get_embedding`: Menghasilkan embedding untuk input teks.
   - `load_data`: Memuat data untuk model.
   - `cosine_similarity`: Menghitung kesamaan kosinus antara vektor.
   - `search_notebook`: Melakukan kueri pencarian pada notebook.

6. **app.py**: Mendefinisikan endpoint API menggunakan FastAPI dan menangani logika bisnis untuk menjawab permintaan pengguna.

Cara Menjalankan Aplikasi
--------------------------

1. Instal dependensi yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```

2. Pastikan telah mengatur variabel lingkungan, terutama `OPENAI_API_KEY`, dengan kunci API OpenAI yang valid. Buat file '.env' yang berisi OPENAI_API_KEY='xxxxxxxxxxxxxxxx'.

3. Jalankan FastAPI server menggunakan uvicorn:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
   API akan aktif di `http://localhost:8000`.

Contoh Penggunaan API
---------------------

Anda dapat berinteraksi dengan API menggunakan permintaan HTTP, seperti `curl` atau Postman. Berikut adalah beberapa contoh permintaan:

1. Melakukan percakapan dengan chatbot:
   ```bash
   curl -X POST "http://localhost:8000/chatbot/" -H "Content-Type: application/json" -d '{"text": "Halo"}'
   ```
   ```
    {
        "data": {
            "message": "Halo! Ada yang bisa saya bantu?",
            "index": ""
        }
    }
   ```
2. Mengajukan pertanyaan:
   ```bash
   curl -X POST "http://localhost:8000/chatbot/" -H "Content-Type: application/json" -d '{"text": "Apa itu PIB?"}'
   ```
   ```
    {
        "data": {
            "message": "Pemberitahuan Impor Barang (PIB) adalah dokumen pemberitahuan oleh importir kepada bea cukai atas barang impor, berdasarkan dokumen pelengkap pabean sesuai prinsip self assessment.",
            "index": "[206, 25, 31, 353, 133]"
        }
    }
   ```
3. Melacak status pengajuan:
   ```bash
   curl -X POST "http://localhost:8000/chatbot/" -H "Content-Type: application/json" -d '{"text": "Status pengajuan 00009001061720231212991201"}'
   ```
   ```
    {
        "data": {
            "message": "Data tidak ditemukan, mohon masukan nomor aju yang benar",
            "index": ""
        }
    }
   ```
   ```
    {
        "data": {
            "message": "NOMOR_AJU: 00002081911420231228000002\nNOMOR_DAFTAR: 600003\nTANGGAL_DAFTAR: 2024-01-05T06:16:00.000Z\nKODE_DOKUMEN: 20\nKODE_KANTOR: 081400\nNAMA_PERUSAHAAN: SYIFA TRANS\n\nDETIL_PROSES:\n130: Penerimaan Dokumen - None\n990: Arsip - 2024-04-18 08:32:08\n400: Pemeriksaan Dokumen - 2024-01-06 14:22:43\n333: Perekaman LHP - 2024-01-06 14:16:14\n331: Perekaman BAP - 2024-01-06 14:13:18\n330: Pemeriksaan Barang - 2024-01-05 16:00:00\n314: Pengeluaran Kemasan - 2024-01-05 15:29:00\n311: Penunjukan PFPB - 2024-01-05 13:48:41\n310: Kesiapan Barang - 2024-01-05 13:48:41\n312: Instruksi Pemeriksaan - 2024-01-05 13:48:41\n300: Pemeriksaan Fisik - 2024-01-05 13:16:00\n250: Penomoran - 2024-01-05 13:16:00\n240: Penjaluran - 2024-01-05 13:15:30\n230: Siap Jalur - 2024-01-05 13:15:22\n110: Validasi - 2024-01-05 13:09:57\n107: LNSW - Analyzing Point - 2024-01-05 12:53:38\n106: LNSW - Cek Mandatory Content - 2024-01-05 12:53:25\n105: LNSW - Penerimaan Dokumen - 2024-01-05 12:50:28\n001: Perekaman Dokumen - 2024-01-05 12:40:31\n\nDETIL_RESPON:\n2008: BERITA ACARA HASIL PEMERIKSAAN - 600001/KBC.1306/2024, 2024-01-06 14:22:43, 2024-01-06 14:22:43\n2007: LAPORAN HASIL PEMERIKSAAN - 600001/KBC.1306/2024, 2024-01-06 14:22:43, 2024-01-06 14:22:43\n2066: INSTRUKSI PEMERIKSAAN - 600001/KBC.1306/2024, 2024-01-05 13:48:41, 2024-01-05 13:48:41\n2005: SURAT PEMBERITAHUAN JALUR MERAH (SPJM) - 600001/KBC.1306/2024, 2024-01-05 13:16:00, 2024-01-05 13:16:00\n2001: NOTA PEMBERITAHUAN PENOLAKAN (REJECT) - None, None, 2024-01-05 10:00:51\n2001: NOTA PEMBERITAHUAN PENOLAKAN (REJECT) - None, None, 2024-01-04 13:56:29\n2001: NOTA PEMBERITAHUAN PENOLAKAN (REJECT) - None, None, 2024-01-04 10:31:18\n2001: NOTA PEMBERITAHUAN PENOLAKAN (REJECT) - None, None, 2023-12-30 10:15:53\n2001: NOTA PEMBERITAHUAN PENOLAKAN (REJECT) - None, None, 2023-12-29 09:45:12",
            "index": ""
        }
    }
   ```
```
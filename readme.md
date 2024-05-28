# LLM API Chatbot

API ini memberikan layanan chatbot menggunakan model bahasa berbasis OpenAI, termasuk fungsionalitas seperti mengklasifikasikan input pengguna, menjawab pertanyaan, dan melacak status pengajuan.

## Struktur Proyek:

1. **classify.py**: Mendefinisikan fungsi untuk mengklasifikasikan input pengguna sebagai salam atau pertanyaan, serta memberikan respons sesuai dengan klasifikasi.
   
2. **greeting.py**: Berisi fungsi untuk merespons salam pengguna dengan pesan yang sesuai.
   
3. **model.py**: Memproses pertanyaan pengguna dan memberikan respons berdasarkan konteks data yang diberikan.
   
4. **tracking.py**: Menangani permintaan untuk melacak status pengajuan dengan mengekstrak nomor aju dari input pengguna dan mengambil informasi terkait dari sumber data eksternal.
   
5. **utils.py**: Berisi fungsi utilitas untuk memuat data, menghasilkan embedding teks, menghitung kemiripan kosinus, dan melakukan pencarian dalam dataset.
    - `get_embedding`: Fungsi untuk menghasilkan embedding untuk input teks.
    - `load_data`: Fungsi untuk memuat data untuk model.
    - `cosine_similarity`: Fungsi untuk menghitung kesamaan kosinus antara vektor.
    - `search_notebook`: Fungsi untuk melakukan kueri pencarian pada notebook.
    
6. **app.py**: Mendefinisikan endpoint API menggunakan FastAPI dan menangani logika bisnis untuk menjawab permintaan pengguna.

## Cara Menjalankan Aplikasi:

1. Instal dependensi yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```

2. Pastikan telah mengatur variabel lingkungan, khususnya `OPENAI_API_KEY`, dengan kunci API OpenAI yang valid.
    Buat file '.env' yang berisi OPENAI_API_KEY='xxxxxxxxxxxxxxxx'

3. Jalankan FastAPI server menggunakan uvicorn:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```
   API akan menjadi aktif di `http://localhost:8000`.

## Contoh Penggunaan API:

Anda dapat berinteraksi dengan API menggunakan permintaan HTTP, misalnya menggunakan `curl` atau Postman. Berikut adalah beberapa contoh permintaan:

1. Melakukan percakapan dengan chatbot:
   ```bash
   curl -X POST "http://localhost:8000/chatbot/" -H "Content-Type: application/json" -d '{"text": "Halo"}'
   ```

2. Mengajukan pertanyaan:
   ```bash
   curl -X POST "http://localhost:8000/chatbot/" -H "Content-Type: application/json" -d '{"text": "Apa itu PIB?"}'
   ```

3. Melacak status pengajuan:
   ```bash
   curl -X POST "http://localhost:8000/chatbot/" -H "Content-Type: application/json" -d '{"text": "Status pengajuan 00009001061720231212991201"}'
   ```
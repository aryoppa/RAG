import os
import pandas as pd
import numpy as np
# from scipy.spatial.distance import cosine
from openai import OpenAI
from dotenv import load_dotenv

# Memuat kunci API OpenAI dari file .env
load_dotenv(override=True)

# Inisialisasi klien OpenAI dengan kunci API
client = OpenAI(
    # Ini adalah default dan bisa diabaikan
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Menentukan jumlah hasil pencarian teratas dan model embedding yang akan digunakan
TOP_N = 3

# Dataset berdasarkan kategori
DATASET_PATH_GENERAL = "data\embedd\BASE_DATA.csv"
DATASET_PATH_SSM_QC = "data\embedd\BASE_DATA_SSMQC.csv"
DATASET_PATH_UMKM_EKSPOR = "data\embedd\BASE_DATA_UMKMEKSPOR.csv"
DATASET_PATH_PENGANGKUT = "data\embedd\BASE_DATA_PENGANGKUT.csv"

#Embedding Model OPEN AI
EMBEDDING_MODEL = "text-embedding-ada-002"

# Fungsi untuk memuat data dari file CSV
def load_data(tag):
    # Membaca data dari file CSV
    if tag == "ssm_qc":
        data = pd.read_csv(DATASET_PATH_SSM_QC)
        # print("QC")
    elif tag == "pengangkut":
        data = pd.read_csv(DATASET_PATH_UMKM_EKSPOR)
        # print("Pengangkut")
    elif tag== "umkm_ekspor":
        data = pd.read_csv(DATASET_PATH_PENGANGKUT)
        # print("UMKM Ekspor")
    else: 
        data = pd.read_csv(DATASET_PATH_GENERAL)
        # print("General")
    # Mengganti nilai null dalam kolom 'embedding' dengan string kosong
    data['embedding'] = data['embedding'].fillna('none')
    return data

# Fungsi untuk mendapatkan embedding dari teks menggunakan model OpenAI
def get_embedding(text, model=EMBEDDING_MODEL):
    # Menghapus newline dari teks
    text = text.replace("\n", " ")
    # Membuat embedding untuk teks
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

# Fungsi untuk menghitung kemiripan kosinus antara dua embedding
def cosine_similarity(embedding1, embedding2):
    # Rumus Cosine Similarity
    dot_product = np.dot(embedding1, embedding2)
    magnitude_embedding1 = np.linalg.norm(embedding1)
    magnitude_embedding2 = np.linalg.norm(embedding2)
    cosine_similarity= dot_product / (magnitude_embedding1 * magnitude_embedding2)
    return cosine_similarity

# Fungsi untuk mencari hasil yang relevan dalam notebook berdasarkan pertanyaan pengguna
def search_notebook(df, question,tag=None, top_n=TOP_N):
    # Mengubah kolom 'embedding' menjadi array numpy
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    # Mendapatkan embedding untuk pertanyaan
    search_embeddings = get_embedding(question)
    # Menghitung kemiripan antara embedding pertanyaan dan embedding dalam dataset
    df["similarity"] = df['embedding'].apply(lambda x: cosine_similarity(x, search_embeddings))
    # Mengurutkan DataFrame berdasarkan kemiripan
    df = df.sort_values(by='similarity', ascending=False)
    # Mendapatkan n hasil teratas
    top_results = df.head(TOP_N)

    # Menyiapkan struktur untuk menyimpan dokumen yang mirip
    similar_docs = {
        "konten": ''' ''',
        "index": [],
        "tag": [],
    }

    # Menambahkan hasil pencarian ke struktur dokumen yang mirip
    for rows in top_results.itertuples():
        # Hanya mengambil data yang memiliki simmiliarity diatas 50%
        if rows.similarity < 0.5:
            similar_docs["konten"] += "Mohon Maaf saya tidak dapat menemukan data terkait"
        else:
            similar_docs["konten"] += rows.konten
            similar_docs["index"].append(rows.index)
            similar_docs['tag'].append(rows.tag if pd.notna(rows.tag) else 'General')  # Handling NaN tags
    return similar_docs

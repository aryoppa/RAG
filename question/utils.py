import os
import pandas as pd
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

# Memuat kunci API OpenAI dari file .env
load_dotenv(override=True)

# Inisialisasi klien OpenAI dengan kunci API
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Menentukan jumlah hasil pencarian teratas dan model embedding yang akan digunakan
TOP_N = 3

# Dataset berdasarkan kategori
DATASET_PATH_GENERAL = "data/embedd/BASE_DATA.csv"

# Embedding Model OpenAI
EMBEDDING_MODEL = "text-embedding-ada-002"

# Fungsi untuk memuat data dari file CSV
def load_data():
    data = pd.read_csv(DATASET_PATH_GENERAL)
    # Mengganti nilai null dalam kolom 'embedding' dengan string kosong
    data['embedding'] = data['embedding'].fillna('[]')
    return data

# Fungsi untuk mendapatkan embedding dari teks menggunakan model OpenAI
def get_embedding(text, model=EMBEDDING_MODEL):
    # Menghapus newline dari teks
    text = text.replace("\n", " ")
    try:
        # Membuat embedding untuk teks
        response = client.embeddings.create(input=[text], model=model)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []

# Fungsi untuk menghitung kemiripan kosinus antara dua embedding
def cosine_similarity(embedding1, embedding2):
    if len(embedding1) == 0 or len(embedding2) == 0:
        return 0
    # Rumus Cosine Similarity
    dot_product = np.dot(embedding1, embedding2)
    magnitude_embedding1 = np.linalg.norm(embedding1)
    magnitude_embedding2 = np.linalg.norm(embedding2)
    if magnitude_embedding1 == 0 or magnitude_embedding2 == 0:
        return 0
    cosine_similarity = dot_product / (magnitude_embedding1 * magnitude_embedding2)
    return cosine_similarity

# Fungsi untuk mencari hasil yang relevan dalam notebook berdasarkan pertanyaan pengguna
def search_notebook(df, question, tag=None, top_n=TOP_N):
    # Mengubah kolom 'embedding' menjadi array numpy
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)

    # Mendapatkan embedding untuk pertanyaan
    search_embeddings = get_embedding(question)

    # Menghitung kemiripan antara embedding pertanyaan dan embedding dalam dataset
    df["similarity"] = df['embedding'].apply(lambda x: cosine_similarity(x, search_embeddings))

    # Filter berdasarkan tag jika diberikan
    if tag:
        df = df[df['tag'].str.lower() == tag.lower()]

    # Mengurutkan DataFrame berdasarkan kemiripan
    df = df.sort_values(by='similarity', ascending=False)

    # Mendapatkan n hasil teratas
    top_results = df.head(top_n)

    # Menyiapkan struktur untuk menyimpan dokumen yang mirip
    similar_docs = {
        "konten": "",
        "index": [],
        "tag": [],
    }

    # Menambahkan hasil pencarian ke struktur dokumen yang mirip
    for row in top_results.itertuples():
        if row.similarity > 0.5:
            similar_docs["konten"] += row.konten
            similar_docs["index"].append(row.Index)  # Menggunakan row.Index untuk mendapatkan indeks baris
            similar_docs['tag'].append(row.tag if pd.notna(row.tag) else 'General')
    # Pesan default jika tidak ada hasil yang memadai
    if not similar_docs["konten"].strip():
        similar_docs["konten"] = "Mohon Maaf saya tidak dapat menemukan data terkait\n"
    # print(similar_docs)
    return similar_docs

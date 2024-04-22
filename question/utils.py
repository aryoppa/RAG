import os
import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
from openai import OpenAI
from dotenv import load_dotenv

# Set OpenAI API key
load_dotenv(override=True)
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

TOP_N = 3
DATASET_PATH = "question\\fix_pusatbantuan_embedding_text3small.csv"
EMBEDDING_MODEL = "text-embedding-3-small"

# Load data and define search function
def load_data():
    data = pd.read_csv(DATASET_PATH)
    # Replace null values in the 'embedding' column with an empty string
    data['embedding'] = data['embedding'].fillna('none')
    return data

def get_embedding(text, model=EMBEDDING_MODEL):
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def cosine_similarity(embedding1, embedding2):
    return 1 - cosine(embedding1, embedding2)

def search_notebook(df, question, top_n=TOP_N):
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    search_embeddings = get_embedding(question)
    df["similarity"] = df['embedding'].apply(lambda x: cosine_similarity(x, search_embeddings))
    # Sort the DataFrame by similarity
    df = df.sort_values(by='similarity', ascending=False)
    # Get the top n results
    top_results = df.head(TOP_N)
    similar_docs = {
                    "konten":''' ''',
                    "index": []
                    }
    for rows in top_results.itertuples():
        if rows.similarity < 0.5:
            similar_docs["konten"] += "Mohon Maaf saya tidak dapat menemukan data terkait"
        else:
            similar_docs["konten"] += rows.konten
            similar_docs["index"].append(rows.index)
    return similar_docs

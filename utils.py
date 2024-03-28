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

# Load data and define search function
def load_data():
    data = pd.read_csv('fix_pusatbantuan_embedding_text3small.csv')
    # Replace null values in the 'embedding' column with an empty string
    data['embedding'] = data['embedding'].fillna('none')
    return data

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def cosine_similarity(embedding1, embedding2):
    return 1 - cosine(embedding1, embedding2)

def search_notebook(df, question, top_n=1):
    df['embedding'] = df['embedding'].apply(eval).apply(np.array)
    search_embeddings = get_embedding(question)
    df["similarity"] = df['embedding'].apply(lambda x: cosine_similarity(x, search_embeddings))
    # Sort the DataFrame by similarity
    df = df.sort_values(by='similarity', ascending=False)
    # Get the top n results
    top_results = df.head(top_n)
    similar_docs = []
    for index, row in top_results.iterrows():
        if row['similarity'] < 0.5:
            similar_docs.append({"konten": "Mohon Maaf saya tidak dapat menemukan data terkait"})
        else:
            similar_docs.append({"konten": row['konten']})
    return similar_docs

1. utils.py : every function suh as get_embeding,load_data, cosine_similarity, search_notebook

2. model.py : consist of vector search and LLM model

3. app.py : api endpoint


Run app.py to activate the LLM API:
uvicorn app:app  --reload --host 0.0.0.0 --port 8000 (Server)

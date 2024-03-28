import requests

url = "http://localhost:8000/chatbot/"
payload = {"text": "alamat lnsw"} #data dalam konteks
# payload = {"text": "saya menemukan bug di website lnsw"} #data dalam konteks
# payload = {"text": "siapa prabowo subianto"} #data diluar konteks
# payload = {"text": "where is LNSW Adress"} #menggunakan bahasa inggris
# payload = {"text": "selamat malam"}

headers = {"Content-Type": "application/json"}
response = requests.post(url, json=payload, headers=headers)
print(response.text)

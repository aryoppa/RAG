from fastapi import FastAPI, Request
from pydantic import BaseModel
from classify.classify import classify_input
from question.model import process_question
from question.model import understanding_question
from tracking.trackings import process_tracking
from greeting.greetings import answer_greeting
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Definisi daftar asal yang diizinkan untuk permintaan lintas-domain (CORS)
origins = ["*"]

# Menambahkan middleware CORS untuk mengizinkan permintaan dari semua asal dengan semua metode dan header
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definisikan model Pydantic untuk data input
class InputData(BaseModel):
    text: str

# Definisikan API endpoint untuk menangani permintaan input dan mengembalikan respons
@app.post("/chatbot/")
async def chatbot_endpoint(input_data: InputData) -> str:
    text = input_data.text.strip().lower()
    classification = classify_input(text)
    
    if text in ["hi", "halo"]:
        response = answer_greeting(text)
    elif classification == "greeting":
        response = answer_greeting(text)
    elif classification == "absurd_question":
        response = {"message": "Maaf, saya tidak mengerti pertanyaan Anda. Bisakah Anda mengajukan pertanyaan lain?", "index": ""}
    elif classification == "faq_question":
        core_question = understanding_question(text)
        response = process_question(core_question)
    elif classification == "tracking_question":
        response = process_tracking(text)
    else:
        response = {"message": "Ada yang bisa saya bantu? Tolong berikan detail pertanyaannya agar saya bisa memberikan bantuan yang lebih spesifik.", "index": ""}
    
    return JSONResponse(content={"data": response})

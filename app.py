from fastapi import FastAPI, Request
from pydantic import BaseModel
from question.model import process_question
from greeting.greetings import answer_greeting, classify_input
from fastapi.middleware.cors import CORSMiddleware

# Inisialisasi aplikasi FastAPI
app = FastAPI()

origins = ["*"]

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
async def chatbot_endpoint(request: Request, input_data: InputData) -> str:
    text = input_data.text.strip().lower()
    if text in ["hi", "halo"]:
        return answer_greeting(text)
    elif classify_input(text) == "greeting":
        return answer_greeting(text)
    elif classify_input(text) == "absurd_question":
        return "Maaf, saya tidak mengerti pertanyaan Anda. Bisakah Anda mengajukan pertanyaan lain? dan "
    elif classify_input(text) == "question":
        return process_question(text)
    else:
        return "Ada yang bisa saya bantu? Tolong berikan detail pertanyaannya agar saya bisa memberikan bantuan yang lebih spesifik."        

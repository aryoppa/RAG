from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from model import process_question, answer_greeting, classify_input
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
@app.post("/chatbot/", response_model=dict)
async def chatbot_endpoint(input_data: InputData) -> dict:
    try:
        text = input_data.text.strip().lower()
        if text in ["hi", "halo"]:
            response_text = answer_greeting(text)
        elif classify_input(text) == "greeting":
            response_text = answer_greeting(text)
        elif classify_input(text) == "absurd_question":
            response_text = "Maaf, saya tidak mengerti pertanyaan Anda. Bisakah Anda mengajukan pertanyaan lain?"
        else:
            response_text = process_question(text)
        return JSONResponse(content={"message": response_text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

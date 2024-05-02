from flask import Flask, request, jsonify
from pydantic import BaseModel
from classify.classify import classify_input
from question.model import process_question
from tracking.trackings import process_tracking
from greeting.greetings import answer_greeting

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Allow CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Definisikan model Pydantic untuk data input
class InputData(BaseModel):
    text: str

# Definisikan API endpoint untuk menangani permintaan input dan mengembalikan respons
@app.route("/chatbot/", methods=["POST"])
def chatbot_endpoint():
    input_data = InputData(**request.json)
    text = input_data.text.strip().lower()
    if text in ["hi", "halo"]:
        return answer_greeting(text)
    elif classify_input(text) == "greeting":
        return answer_greeting(text)
    elif classify_input(text) == "absurd_question":
        return "Maaf, saya tidak mengerti pertanyaan Anda. Bisakah Anda mengajukan pertanyaan lain?"
    elif classify_input(text) == "faq_question":
        return process_question(text)
    elif classify_input(text) == "tracking_question":
        return process_tracking(text)
    else:
        return "Ada yang bisa saya bantu? Tolong berikan detail pertanyaannya agar saya bisa memberikan bantuan yang lebih spesifik."

if __name__ == "__main__":
    app.run(debug=True)

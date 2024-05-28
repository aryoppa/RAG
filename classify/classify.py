import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# Set OpenAI API key
load_dotenv(override=True)
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

MODEL = "gpt-3.5-turbo"
# MODEL = "gpt-4o"

# Define function to classify user input as a greeting or question
def classify_input(user_input: str) -> str:
    try:
        system_message =  f"""
            You are a virtual assistant that helps to classify user input as a label. \n
            You will be provided with user queries. \n
            You are required to classify the user input into one of the labels: 'greeting', 'absurd_question', 'faq_question', 'tracking_question'. \n
            Only one label should be assigned to user input, and only return the label. \n

            Here is an example of a user query category: \n
            A. Example 'absurd_question':\n
                1. Example Question: "p" \n
                2. Example Question: "jdjnc8e" \n

            B. Example category 'greeting':\n
                1. Example Question: "Halo mas" \n
                2. Example Question: "Hi" \n
                3. Example Question: "siang" \n
                4. Example Question: "malam" \n
                5. Example Question: "selamat malam" \n

            C. Example category 'faq_question':\n
                1. Example Question: "PIB itu apa" \n
                2. Example Question: "Alamat Lnsw" \n
                3. Example Question: "Apa itu ecoo" \n
                4. Example Question: "cara tracking registrasi insw" \n
                5. Example Question: "saya menemukan bug" \n

            D. Category 'tracking_question' must be include no Aju 26 digit or have ticket number using the following format: \n 
            
            Example category 'tracking_question':\n
                Here user ask about tracking status of aju. \n
                Check Aju: \n
                    - Example Format: "Status aju aju / Respon aju /Status pengajuan [Aju 26 digit]"\n
                    - Example Question: "Status aju 00009001061720231212991201" \n
                    - Example Question: "Status pengajuan 00009001061720231212991201" \n
                    - Example Question: "Respon aju 0009001061720231212991201" \n
                or other related format that means user ask about tracking status of aju but must be include 26 Digit Number(26 digit number consisting of number and alphabet)\n

                Please classify {user_input} and give only 1 sentence consist of one of the labels: 'greeting', 'absurd_question', 'faq_question', 'tracking_question'. \n
        """
        prompt = [
            {
                "role": "system",
                "content": f"{system_message}"
            },
            {
                "role": "user",
                "content": f"{user_input}"
            }
        ]
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=prompt,
            temperature=0.0,
            max_tokens=20,
            stop=["\n"],
        )
        # Extract the generated label from the completion
        label = response.choices[0].message.content
        return label
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't classify the input at the moment."


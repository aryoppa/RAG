import os
from openai import OpenAI
from dotenv import load_dotenv

# Set OpenAI API key
load_dotenv(override=True)
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

MODEL = "gpt-3.5-turbo"

# Define function to classify user input as a greeting or question
def classify_input(user_input: str) -> str:
    try:
        system_message =  f"""
            You are a virtual assistant that helps to classify user input as a label. \n
            You will be provided with user queries. \n
            You are required to classify the user input into one of the labels: 'greeting', 'absurd_question', 'faq_question', 'tracking_question'. \n
            Only one label should be assigned to each user input, and only return the label. \n

            Here is an example of a user query for each category: \n
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

            D. Category 'tracking_question' must be in the following format: \n 
            
            Example category 'tracking_question':\n
                    1. Check Aju: \n
                    - Format: "Status aju aju / Respon aju [Aju 26 digit]" \n
                    - Example Question: "Status aju 00009001061720231212991201" \n

                    2. Check NPE/SPPB/SPTNP: \n
                    - Format: "Check sptnp/npw/sppb aju [Aju 26 digit]" \n
                    - Example Question: "sptnp aju 00009001061720231212991201" \n
                    - Example Question: "sppb aju 00009001061720231212991201" \n
                    - Example Question: "npe aju 00009001061720231212991201" \n

                    3. Check Ticket BCare: \n
                    - Format: "Status ticket / Tracking ticket [ticket number]" \n
                    - Example Question: "Status ticket 300001" \n    
        """
        prompt = [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": f"Classify what label is this sentence: {user_input}"
            }
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            temperature=0.2,
            max_tokens=20
        )
        text = response.choices[0].delta.content
        if text is not None:
            return text.strip()
        return "Unable to classify the input."
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't generate a response at the moment. How can I assist you?"

# Example usage:
user_input = "Hi there"
print(classify_input(user_input))

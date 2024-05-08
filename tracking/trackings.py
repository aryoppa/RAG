import os
from openai import OpenAI
from dotenv import load_dotenv
import requests  

# Set OpenAI API key
load_dotenv(override=True)
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

MODEL = "gpt-3.5-turbo"
def process_tracking(tracking: str) -> str:
    try:
        system_message =  f"""
        Your task is to extract Nomor Aju (26 digit number consisting of number and alphabet) from the tracking number from user input. \n
        Please only return the Nomor Aju value (26 digit number consisting of number and alphabet) from the tracking number. \n
        example: \n
        30101A0B50EA2013042900003B \n

        so in this case, the your task is to only return '30101A0B50EA2013042900003B' from the tracking number.
        """
        prompt = [  
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"Extract Nomor Aju from tracking number : {tracking}."}  
        ] 
        response = client.chat.completions.create(
            model=MODEL, messages=prompt, temperature=0.1, max_tokens=500
        )

        no_aju = response.choices[0].message.content.strip().upper()
        print(no_aju)
        # Make API call using the extracted "No Aju" value
        api_url = f"http://10.239.13.192/TrackingCeisaService/getStatus?noAju={no_aju}"
        # # Make the API call using the api_url
        final_response = requests.get(api_url)
        final_response = final_response.json()
        
        tracking_status = str(final_response)

        return tracking_status
        # return api_url
    except TypeError:
        return "Data diluar konteks yang ada, mohon masukan pertanyaan lainnya"
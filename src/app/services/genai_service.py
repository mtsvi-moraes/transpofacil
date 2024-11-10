import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def get_response(input_text: str) -> str:
    chat_session = model.start_chat(
        history=[]
    )
    response = chat_session.send_message(input_text)
    return response.text
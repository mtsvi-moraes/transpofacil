import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai

class OlhoVivoService:
    def __init__(self):
        load_dotenv()  # Carregar variáveis de ambiente do .env
        self.api_key = os.getenv("OLHO_VIVO_API_KEY")
        self.session = requests.Session()
        self.base_url = "https://api.olhovivo.sptrans.com.br/v2.1"
        
        # Configuração da IA generativa
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        generation_config = {
            "temperature": 0,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

    def autenticar(self) -> bool:
        """Autentica na API do Olho Vivo."""
        url_login = f"{self.base_url}/Login/Autenticar"
        response = self.session.post(url_login, params={"token": self.api_key})
        return response.status_code == 200 and response.text.lower() == "true"

    def buscar_linhas(self, termos_busca: str) -> list:
        """Busca linhas de ônibus usando a API do Olho Vivo."""
        if not self.autenticar():
            raise Exception("Erro ao autenticar na API do Olho Vivo.")
        
        url_buscar_linha = f"{self.base_url}/Linha/Buscar"
        response = self.session.get(url_buscar_linha, params={"termosBusca": termos_busca})
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro ao buscar linhas: {response.status_code} - {response.text}")

    def gerar_resposta(self, linhas: list, prompt: str) -> str:
        """
        Utiliza a IA generativa para criar uma resposta baseada nos dados das linhas
        retornados pela API do Olho Vivo.
        """
        # Formatar as informações da linha para o prompt
        linhas_formatadas = "\n".join(
            [
                (
                    f"Código: {linha['cl']}\n"
                    f"Circular: {'Sim' if linha['lc'] else 'Não'}\n"
                    f"Letreiro numérico: {linha['lt']} - {linha['tl']}\n"
                    f"Sentido 1: {linha['tp']}\n"
                    f"Sentido 2: {linha['ts']}\n"
                )
                for linha in linhas
            ]
        )

        input_text = f"{prompt}\n\n{linhas_formatadas}"
        
        # Gerar a resposta com a IA
        chat_session = self.model.start_chat(history=[])
        response = chat_session.send_message(input_text)
        return response.text

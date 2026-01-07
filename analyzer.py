import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Сенің жаңа API кілтің
API_KEY = "GEMINI_API_KEY"
genai.configure(api_key=API_KEY)

def check_phishing_with_ai(text):
    """Gemini 2.5 Pro арқылы терең талдау"""
    try:
        # Нақты 2.5 Pro моделін шақыру
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        prompt = (
            f"Сен Warden-X киберқауіпсіздік маманысың. Мына мәтінді фишингке немесе алаяқтыққа мұқият талда: '{text}'. "
            f"Қауіп деңгейін 0-100 арасында көрсет және неге бұлай бағалағаныңды түсіндір. "
            f"Жауапты тек қазақ тілінде бер."
        )
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.replace("*", "")
        else:
            return "АИ жауап қайтармады. Қайтадан көріңіз."
            
    except Exception as e:
        # Егер 2.5 Pro-да квота немесе басқа қате болса, 2.5 Flash-қа автоматты ауысу (презентация қатып қалмауы үшін)
        try:
            model_flash = genai.GenerativeModel('gemini-2.5-flash')
            res = model_flash.generate_content(prompt)
            return res.text.replace("*", "")
        except:
            return f"ЖИ Қатесі: {str(e)}"
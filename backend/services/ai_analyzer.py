import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar el SDK de Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

async def analyze_trends(trends_data: list) -> dict:
    """
    Analiza la información cruda de tendencias usando Gemini
    y devuelve un resumen estructurado en formato JSON.
    """
    # Validación básica por si no hay clave
    if not api_key or api_key == "tu_clave_aqui":
        return {
            "error": "API Key de Gemini no configurada correctamente.",
            "main_topics": [], 
            "summary": "N/A", 
            "top_signals": []
        }

    try:
        # Configurar modelo con system instruction
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction="You are an expert AI Data Analyst. You receive raw tech news and must analyze emerging trends. You MUST always respond in valid JSON format."
        )
        
        # Configurar temperature para ser más analítico y preciso
        generation_config = genai.GenerationConfig(
            temperature=0.2,
            response_mime_type="application/json"
        )
        
        # Prompt pidiendo la estructura estricta
        prompt = f"""
        Analiza los siguientes datos de tendencias tecnológicas y devuelve un JSON con esta estructura exacta:
        {{"main_topics": ["topic1", "topic2"], "summary": "Un resumen ejecutivo de 3 líneas", "top_signals":[{{"topic": "Name", "importance": "High/Medium", "explanation": "Why it matters"}}]}}

        Datos a analizar:
        {json.dumps(trends_data, ensure_ascii=False)}
        """
        
        # Generar contenido de forma asíncrona
        response = await model.generate_content_async(
            prompt,
            generation_config=generation_config
        )
        
        # Limpiar la respuesta (por si acaso Gemini inserta tags markdown)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
            
        # Parsear string a diccionario Python
        result_dict = json.loads(text)
        return result_dict
        
    except Exception as e:
        print(f"Error en el análisis de IA: {e}")
        # En caso de que falle la API (bloqueo, rate limit, etc.)
        return {
            "error": str(e),
            "main_topics": ["Error de procesamiento"], 
            "summary": "Hubo un error al intentar generar el resumen con Gemini. Por favor, verifica la consola para más detalles.", 
            "top_signals": []
        }

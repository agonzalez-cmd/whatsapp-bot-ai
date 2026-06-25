import os
import google.generativeai as genai
from dotenv import load_dotenv
from knowledge_base import read_knowledge_base

load_dotenv()

# Configurar el SDK de Gemini (Motor del Agente Antigravity)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Instrucciones del sistema según especificaciones
SYSTEM_INSTRUCTIONS = """
Eres un asistente virtual profesional, amigable, cercano y empático de atención al cliente. 
Debes ser claro, educado y responder de forma breve y estructurada.

REGLAS ESTRICTAS:
1. FUENTE DE INFORMACIÓN: Tu única fuente de verdad es el documento proporcionado en el contexto. 
Si el usuario pregunta algo que NO está explícitamente en el contexto, DEBES responder cortésmente que no posees esa información y ofrecer derivar con un humano. 
2. NO INVENTAR: Bajo ninguna circunstancia debes inventar información, suponer, ni responder usando tu conocimiento general pre-entrenado. Si no está en el contexto, no lo sabes.
3. TONO: Mantén un tono estrictamente profesional pero amigable, cercano y empático.
4. EMOJIS: Utiliza un MÁXIMO de un (1) emoji por mensaje para mantener la calidez sin perder la formalidad.

Contexto de la Base de Conocimiento (única fuente de verdad):
{knowledge}
"""

def get_agent_response(user_message: str) -> str:
    """
    Genera una respuesta usando el SDK de Gemini configurado como el agente Antigravity.
    """
    if not GEMINI_API_KEY:
        return "El Agente no está configurado (Falta GEMINI_API_KEY)."

    try:
        # 1. Leer la base de conocimiento actualizada
        knowledge = read_knowledge_base()
        
        # 2. Preparar las instrucciones del sistema con el contexto inyectado
        instructions = SYSTEM_INSTRUCTIONS.format(knowledge=knowledge)
        
        # 3. Configurar el modelo
        # gemini-1.5-flash soporta system instructions y es muy rápido
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=instructions,
            generation_config=genai.GenerationConfig(
                temperature=0.1, # Baja temperatura para que no sea muy creativo e invente cosas
            )
        )
        
        # 4. Generar respuesta
        response = model.generate_content(user_message)
        return response.text.strip()
    
    except Exception as e:
        print(f"Error generando respuesta del agente: {e}")
        return "Lo siento, estoy experimentando dificultades técnicas en este momento. ¿Te gustaría que te derive a un humano?"

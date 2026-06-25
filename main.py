import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import get_agent_response

load_dotenv()

app = FastAPI(title="WhatsApp Bot AI Backend")

class MessagePayload(BaseModel):
    message: str
    sender: str

@app.post("/chat")
async def chat_endpoint(payload: MessagePayload):
    """
    Recibe un mensaje desde el script de Node.js,
    lo procesa con el agente de Gemini y devuelve la respuesta.
    """
    try:
        incoming_text = payload.message
        sender = payload.sender
        
        print(f"\n[+] Recibido de {sender}: {incoming_text}")
        
        # Pasar el mensaje por el Agente
        bot_reply = get_agent_response(incoming_text)
        print(f"[-] Respuesta del Agente a {sender}: {bot_reply}")
        
        # Devolver la respuesta al script puente
        return {"reply": bot_reply}
        
    except Exception as e:
        print(f"Error procesando el mensaje: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

if __name__ == "__main__":
    import uvicorn
    # Inicia el servidor local en el puerto especificado o en el 8000 por defecto
    port = int(os.environ.get("PORT", 8000))
    # Para producción, es recomendable desactivar reload=True, pero lo dejamos si es genérico.
    uvicorn.run("main:app", host="0.0.0.0", port=port)

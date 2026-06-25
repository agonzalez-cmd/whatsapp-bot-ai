import os
import PyPDF2

KNOWLEDGE_DIR = "base_conocimiento"

def ensure_knowledge_dir():
    if not os.path.exists(KNOWLEDGE_DIR):
        os.makedirs(KNOWLEDGE_DIR)

def read_knowledge_base() -> str:
    """
    Escanea la carpeta 'base_conocimiento' y extrae el texto de archivos .txt y .pdf.
    Retorna todo el texto concatenado.
    """
    ensure_knowledge_dir()
    
    knowledge_text = []
    
    for filename in os.listdir(KNOWLEDGE_DIR):
        filepath = os.path.join(KNOWLEDGE_DIR, filename)
        
        if filename.lower().endswith('.txt'):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    knowledge_text.append(f"--- Documento: {filename} ---\n{content}\n")
            except Exception as e:
                print(f"Error leyendo txt {filename}: {e}")
                
        elif filename.lower().endswith('.pdf'):
            try:
                with open(filepath, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    pdf_text = ""
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            pdf_text += extracted + "\n"
                    knowledge_text.append(f"--- Documento: {filename} ---\n{pdf_text}\n")
            except Exception as e:
                print(f"Error leyendo pdf {filename}: {e}")
                
    if not knowledge_text:
        return "No hay información en la base de conocimiento local."
        
    return "\n".join(knowledge_text)

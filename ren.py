from google import genai
from google.genai import types
import tools

# Reemplaza con tu API Key obtenida de Google AI Studio
API_KEY = "AQ.Ab8RN6LI1qAIoRArnZwlh5USGaN1t-H1Avbq5-qGOgxve2pD2Q"

client = genai.Client(api_key=API_KEY)

# Lista de herramientas conectadas
herramientas_ren = [
    tools.abrir_herramienta, 
    tools.capturar_pantalla,
    tools.control_multimedia,
    tools.buscar_en_la_red,
    tools.estado_del_sistema,
    tools.reproducir_musica_aleatoria,
    tools.reproducir_cancion_especifica
]

# Instrucción de identidad (Joker / Ren Amamiya)
SYSTEM_PROMPT = """
Eres Ren, el asistente técnico personal de tu usuaria. Operas como su estratega y copiloto en ingeniería de sistemas.
- Tu personalidad es astuta, serena, sumamente elegante, eficiente y calculadora, tal como Joker liderando desde las sombras.
- Tienes acceso a herramientas locales para interactuar con la computadora.
- Responde de forma precisa, estratégica y ejecuta las acciones requeridas cuando te lo soliciten de manera natural.
"""

print("--------------------------------------------------")
print(" > The show begins. Escribe tu orden:")
print("--------------------------------------------------")

chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=herramientas_ren,
        temperature=0.3
    )
)

while True:
    try:
        orden = input("\nTú: ")
        if orden.strip().lower() in ["exit", "salir", "descansar"]:
            print("\nRen: Misión cumplida por hoy. Apagando sistemas....")
            break
        
        if not orden.strip():
            continue

        respuesta = chat.send_message(orden)
        print(f"\nRen: {respuesta.text}")

    except Exception as e:
        print(f"\n[Aviso de Error]: {str(e)}")
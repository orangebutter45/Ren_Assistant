import os
import re
import io
import time
import socket
import subprocess
import pyautogui
import tools
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Configuración de entorno y aislamiento en Disco D:
load_dotenv()
os.environ["HF_HOME"] = "D:/AI_Models/huggingface"
os.environ["TORCH_HOME"] = "D:/AI_Models/torch"

def asegurar_omniroute():
    """Verifica si el puerto local 20128 responde; si no, lanza OmniRoute desde D:\\Proyectos\\OmniRoute."""
    puerto = 20128
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        if s.connect_ex(('127.0.0.1', puerto)) == 0:
            return

    print("[Sistema]: OmniRoute inactivo. Levantando servidor en segundo plano desde D:\\Proyectos\\OmniRoute...")
    try:
        ruta_omniroute = r"D:\Proyectos\OmniRoute"
        subprocess.Popen(f'start /min cmd.exe /k "cd /d {ruta_omniroute} && omniroute"', shell=True)
        
        for _ in range(15):
            time.sleep(0.5)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex(('127.0.0.1', puerto)) == 0:
                    print("[Sistema]: OmniRoute sincronizado y en línea.")
                    return
        print("[Aviso]: El servidor OmniRoute tardó en responder.")
    except Exception as e:
        print(f"[Aviso]: No se pudo auto-iniciar OmniRoute: {str(e)}")

# Asegurar proxy local
asegurar_omniroute()

OMNI_API_KEY = os.getenv("OMNIROUTE_API_KEY", "sk-17fab00283a5519b-86bfab-3b53b5a3")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", OMNI_API_KEY)

# Cliente para Chat / Herramientas (a través de OmniRoute)
client_chat = genai.Client(
    api_key=OMNI_API_KEY,
    http_options=types.HttpOptions(
        base_url="http://localhost:20128"
    )
)

# Cliente directo a Google AI Studio para procesamiento nativo de imágenes
client_vision = genai.Client(
    api_key=GEMINI_KEY
)

herramientas_ren = [
    tools.abrir_herramienta, 
    tools.control_multimedia,
    tools.buscar_en_la_red,
    tools.estado_del_sistema,
    tools.reproducir_cancion_especifica
]

MAPA_HERRAMIENTAS = {func.__name__: func for func in herramientas_ren}

SYSTEM_PROMPT = """
Eres Ren, el asistente técnico personal de tu usuaria. Operas como su estratega y copiloto en ingeniería de sistemas.
- Tu personalidad es astuta, serena, sumamente elegante, eficiente y calculadora, tal como Joker liderando desde las sombras.
- Tienes acceso a herramientas locales y a visión táctica para ver su pantalla.
- Cuando analices imágenes o pantallas con errores de código, sé analítico, directo y dale la solución exacta.
"""

print("--------------------------------------------------")
print(" > The show begins. Presiona Enter para hablar por micrófono o escribe tu orden:")
print("--------------------------------------------------")

try:
    chat = client_chat.chats.create(
        model="ren-auto",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=herramientas_ren,
            temperature=0.2
        )
    )
except Exception as e:
    print(f"[Error de Inicialización]: {str(e)}")
    chat = None

def analizar_pantalla_tactica(pregunta_usuario: str):
    """Captura la pantalla actual y la envía directamente al modelo de visión de Gemini."""
    print("\n[Visión Táctica]: Escaneando pantalla actual...")
    
    try:
        time.sleep(0.3)
        screenshot = pyautogui.screenshot()
        
        # Guardar en memoria RAM sin archivos temporales
        buffer_img = io.BytesIO()
        screenshot.save(buffer_img, format="PNG")
        bytes_imagen = buffer_img.getvalue()

        parte_imagen = types.Part.from_bytes(
            data=bytes_imagen,
            mime_type="image/png"
        )

        prompt_analisis = f"""
        Actúa como Ren (Joker), estratega e ingeniero de sistemas.
        Observa minuciosamente la captura adjunta de la pantalla de tu usuaria.
        Su duda u orden es: '{pregunta_usuario if pregunta_usuario else 'Analiza el código o error visible en pantalla'}'.
        Lee el texto del código, la terminal o las ventanas visibles en la imagen, detecta cualquier error de sintaxis, traza o fallo y dale la solución técnica exacta y concisa.
        """

        # Versión directa solicitada por la API
        respuesta = client_vision.models.generate_content(
            model="gemini-3.6-flash",
            contents=[parte_imagen, prompt_analisis],
            config=types.GenerateContentConfig(
                temperature=0.2
            )
        )
        
        texto_salida = respuesta.text or ""
        print(f"\nRen [Análisis Visual]:\n{texto_salida}")
        tools.decir("Análisis táctico completado. He colocado el diagnóstico en la terminal.")
    except Exception as e:
        print(f"[Error de Visión]: {str(e)}")

while True:
    try:
        entrada_teclado = input("\nTú [Enter para Micrófono]: ").strip()
        
        if entrada_teclado:
            orden = entrada_teclado
        else:
            orden = tools.escuchar_microfono()
            if not orden:
                continue

        if orden.strip().lower() in ["exit", "salir", "descansar"]:
            mensaje_despedida = "Misión cumplida por hoy. Apagando sistemas..."
            print(f"\nRen: {mensaje_despedida}")
            tools.decir(mensaje_despedida)
            break

        # Limpiar prefijos
        orden_normalizada = re.sub(r'^(ren|oye ren|por favor|hey ren)[,\s]*', '', orden, flags=re.IGNORECASE).strip()
        orden_low = orden_normalizada.lower()

        # 1. Visión Táctica
        if any(p in orden_low for p in ["pantalla", "analiza mi", "qué ves", "que ves", "revisa mi código", "revisa el código", "mira este error", "mira el código", "qué hay aquí", "escanea"]):
            analizar_pantalla_tactica(orden)
            continue

        # 2. Reproducción de canciones
        elif any(verbo in orden_low for verbo in ["reproduce", "pon la cancion", "pon la canción", "busca la canción", "escuchar", "toca", "ponte"]):
            cancion_limpia = re.sub(r'^(reproduce|pon la cancion|pon la canción|pon|escuchar|toca|ponte)\s+', '', orden_normalizada, flags=re.IGNORECASE).strip()
            if cancion_limpia and not any(p in cancion_limpia.lower() for p in ["música aleatoria", "musica"]):
                tools.reproducir_cancion_especifica(cancion_limpia)

        # 3. Control Multimedia / Volumen
        elif any(p in orden_low for p in ["pausa", "detén", "reanuda", "continua"]):
            tools.control_multimedia("pausar")
        elif any(p in orden_low for p in ["sube el volumen", "subir volumen", "sube volumen", "alto"]):
            tools.control_multimedia("subir")
        elif any(p in orden_low for p in ["baja el volumen", "bajar volumen", "baja volumen", "bajo"]):
            tools.control_multimedia("bajar")
        elif any(p in orden_low for p in ["silencio", "mute", "silenciar"]):
            tools.control_multimedia("silenciar")
        elif any(p in orden_low for p in ["musica", "música"]):
            tools.control_multimedia("pausar")

        # 4. Lanzador de Aplicaciones
        elif any(v in orden_low for v in ["abre", "abrir", "inicia", "ejecuta", "lanzar"]):
            if "apple" in orden_low or "itunes" in orden_low:
                tools.abrir_herramienta("apple music")
            elif "bloc" in orden_low or "notepad" in orden_low or "notas" in orden_low:
                tools.abrir_herramienta("notepad")
            elif "chrome" in orden_low or "navegador" in orden_low:
                tools.abrir_herramienta("chrome")
            elif "vs" in orden_low or "code" in orden_low:
                tools.abrir_herramienta("code")

        # 5. Telemetría del Hardware
        elif any(p in orden_low for p in ["sistema", "ram", "cpu", "bateria", "batería", "telemetria", "rendimiento"]):
            reporte = tools.estado_del_sistema()
            print(f"\n[Telemetría]:\n{reporte}")

        # 6. Búsqueda Web
        elif any(p in orden_low for p in ["busca en la red", "busca en google", "investiga sobre"]):
            consulta = re.sub(r'^(busca en la red|busca en google|investiga sobre)\s+', '', orden_normalizada, flags=re.IGNORECASE).strip()
            tools.buscar_en_la_red(consulta)

        # 7. Conversación regular y herramientas en OmniRoute
        elif chat:
            try:
                respuesta = chat.send_message(orden)

                if respuesta.function_calls:
                    for llamada in respuesta.function_calls:
                        nombre_funcion = llamada.name
                        argumentos = llamada.args or {}
                        if nombre_funcion in MAPA_HERRAMIENTAS:
                            resultado = MAPA_HERRAMIENTAS[nombre_funcion](**argumentos)
                            resp_tool = chat.send_message(
                                types.Part.from_function_response(
                                    name=nombre_funcion,
                                    response={"result": resultado}
                                )
                            )
                            texto_salida = resp_tool.text or ""
                            print(f"\nRen: {texto_salida}")
                            tools.decir(texto_salida)
                else:
                    texto_salida = respuesta.text or ""
                    if texto_salida:
                        print(f"\nRen: {texto_salida}")
                        tools.decir(texto_salida)
            except Exception as e:
                print(f"\n[Aviso IA]: {str(e)}")

    except Exception as e:
        print(f"\n[Aviso de Error]: {str(e)}")
import os
import subprocess
import webbrowser
import psutil
import pyautogui
import pywhatkit
import speech_recognition as sr
import pyttsx3

# Inicializar motor de voz local básico (fallback)
motor_voz = None
try:
    motor_voz = pyttsx3.init()
    motor_voz.setProperty("rate", 165)
except Exception:
    pass

def decir(texto: str):
    """Emite voz mediante el motor local actual."""
    if not texto:
        return
    try:
        if motor_voz:
            motor_voz.say(texto)
            motor_voz.runAndWait()
    except Exception as e:
        print(f"[Error de Voz]: {str(e)}")

def escuchar_microfono() -> str:
    """Captura audio desde el micrófono del equipo y lo convierte a texto."""
    reconocedor = sr.Recognizer()
    with sr.Microphone() as fuente:
        print("\n[Escuchando...] Habla ahora:")
        reconocedor.adjust_for_ambient_noise(fuente, duration=0.6)
        try:
            audio = reconocedor.listen(fuente, timeout=5, phrase_time_limit=8)
            texto = reconocedor.recognize_google(audio, language="es-ES")
            print(f"Tú (Voz): {texto}")
            return texto
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            print("[Sistema]: No se detectó audio claro.")
            return ""
        except Exception as e:
            print(f"[Error Micrófono]: {str(e)}")
            return ""

def abrir_herramienta(nombre_app: str) -> str:
    """Abre aplicaciones comunes en Windows."""
    nombre_app = nombre_app.lower()
    try:
        if "chrome" in nombre_app:
            subprocess.Popen("start chrome", shell=True)
            return "Google Chrome abierto."
        elif "notepad" in nombre_app or "bloc" in nombre_app:
            subprocess.Popen("notepad.exe")
            return "Bloc de notas abierto."
        elif "code" in nombre_app or "vs" in nombre_app:
            subprocess.Popen("code", shell=True)
            return "Visual Studio Code abierto."
        elif "apple" in nombre_app:
            subprocess.Popen("start itunes:", shell=True)
            return "Apple Music / iTunes solicitado."
        else:
            subprocess.Popen(f"start {nombre_app}", shell=True)
            return f"Ejecutando {nombre_app}."
    except Exception as e:
        return f"Error al abrir {nombre_app}: {str(e)}"

def control_multimedia(accion: str) -> str:
    """Controla la reproducción de música y el volumen general del sistema."""
    accion = accion.lower()
    try:
        if "pausar" in accion or "play" in accion:
            pyautogui.press("playpause")
            return "Reproducción alternada."
        elif "subir" in accion:
            for _ in range(5):
                pyautogui.press("volumeup")
            return "Volumen aumentado."
        elif "bajar" in accion:
            for _ in range(5):
                pyautogui.press("volumedown")
            return "Volumen reducido."
        elif "silenciar" in accion:
            pyautogui.press("volumemute")
            return "Audio silenciado."
        return "Comando multimedia no reconocido."
    except Exception as e:
        return f"Error en control multimedia: {str(e)}"

def reproducir_cancion_especifica(cancion: str) -> str:
    """Busca y reproduce una pista en YouTube."""
    try:
        pywhatkit.playonyt(cancion)
        return f"Reproduciendo {cancion} en YouTube."
    except Exception as e:
        return f"Error al reproducir: {str(e)}"

def buscar_en_la_red(consulta: str) -> str:
    """Abre una búsqueda en el navegador predeterminado."""
    try:
        url = f"https://www.google.com/search?q={consulta}"
        webbrowser.open(url)
        return f"Buscando '{consulta}' en la web."
    except Exception as e:
        return f"Error en búsqueda: {str(e)}"

def estado_del_sistema() -> str:
    """Reporta telemetría de hardware (CPU, RAM y Batería)."""
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        bateria = psutil.sensors_battery()
        
        estado_bat = "Sin batería detectada (PC de escritorio/CA)"
        if bateria:
            estado_bat = f"{bateria.percent}% {'(Cargando)' if bateria.power_plugged else '(Descargando)'}"
            
        return (
            f"CPU: {cpu}%\n"
            f"RAM: {ram.percent}% ({ram.used // (1024**2)} MB / {ram.total // (1024**2)} MB)\n"
            f"Batería: {estado_bat}"
        )
    except Exception as e:
        return f"Error de telemetría: {str(e)}"
    
import os
import subprocess
import webbrowser
import psutil
import pyautogui
import random
import urllib.parse

def abrir_herramienta(nombre: str) -> str:
    """Abre aplicaciones y herramientas locales en la computadora como Apple Music, Chrome, Bloc de notas, etc."""
    nombre_lower = nombre.lower()
    try:
        if "apple" in nombre_lower or "música" in nombre_lower or "musica" in nombre_lower:
            try:
                subprocess.Popen(["cmd", "/c", "start", "AppleMusic.exe"])
            except Exception:
                subprocess.Popen(["cmd", "/c", "start", "https://music.apple.com"])
            return "Frecuencia musical sincronizada. Apple Music en ejecución."
        elif "chrome" in nombre_lower or "navegador" in nombre_lower:
            subprocess.Popen("start chrome", shell=True)
            return "Navegador Chrome desplegado en pantalla."
        elif "notepad" in nombre_lower or "notas" in nombre_lower:
            subprocess.Popen("notepad")
            return "Bloc de notas abierto para apuntes rápidos."
        elif "code" in nombre_lower or "vs" in nombre_lower:
            subprocess.Popen("code", shell=True)
            return "Entorno de desarrollo Visual Studio Code listo."
        else:
            subprocess.Popen(f"start {nombre}", shell=True)
            return f"Ejecutando comando del sistema para {nombre}..."
    except Exception as e:
        return f"Interferencia al abrir la herramienta: {str(e)}"

def capturar_pantalla() -> str:
    """Toma una captura de la pantalla táctica y la guarda en el Escritorio."""
    try:
        ruta = os.path.join(os.path.expanduser("~"), "Desktop", "phantom_scan.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(ruta)
        return f"Reconocimiento visual completado. Captura guardada en: {ruta}"
    except Exception as e:
        return f"Falla en el escaneo de pantalla: {str(e)}"

def control_multimedia(accion: str) -> str:
    """Controla la reproducción multimedia y volumen del sistema (pausar, reproducir, subir_volumen, bajar_volumen, silenciar)."""
    accion_lower = accion.lower()
    try:
        if "pausar" in accion_lower or "play" in accion_lower or "reproducir" in accion_lower or "reanudar" in accion_lower:
            pyautogui.press("playpause")
            return "Comando multimedia enviado: Reproducir/Pausar."
        elif "subir" in accion_lower:
            for _ in range(5):
                pyautogui.press("volumeup")
            return "Nivel de audio incrementado."
        elif "bajar" in accion_lower:
            for _ in range(5):
                pyautogui.press("volumedown")
            return "Nivel de audio reducido."
        elif "silenciar" in accion_lower or "mute" in accion_lower:
            pyautogui.press("volumemute")
            return "Audio silenciado."
        else:
            return "Acción multimedia no reconocida."
    except Exception as e:
        return f"Error en el control de medios: {str(e)}"

def buscar_en_la_red(consulta: str) -> str:
    """Abre el navegador y realiza una búsqueda directa sobre el tema solicitado."""
    try:
        url = f"https://www.google.com/search?q={consulta.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Búsqueda desplegada en la red sobre: '{consulta}'."
    except Exception as e:
        return f"Error al acceder a la red: {str(e)}"

def estado_del_sistema() -> str:
    """Realiza un diagnóstico de telemetría de hardware: uso de CPU, memoria RAM y estado de batería."""
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        bateria = psutil.sensors_battery()
        
        info_bateria = f"{bateria.percent}% {'(Cargando)' if bateria.power_plugged else '(Batería)'}" if bateria else "Sin sensor de batería detectado"
        
        return (
            f"Diagnóstico de hardware completado:\n"
            f"- Carga de CPU: {cpu}%\n"
            f"- Memoria RAM en uso: {ram.percent}% ({round(ram.used / (1024**3), 1)} GB / {round(ram.total / (1024**3), 1)} GB)\n"
            f"- Estado de energía: {info_bateria}"
        )
    except Exception as e:
        return f"Falla en el diagnóstico del sistema: {str(e)}"


def reproducir_musica_aleatoria() -> str:
    """Inicia la reproducción o activa el modo aleatorio de música en el reproductor."""
    try:
        # Envía la pulsación multimedia Play/Pause y cambia de pista
        pyautogui.press("playpause")
        return "Iniciando reproducción musical aleatoria."
    except Exception as e:
        return f"Interferencia al reproducir música: {str(e)}"

def reproducir_cancion_especifica(cancion: str, artista: str = "") -> str:
    """Busca y reproduce una canción o artista específico en Apple Music / Web Player."""
    try:
        busqueda = f"{cancion} {artista}".strip()
        query_encoded = urllib.parse.quote(busqueda)
        # Abre la búsqueda directa en el ecosistema de Apple Music
        url_apple = f"https://music.apple.com/search?term={query_encoded}"
        webbrowser.open(url_apple)
        return f"Pista localizada: '{cancion}' {f'de {artista}' if artista else ''}. Desplegando en el reproductor."
    except Exception as e:
        return f"Falla al localizar la pista: {str(e)}"
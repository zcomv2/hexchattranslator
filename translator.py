import hexchat
import requests
import time

__module_name__ = "HexChat Translator"
__module_version__ = "15.1"
__module_description__ = "Traduce en tiempo real del español al inglés y japonés en cualquier canal"

# API de Google Translate
GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"

# Cooldown para evitar spam
last_message_time = 0

def on_message(word, word_eol, userdata):
    """Captura los mensajes y traduce directamente SIN funciones externas."""
    global last_message_time

    try:
        current_time = time.time()
    except Exception as e:
        hexchat.prnt(f"🔥 ERROR en time.time(): {e}")
        return hexchat.EAT_NONE

    if current_time - last_message_time < 1.5:
        return hexchat.EAT_NONE

    if len(word) < 2 or not word[1]:
        return hexchat.EAT_NONE

    original_text = word_eol[1].strip()
    if not original_text:
        return hexchat.EAT_NONE

    if original_text.startswith("[EN]") or original_text.startswith("[JA]") or original_text.startswith("[ES]"):
        return hexchat.EAT_NONE

    channel = hexchat.get_info("channel")
    if not channel:
        return hexchat.EAT_NONE

    last_message_time = current_time

    # 🔥 Traducir dentro de la misma función para que HexChat no borre nada
    def translate(text, target_lang):
        params = {
            "client": "gtx",
            "sl": "es",
            "tl": target_lang,
            "dt": "t",
            "q": text
        }

        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(GOOGLE_TRANSLATE_URL, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json()[0][0][0]
            return "[Error en traducción]"
        except requests.RequestException:
            return "[Error en conexión]"

    translated_en = translate(original_text, "en")
    translated_ja = translate(original_text, "ja")

    # 🔥 CORRECCIÓN FINAL: Cerramos bien la condición del `if`
    if ("[Error" in translated_en) or ("[Error" in translated_ja) :
        hexchat.prnt("[HexChat Translator] Error en la traducción.")
        return hexchat.EAT_NONE

    hexchat.command(f"say [ES] {original_text}")
    hexchat.command(f"say [EN] {translated_en}")
    hexchat.command(f"say [JA] {translated_ja}")

    return hexchat.EAT_ALL

# Hook para capturar los mensajes escritos
hexchat.hook_command("say", on_message)

hexchat.prnt(f"{__module_name__} v{__module_version__} cargado correctamente. Usando Google Translate.")
hexchat.prnt("🔥 DEBUG: Script iniciado sin errores. Listo para traducir.")

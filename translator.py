import hexchat
import requests
import time

__module_name__ = "HexChat Translator"
__module_version__ = "18.4"
__module_description__ = "Translates messages in real-time in HexChat into multiple languages."

# API for Google Translate
GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"

# Cooldown to prevent spam
last_message_time = 0

LANGUAGES_FULL = {
    "en": "English",
    "ja": "Japanese",
    "ru": "Russian",
    "zh-CN": "Chinese",
    "fr": "French"
}

LANGUAGES_SAY = {"en": "English", "ja": "Japanese"}  # Only English and Japanese for /say

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
        return "[Translation Error]"
    except requests.RequestException:
        return "[Connection Error]"

def on_message(word, word_eol, userdata):
    """Captures messages and translates them directly for /say."""
    global last_message_time

    try:
        current_time = time.time()
    except Exception as e:
        hexchat.prnt(f"🔥 ERROR in time.time(): {e}")
        return hexchat.EAT_NONE

    if current_time - last_message_time < 1.5:
        return hexchat.EAT_NONE

    if len(word) < 2 or not word[1]:
        return hexchat.EAT_NONE

    original_text = word_eol[1].strip()
    if not original_text:
        return hexchat.EAT_NONE

    if any(original_text.startswith(f"[{lang.upper()}]") for lang in LANGUAGES_SAY.keys()):
        return hexchat.EAT_NONE

    channel = hexchat.get_info("channel")
    if not channel:
        return hexchat.EAT_NONE

    last_message_time = current_time

    translations = {lang: translate(original_text, lang) for lang in LANGUAGES_SAY.keys()}

    if any("[Error" in t for t in translations.values()):
        hexchat.prnt("[HexChat Translator] Translation error.")
        return hexchat.EAT_NONE

    hexchat.command(f"say [ES] {original_text}")
    for lang, text in translations.items():
        hexchat.command(f"say [{lang.upper()}] {text}")

    return hexchat.EAT_ALL

def on_trans_command(word, word_eol, userdata):
    """Handles /trans command for manual translation into all languages."""
    if len(word) < 2:
        hexchat.prnt("Usage: /trans <message>")
        return hexchat.EAT_ALL

    original_text = word_eol[1].strip()
    translations = {lang: translate(original_text, lang) for lang in LANGUAGES_FULL.keys()}

    hexchat.command(f"say [ES] {original_text}")
    for lang, text in translations.items():
        hexchat.command(f"say [{lang.upper()}] {text}")

    return hexchat.EAT_ALL

# Hook to capture written messages
hexchat.hook_command("say", on_message)
hexchat.hook_command("trans", on_trans_command)

hexchat.prnt(f"{__module_name__} v{__module_version__} loaded successfully. Using Google Translate.")
hexchat.prnt("🔥 DEBUG: Script started without errors. Ready to translate.")

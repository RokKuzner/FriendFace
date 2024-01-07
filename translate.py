from langdetect import detect
from googletrans import Translator

def detect_lang(text:str):
    detected_language = detect(text)

    return detected_language

def translate(text:str, from_lang:str, to_lang="en"):
    if from_lang == to_lang:
        return text

    translator = Translator()
    try:
        translation = translator.translate(text, src=from_lang, dest=to_lang)
    except:
        return {"status": "error"}

    return translation.text
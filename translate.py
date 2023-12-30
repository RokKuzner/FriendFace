from langdetect import detect
from googletrans import Translator

def detect_lang(text:str):
    detected_language = detect(text)

    return detected_language

def translate(text:str, from_lang="auto", to_lang="en"):
    if from_lang == "auto":
        from_lang = detect_lang(text)

    if from_lang == to_lang:
        return text

    translator = Translator()
    translation = translator.translate(text, src=from_lang, dest=to_lang)

    return translation.text
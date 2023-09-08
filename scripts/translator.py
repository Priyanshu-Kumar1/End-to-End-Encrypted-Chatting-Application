from googletrans import Translator

translator = Translator()

def translate_text(text):
    return translator.translate(text, dest='hi').text
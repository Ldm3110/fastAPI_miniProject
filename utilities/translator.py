import requests

URL_DETECT = "https://translate.argosopentech.com/detect"
URL_TRANSLATE = "https://translate.argosopentech.com/translate"


def detect_language(comment):
    data = {
        "q": comment
    }
    response = requests.post(URL_DETECT, data=data)
    response_json = response.json()
    try:
        lang = response_json[0]["language"]
        return lang
    except KeyError:
        return None


def translate(comment, lang):
    if lang == 'en':
        data = {
            "q": comment,
            "source": lang,
            "target": "fr"
        }
        response = requests.post(
            URL_TRANSLATE,
            data=data,
        )
        response_json = response.json()
        return response_json["translatedText"]
    elif lang == 'fr':
        data = {
            "q": comment,
            "source": lang,
            "target": "en"
        }
        response = requests.post(
            URL_TRANSLATE,
            data=data
        )
        response_json = response.json()
        return response_json["translatedText"]


def return_good_text(first_text, second_text, lang):
    """
    return the good text in FR and in EN
    :param first_text: the initial comment
    :param second_text: the translated comment
    :param lang: the lang of the initial comment
    :return: good textFr and textEn
    """
    if lang == "en":
        text_en = first_text
        text_fr = second_text
        return text_en, text_fr
    elif lang == "fr":
        text_en = second_text
        text_fr = first_text
        return text_en, text_fr

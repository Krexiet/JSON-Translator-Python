import json
import requests

def translate_text(text, target_lang='fr', source_lang='en'):
    url = 'https://api.mymemory.translated.net/get'

    params = {
        'q': text,
        'langpair': f'{source_lang}|{target_lang}',
        'de': f'sahsa0960909@gmail.com'
    }

    response = requests.get(url, params=params)
    translated_text = response.json()['responseData']['translatedText']
    return translated_text

def translate_json(json_data, target_language='en', exclude_strings=None, source_language='en'):
    if exclude_strings is None:
        exclude_strings = []

    translated_data = {}

    for key, value in json_data.items():
        if any(exc_str in value for exc_str in exclude_strings):
            translated_data[key] = value
        elif isinstance(value, str):
            translated_text = translate_text(value, target_language, source_language)
            translated_data[key] = translated_text
        elif isinstance(value, dict):
            translated_data[key] = translate_json(value, target_language, exclude_strings, source_language)
        else:
            translated_data[key] = value

    return translated_data

def translate_json_file(input_file, output_file, target_language='fr', exclude_strings=None, source_language='en'):
    if exclude_strings is None:
        exclude_strings = []

    with open(input_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    translated_data = translate_json(json_data, target_language, exclude_strings, source_language)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, indent=4, ensure_ascii=False)

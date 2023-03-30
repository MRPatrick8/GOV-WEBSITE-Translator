import requests
import json
import string
import pandas as pd

class GoogleTranslate:
    api_url = 'https://translate.googleapis.com/translate_a/single'
    client = '?client=gtx'
    dt = '&dt=t'

def translate_row(row, target_lang, source_lang):
    sl = f"&sl={source_lang}"
    tl = f"&tl={target_lang}"
    
    # Remove punctuation marks from the input text
    translator = str.maketrans('', '', string.punctuation)
    text = row['content'].translate(translator)
    
    r = requests.get(f"{GoogleTranslate.api_url}{GoogleTranslate.client}{GoogleTranslate.dt}{sl}{tl}&q={text}")
    if r.status_code == 200:
        response_data = json.loads(r.text)
        translated_text = response_data[0][0][0]
    else:
        translated_text = ""
    row['translated_text'] = translated_text
    return row

def translate_dataframe(df, target_lang, source_lang):
    df_translated = df.apply(translate_row, axis=1, args=(target_lang, source_lang))
    return df_translated[['translated_text']]
### Back translation
def Back_translate_row(row, target_lang, source_lang):
    sl = f"&sl={source_lang}"
    tl = f"&tl={target_lang}"
    
    # Remove punctuation marks from the input text
    translator = str.maketrans('', '', string.punctuation)
    text = row['translated_text'].translate(translator)
    
    r = requests.get(f"{GoogleTranslate.api_url}{GoogleTranslate.client}{GoogleTranslate.dt}{sl}{tl}&q={text}")
    if r.status_code == 200:
        response_data = json.loads(r.text)
        translated_text = response_data[0][0][0]
    else:
        translated_text = ""
    row['back_translated_text'] = translated_text
    return row   
def back_translate_dataframe(df, target_lang, source_lang):
    df_translated = df.apply(Back_translate_row, axis=1, args=(target_lang, source_lang))
    return df_translated[['back_translated_text']]

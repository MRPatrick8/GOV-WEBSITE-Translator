# import requests
# import json
# import string
# import pandas as pd
# import docx
# import re

# class GoogleTranslate:
#     api_url = 'https://translate.googleapis.com/translate_a/single'
#     client = '?client=gtx'
#     dt = '&dt=t'

# def translate_row(text, target_lang, source_lang):
#     sl = f"&sl={source_lang}"
#     tl = f"&tl={target_lang}"
    
#     r = requests.get(f"{GoogleTranslate.api_url}{GoogleTranslate.client}{GoogleTranslate.dt}{sl}{tl}&q={text}")
#     if r.status_code == 200:
#         response_data = json.loads(r.text)
#         translated_text = response_data[0][0][0]
#     else:
#         translated_text = ""
#     return translated_text

# def translate_paragraphs(input_paragraphs, target_lang, source_lang=None):
#     paragraphs = []
#     for paragraph in input_paragraphs:
#         trans_paragraph = translate_row(paragraph, target_lang, source_lang)
#         paragraphs.append(trans_paragraph)

#     return paragraphs

import requests
import json
import string
import pandas as pd
import docx
import re

class GoogleTranslate:
    api_url = 'https://translate.googleapis.com/translate_a/single'
    client = '?client=gtx'
    dt = '&dt=t'

def translate_row(text, target_lang, source_lang):
    sl = f"&sl={source_lang}"
    tl = f"&tl={target_lang}"
    
    r = requests.get(f"{GoogleTranslate.api_url}{GoogleTranslate.client}{GoogleTranslate.dt}{sl}{tl}&q={text}")
    if r.status_code == 200:
        response_data = json.loads(r.text)
        translated_text = response_data[0][0][0]
        accuracy = response_data[0][0][2]
    else:
        translated_text = ""
        accuracy = 0.0
    return translated_text, accuracy

def translate_paragraphs(input_paragraphs, target_lang, source_lang=None):
    paragraphs = []
    accuracies = []
    for paragraph in input_paragraphs:
        trans_paragraph, accuracy = translate_row(paragraph, target_lang, source_lang)
        paragraphs.append(trans_paragraph)
        accuracies.append(accuracy)

    # Find the lowest accuracy and highlight the corresponding paragraph
    min_accuracy = min(accuracies)
    for i, acc in enumerate(accuracies):
        if acc == min_accuracy:
            paragraphs[i] = f"*** {paragraphs[i]} ***"  # highlight the paragraph

    # Print the accuracies for each paragraph
    for i, (paragraph, accuracy) in enumerate(zip(paragraphs, accuracies)):
        print(f"Paragraph {i+1}: Accuracy = {accuracy:.2f}")
    
    return paragraphs


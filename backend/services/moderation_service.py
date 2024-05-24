""" module with analyzer by signatures and then use ai """
from utils import sec_analyzer  # ai here
from typing import List, Optional

import re

import pandas as pd
from difflib import SequenceMatcher

def process_message(message, dataset_path, 
                    threshold=0.25, min_count=3,  # dev
                    match_columns=['text', 'canonical_form_1', 
                                  'canonical_form_2', 'canonical_form_3']):
    """ load bad words from dataset and compare with message 
        on 25% and 3 count in message_ch """
    data = pd.read_csv(dataset_path)
    bad_words = data[match_columns].values.flatten().tolist()  # Flatten the list of lists

    message_ch = message.lower()
    matches_count = 0
    for bad_word in bad_words:
        similarity = SequenceMatcher(None, message_ch, str(bad_word)).ratio()
        if similarity >= threshold:
            matches_count += 1

    if matches_count >= min_count:
        return None
    else:
        return message

def clean_posts(posts: list) -> list:
    # TODO: write exceptions if file not found
    cleaned_posts = []
    for post in posts:
        cleaned_content = process_message(  # path on run main is from project root
            post['content'], './backend/services/profanity_en.csv') 
        if cleaned_content is not None:
            post['content'] = cleaned_content
            cleaned_posts.append(post)
    return cleaned_posts

def clean_post(post: dict) -> dict:
    # TODO: cleans post by signatures and AI
    return post

def clean_ct(category: str) -> str:
    # TODO: add en regex pattern
    pattern = r"(?iu)\b(([уyu]|[нзnz3][аa]|(хитро|не)?[вvwb][зz3]?[ыьъi]|[сsc][ьъ']|(и|[рpr][аa4])[зсzs]ъ?|([оo0][тбtb6]|[пp][оo0][дd9])[ьъ']?|(.\B)+?[оаеиeo])?-?([еёe][бb6](?!о[рй])|и[пб][ае][тц]).*?|([нn][иеаaie]|([дпdp]|[вv][еe3][рpr][тt])[оo0]|[рpr][аa][зсzc3]|[з3z]?[аa]|с(ме)?|[оo0]([тt]|дно)?|апч)?-?[хxh][уuy]([яйиеёюuie]|ли(?!ган)).*?|([вvw][зы3z]|(три|два|четыре)жды|(н|[сc][уuy][кk])[аa])?-?[бb6][лl]([яy](?!(х|ш[кн]|мб)[ауеыио]).*?|[еэe][дтdt][ь']?)|([рp][аa][сзc3z]|[знzn][аa]|[соsc]|[вv][ыi]?|[пp]([еe][рpr][еe]|[рrp][оиioеe]|[оo0][дd])|и[зс]ъ?|[аоao][тt])?[пpn][иеёieu][зz3][дd9].*?|([зz3][аa])?[пp][иеieu][дd][аоеaoe]?[рrp](ну.*?|[оаoa][мm]|([аa][сcs])?([иiu]([лl][иiu])?[нщктлtlsn]ь?)?|([оo](ч[еиei])?|[аa][сcs])?[кk]([оo]й)?|[юu][гg])[ауеыauyei]?|[мm][аa][нnh][дd]([ауеыayueiи]([лl]([иi][сзc3щ])?[ауеыauyei])?|[оo][йi]|[аоao][вvwb][оo](ш|sh)[ь']?([e]?[кk][ауеayue])?|юк(ов|[ауи])?)|[мm][уuy][дd6]([яyаиоaiuo0].*?|[еe]?[нhn]([ьюия'uiya]|ей))|мля([тд]ь)?|лять|([нз]а|по)х|м[ао]л[ао]фь([яию]|[её]й))\b"
    matches = re.findall(pattern, category)  # ret [('asd',''),]
    if len(matches) >= 3:  # works on words and phrases
        return "temp"
    else:
        return category


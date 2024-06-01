""" module with analyzer by signatures and then use ai """
from difflib import SequenceMatcher
import re

import pandas as pd
from better_profanity import profanity

from utils import sec_analyzer  # ai here
from utils import exceptions
# TODO: unit tests for this module

def process_message(message, dataset_path, threshold=0.25, min_count=3,  # dev
    match_columns=['text', 'canonical_form_1', 'canonical_form_2', 'canonical_form_3']):
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
        raise exceptions.InvalidInputException(detail="Bad word detected more than min_count")
    return message

def clean_posts(posts: list) -> list:
    """ cleans posts on out list by static analyzer """
    cleaned_posts = []
    for post in posts:
        cleaned_content = process_message(post['content'],  # path on run main is from project root
        './backend/services/profanity_en.csv') 
        if cleaned_content is not None:
            post['content'] = cleaned_content
            cleaned_posts.append(post)
    return cleaned_posts

def clean_post(post: dict) -> dict:
    """ cleans post on in dict by static analyzer and AI"""
    # TODO: cleans post AI
    cleaned_content = process_message(post['content'],  # path on run main is from project root
        './backend/services/profanity_en.csv') 
    pipe = sec_analyzer.get_model('profanity')
    cleaned_ai_content = sec_analyzer.check_count_by_model(
        cleaned_content, pipe, 'abusive text')
    if cleaned_ai_content is not None:
        post['content'] = cleaned_content
    pr_count = 0
    for word in post['title'].split():
        if profanity.contains_profanity(word):
            pr_count += 1
    if pr_count > 3:
        raise exceptions.InvalidInputException(detail="Profanity detected more than 3")
    return post

def clean_ct(category: str) -> str:
    """ cleans category by static analyzer on regex """
    pattern_ru = r"(?iu)\b(([уyu]|[нзnz3][аa]|(хитро|не)?[вvwb][зz3]?[ыьъi]|[сsc][ьъ']|(и|[рpr][аa4])[зсzs]ъ?|([оo0][тбtb6]|[пp][оo0][дd9])[ьъ']?|(.\B)+?[оаеиeo])?-?([еёe][бb6](?!о[рй])|и[пб][ае][тц]).*?|([нn][иеаaie]|([дпdp]|[вv][еe3][рpr][тt])[оo0]|[рpr][аa][зсzc3]|[з3z]?[аa]|с(ме)?|[оo0]([тt]|дно)?|апч)?-?[хxh][уuy]([яйиеёюuie]|ли(?!ган)).*?|([вvw][зы3z]|(три|два|четыре)жды|(н|[сc][уuy][кk])[аa])?-?[бb6][лl]([яy](?!(х|ш[кн]|мб)[ауеыио]).*?|[еэe][дтdt][ь']?)|([рp][аa][сзc3z]|[знzn][аa]|[соsc]|[вv][ыi]?|[пp]([еe][рpr][еe]|[рrp][оиioеe]|[оo0][дd])|и[зс]ъ?|[аоao][тt])?[пpn][иеёieu][зz3][дd9].*?|([зz3][аa])?[пp][иеieu][дd][аоеaoe]?[рrp](ну.*?|[оаoa][мm]|([аa][сcs])?([иiu]([лl][иiu])?[нщктлtlsn]ь?)?|([оo](ч[еиei])?|[аa][сcs])?[кk]([оo]й)?|[юu][гg])[ауеыauyei]?|[мm][аa][нnh][дd]([ауеыayueiи]([лl]([иi][сзc3щ])?[ауеыauyei])?|[оo][йi]|[аоao][вvwb][оo](ш|sh)[ь']?([e]?[кk][ауеayue])?|юк(ов|[ауи])?)|[мm][уuy][дd6]([яyаиоaiuo0].*?|[еe]?[нhn]([ьюия'uiya]|ей))|мля([тд]ь)?|лять|([нз]а|по)х|м[ао]л[ао]фь([яию]|[её]й))\b"
    matches_ru = re.findall(pattern_ru, category)  # ret [('asd',''),]
    if len(matches_ru) >= 3 or profanity.contains_profanity(category):  # works on words and phrases
        raise InvalidInputException('Category is invalid')
    return category

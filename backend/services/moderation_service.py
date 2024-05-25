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
    # TODO: cleans post AI
    cleaned_content = process_message(  # path on run main is from project root
        post['content'], './backend/services/profanity_en.csv') 
    if cleaned_content is not None:
        post['content'] = cleaned_content
    else:
        post = None
    return post

def clean_ct(category: str) -> str:
    pattern_en = r"""
    nig[^(h|n|m)]n.{0,3}ggn(\.)\1{0,}ggf.{1}g(c|k)(u|v)\1{0,}nt(c|k)r.?\.?k.?rf(\.)\1{0,}(k|ck){1,2}d(i|1|y)\1{0,}(ck|k)(c|k)(0|o|u)\1{0,}cksh(i|1)\1{0,}tb(\.)\1{0,}st(\.)\1{0,}rdb(i|1)\1{0,}(t|7)\1{0,}chb(0|o)ll(0|o)(k|ck|x)b(0|o)ll(t|7)(i|1)\1{0,}(t|7)\1{0,}sch(i|1)\1{0,}n(c|k)cum(c|k)l(i|1)\1{0,}tch(0|o)(ad|de)d(i|1)ld(0|o)j(i|1)zk(i|1|y)\1{0,}k(e|3)n(e|3)\1{0,}gr(o|0)p(i|1)ssp(u|v)\1{0,}(s)\1{0,}(y|i)pr(i|1)(k|ck)sl(u|v)\1{0,}tsm(e|3)\1{0,}gsp(i|1)\1{0,}(c|k)t(a|4)\1{0,}rdw(a|4)\1{0,}nkwh(0|o)\1{0,}r(e|3)
    """
    pattern_ru = r"(?iu)\b(([уyu]|[нзnz3][аa]|(хитро|не)?[вvwb][зz3]?[ыьъi]|[сsc][ьъ']|(и|[рpr][аa4])[зсzs]ъ?|([оo0][тбtb6]|[пp][оo0][дd9])[ьъ']?|(.\B)+?[оаеиeo])?-?([еёe][бb6](?!о[рй])|и[пб][ае][тц]).*?|([нn][иеаaie]|([дпdp]|[вv][еe3][рpr][тt])[оo0]|[рpr][аa][зсzc3]|[з3z]?[аa]|с(ме)?|[оo0]([тt]|дно)?|апч)?-?[хxh][уuy]([яйиеёюuie]|ли(?!ган)).*?|([вvw][зы3z]|(три|два|четыре)жды|(н|[сc][уuy][кk])[аa])?-?[бb6][лl]([яy](?!(х|ш[кн]|мб)[ауеыио]).*?|[еэe][дтdt][ь']?)|([рp][аa][сзc3z]|[знzn][аa]|[соsc]|[вv][ыi]?|[пp]([еe][рpr][еe]|[рrp][оиioеe]|[оo0][дd])|и[зс]ъ?|[аоao][тt])?[пpn][иеёieu][зz3][дd9].*?|([зz3][аa])?[пp][иеieu][дd][аоеaoe]?[рrp](ну.*?|[оаoa][мm]|([аa][сcs])?([иiu]([лl][иiu])?[нщктлtlsn]ь?)?|([оo](ч[еиei])?|[аa][сcs])?[кk]([оo]й)?|[юu][гg])[ауеыauyei]?|[мm][аa][нnh][дd]([ауеыayueiи]([лl]([иi][сзc3щ])?[ауеыauyei])?|[оo][йi]|[аоao][вvwb][оo](ш|sh)[ь']?([e]?[кk][ауеayue])?|юк(ов|[ауи])?)|[мm][уuy][дd6]([яyаиоaiuo0].*?|[еe]?[нhn]([ьюия'uiya]|ей))|мля([тд]ь)?|лять|([нз]а|по)х|м[ао]л[ао]фь([яию]|[её]й))\b"
    matches_ru = re.findall(pattern_ru, category)  # ret [('asd',''),]
    if len(matches_ru) >= 3:  # works on words and phrases
        return "temp"
    else:
        return category


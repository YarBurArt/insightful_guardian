""" module with analyzer by signatures and then use ai """
import re
from os import name as os_name
import ctypes

import urllib.request, json
from urllib.error import HTTPError
from utils import exceptions

import pandas as pd
from better_profanity import profanity
from Levenshtein import ratio


# TODO: use c variant of process_message on windows, it's just static analyzer
# python basically it's C, then just use ctypes for best performance
if os_name == 'posix':
    # load bad words from dataset and compare with message on 25% and 3 count in message_ch
    # define function signature based on the modified C function, fix here
    process_message_c = ctypes.CDLL(
        "./backend/services/lib_profanity/statprofilter.so").process_message
    process_message_c.argtypes = [
        ctypes.c_char_p,  # message (char*)
        ctypes.c_float,  # threshold (float)
        ctypes.c_int,  # min_count (int)
    ]
    process_message_c.restype = ctypes.c_int  # return type (int)

    async def process_message(message: str, threshold: float=0.95, min_count: int=300) -> str:
        """ process message wrapper """
        result = process_message_c(
            ctypes.c_char_p(message.encode('utf-8')),
                ctypes.c_float(threshold), ctypes.c_int(min_count))
        if result >= min_count:
            raise exceptions.InvalidInputException(detail="Bad word detected more than min_count 1")
        return message

elif os_name == 'nt': # stable based on docker requirements
    # load bad words from dataset and compare with message on 25% and 3 count in message_ch 
    data = pd.read_csv('./backend/services/profanity_en.csv')
    match_columns = ['text', 'canonical_form_2', 'canonical_form_3']
    cached_bad_words = data[match_columns].values.flatten().tolist()
    cached_bad_words_s = list(map(str, cached_bad_words))

    async def process_message(message: str, threshold: float=0.95, min_count: int=300) -> str:
        """ process message via python levenshtein ratio """
        if cached_bad_words_s is None:
            raise exceptions.InvalidInputException(detail="Developers are working on this")
        matches_count = 0

        for bad_word in cached_bad_words_s:
            for word in message.split():
                if ratio(bad_word, word) >= threshold:
                    print(word, ratio(bad_word, word))
                    matches_count += 1

        if matches_count >= min_count:
            raise exceptions.InvalidInputException(detail="Bad word detected more than min_count 1")
        return message


def get_pr_ai_count(message: str) -> int:
    """ profanity check via LLM for disrespectful words """
    try:
        req = urllib.request.Request(
            'http://localhost:8005/check_profanity',  # dev, it can be run on docker
            json.dumps({'text': message}).encode('utf-8'),
            headers={'Content-Type': 'application/json'}, method='POST'
        )
        response = urllib.request.urlopen(req)
        resp_json = json.loads(response.read().decode('utf-8'))
        pr_ai_count = int(resp_json['result'])
    except HTTPError:
        print("Can't connect to LLM http service")
        pr_ai_count = 0
    return pr_ai_count


async def clean_posts(posts: list) -> list:
    """ cleans posts on out list by static analyzer """
    cleaned_posts = []
    for post in posts:
        cleaned_content = await process_message(post['content'])
        post['content'] = cleaned_content
        cleaned_posts.append(post)
    return cleaned_posts


async def clean_post(post: dict) -> dict:
    """ cleans post on in dict by static analyzer and AI"""
    cleaned_content = process_message(post['content'])
    pr_ai_count = get_pr_ai_count(cleaned_content)
    if pr_ai_count > 8:
        raise exceptions.InvalidInputException(detail="Profanity detected more than 8 (llm)")

    post['content'] = cleaned_content
    pr_count = 0
    for word in post['title'].split():
        if profanity.contains_profanity(word):
            pr_count += 1
    if pr_count > 3:
        raise exceptions.InvalidInputException(detail="Profanity detected more than 3")
    return post

async def clean_ct(category: str) -> str:
    """ cleans category by static analyzer on regex """
    pattern_ru = r"(?iu)\b(([уyu]|[нзnz3][аa]|(хитро|не)?[вvwb][зz3]?[ыьъi]|[сsc][ьъ']|(и|[рpr][аa4])[зсzs]ъ?|([оo0][тбtb6]|[пp][оo0][дd9])[ьъ']?|(.\B)+?[оаеиeo])?-?([еёe][бb6](?!о[рй])|и[пб][ае][тц]).*?|([нn][иеаaie]|([дпdp]|[вv][еe3][рpr][тt])[оo0]|[рpr][аa][зсzc3]|[з3z]?[аa]|с(ме)?|[оo0]([тt]|дно)?|апч)?-?[хxh][уuy]([яйиеёюuie]|ли(?!ган)).*?|([вvw][зы3z]|(три|два|четыре)жды|(н|[сc][уuy][кk])[аa])?-?[бb6][лl]([яy](?!(х|ш[кн]|мб)[ауеыио]).*?|[еэe][дтdt][ь']?)|([рp][аa][сзc3z]|[знzn][аa]|[соsc]|[вv][ыi]?|[пp]([еe][рpr][еe]|[рrp][оиioеe]|[оo0][дd])|и[зс]ъ?|[аоao][тt])?[пpn][иеёieu][зz3][дd9].*?|([зz3][аa])?[пp][иеieu][дd][аоеaoe]?[рrp](ну.*?|[оаoa][мm]|([аa][сcs])?([иiu]([лl][иiu])?[нщктлtlsn]ь?)?|([оo](ч[еиei])?|[аa][сcs])?[кk]([оo]й)?|[юu][гg])[ауеыauyei]?|[мm][аa][нnh][дd]([ауеыayueiи]([лl]([иi][сзc3щ])?[ауеыauyei])?|[оo][йi]|[аоao][вvwb][оo](ш|sh)[ь']?([e]?[кk][ауеayue])?|юк(ов|[ауи])?)|[мm][уuy][дd6]([яyаиоaiuo0].*?|[еe]?[нhn]([ьюия'uiya]|ей))|мля([тд]ь)?|лять|([нз]а|по)х|м[ао]л[ао]фь([яию]|[её]й))\b"
    matches_ru = re.findall(pattern_ru, category)  # ret [('asd',''),]
    if len(matches_ru) >= 3 or profanity.contains_profanity(category):  # works on words and phrases
        raise exceptions.InvalidInputException('Category is invalid')
    return category

""" module with analyzer by signatures and then use ai """
from utils import sec_analyzer  # ai here
from typing import List, Optional

import nltk
from nltk.corpus import stopwords

# load stop words from nltk
# nltk.download('stopwords')
# nltk.download('punkt')
stop_words_ru = set(stopwords.words('russian'))
stop_words_en = set(stopwords.words('english'))
# because some words if false we should ret error
aggressive_stop_words_threshold = 64 
# TODO: if sentence {} is stop words ret error
def process_message(message):
    # check if message contains only ascii chars
    if all(ord(char) < 128 for char in message):
        stop_words = stop_words_en
    else:
        stop_words = stop_words_ru
    # tokenize to get words list  
    tokens = nltk.word_tokenize(message.lower())
    stop_words_count = sum(1 for token in tokens if token in stop_words)
    # ret error if stop words count >= 64
    if stop_words_count >= aggressive_stop_words_threshold:
        return None
    else:
        return message

def clean_posts(posts: List[dict]) -> List[dict]:
    for post in posts:
        post['content'] = process_message(post['content'])
    return posts

def clean_post(post: dict) -> dict:
    # TODO: cleans post by signatures and AI
    return post

def clean_ct(category: str) -> dict:
    # TODO: clean category by signatures
    return category


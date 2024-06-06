import pytest 
from faker import Faker; fake = Faker()

from backend.services.moderation_service import (
    process_message, clean_post, clean_ct)

# TODO: real random data fuzz with profanity 
def fuzz_prmt_process_message():
    """ generate fuzz text/int prmt for process_message function """
    for message in  [fake.sentence() for _ in range(32)]:
        for threshold in range(0.0, 1.0, step=0.05):
            for min_count in range(50, 500, step=50):
                yield message, threshold, min_count

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
def fuzz_prmt_clean_post():
    """ generate fuzz text prmt for clean_post function """ 
    for title in  [fake.sentence() for _ in range(32)]:
        for content in [fake.text() for _ in range(32)]:
            yield {"title": title, "content": content}
            

def fuzz_prmt_clean_ct():
    """ generate fuzz text prmt for clean_ct function """ 
    for category in  [fake.word() for _ in range(32)]:
        yield category

@pytest.mark.parametrize("message,threshold,min_count", fuzz_prmt_process_message())
def test_process_message(message, threshold, min_count):
    """ test process_message function """
    assert process_message(message, threshold, min_count)


@pytest.mark.parametrize("title,content", fuzz_prmt_clean_post())
def test_clean_post(title, content):
    """ test clean_post function """
    assert clean_post({"title": title, "content": content})                


@pytest.mark.parametrize("category", fuzz_prmt_clean_ct())
def test_clean_ct(category):
    """ test clean_ct function """
    assert clean_ct(category)
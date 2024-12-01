""" module for testing post service """
import pytest
from faker import Faker; fake = Faker()

from backend.services.post_service import (
    get_posts_with_page, get_post_by_id_without_auth,
    get_posts_by_category_with_val, get_posts_by_text_with_val
)

def fuzz_prmt_get_posts_with_page():
    """ generate fuzz int prmt for get_posts_with_page function """
    yield from [(page, page_size) for page in range(1, 100)
                for page_size in range(1, 100)]

def fuzz_prmt_get_post_by_id():
    """ generate fuzz text prmt for get_post_by_id_without_auth function """ 
    yield from [fake.uuid4() for _ in range(32)]


def fuzz_prmt_get_posts_by_category_with_val():
    """ generate fuzz text prmt for get_posts_by_category_with_val function """ 
    yield from [fake.word() for _ in range(32)]

def fuzz_prmt_get_posts_by_text_with_val():
    """ generate fuzz text prmt for get_posts_by_text_with_val function """ 
    yield from [fake.sentence() for _ in range(32)]


@pytest.mark.parametrize("page,page_size", fuzz_prmt_get_posts_with_page())
def test_get_posts_with_page(page, page_size):
    """ test get_posts_with_page function """
    assert get_posts_with_page(page, page_size)


@pytest.mark.parametrize("post_id", fuzz_prmt_get_post_by_id())
def test_get_post_by_id_without_auth(post_id):
    """ test get_post_by_id_without_auth function """
    assert get_post_by_id_without_auth(post_id)


@pytest.mark.parametrize("category", fuzz_prmt_get_posts_by_category_with_val())
def test_get_posts_by_category_with_val(category):
    """ test get_posts_by_category_with_val function """
    assert get_posts_by_category_with_val(category)


@pytest.mark.parametrize("query", fuzz_prmt_get_posts_by_text_with_val())
def test_get_posts_by_text_with_val(query):
    """ test get_posts_by_text_with_val function """
    assert get_posts_by_text_with_val(query)


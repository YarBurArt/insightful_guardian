""" module with only analyzer by ai """
# TODO: add api to moderate agressive posts
from transformers import pipeline

# TODO: optimize model loading
# pipe = pipeline("text-classification", model="parsawar/Profanity2.1")
# res = pipe(["This restaurant is awesome", "This restaurant is awful"])
# print (res)

PROFANITY_PIPE = pipeline("text-classification", model="parsawar/Profanity2.1")
SENTIMENT_PIPE = pipeline("text-classification", model="sbcBI/sentiment_analysis")


def check_count_by_model(text: str, pipe, label: str):
    """ check text for profanity """
    if len(text) < 96:
        result = pipe([text])
        print(result)       
        if result[0]['label'] == label: #'abusive text':
            return None
        else:
            return text
    
    ab_count = 0
    parts_t = [text[i:i+96] for i in range(0, len(text), 96)]
    results = pipe(parts_t)
    print(results)
    abusive_count = sum(1 for result in results if result['label'] == 'abusive text')
    
    if abusive_count / len(parts) > 0.9:
        return None
    return text

def get_model(name: str):
    """ get model pipeline by name """
    if name == 'profanity':
        return PROFANITY_PIPE
    else:
        return SENTIMENT_PIPE

if __name__ == "__main__":
    check_count_by_model("This restaurant is awesom arse-bandits and so is this one. It is awesome", PROFANITY_PIPE, 'abusive text')
    check_count_by_model("This restaurant is awful arse-bandits", SENTIMENT_PIPE, 'NEGATIVE')



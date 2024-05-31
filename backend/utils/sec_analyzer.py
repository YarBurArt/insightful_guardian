""" module with only analyzer by ai """
# TODO: add api to moderate agressive posts
#
from transformers import pipeline

pipe = pipeline("text-classification", model="parsawar/Profanity2.1")
# res = pipe(["This restaurant is awesome", "This restaurant is awful"])
# print (res)

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
        return pipeline("text-classification", model="parsawar/Profanity2.1")
    else: # TODO: change model
        return pipeline('sentiment-analysis')

if __name__ == "__main__":
    pipe = pipeline("text-classification", model="parsawar/Profanity2.1")
    check_count_by_model("This restaurant is awesom arse-bandits and so is this one. It is awesome", pipe, 'abusive text')
    pipe = pipeline('sentiment-analysis')  # TODO: change model
    check_count_by_model("This restaurant is awful arse-bandits", pipe, 'NEGATIVE')



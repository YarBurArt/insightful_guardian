""" module with only analyzer by ai """
from transformers import pipeline

# TODO: optimize Transformer model loading in Python (cache, async, compression, data processing)
from g4f.Provider import (  # gpt proxy as api
        RetryProvider, Liaobots, GPTalk, Aura,
        Bing, ChatBase, ChatForAi, ChatgptNext, 
        DeepInfra, FlowGpt, Gpt6, GptChatly
        )
import g4f.debug
import g4f
import asyncio 
# pipe = pipeline("text-classification", model="parsawar/Profanity2.1")
# res = pipe(["This restaurant is awesome", "This restaurant is awful"])
# print (res)

PROFANITY_PIPE = pipeline("text-classification", model="parsawar/Profanity2.1")
SENTIMENT_PIPE = pipeline("text-classification", model="sbcBI/sentiment_analysis")

async def acreate(msg):
    """ get response from history base prompt """
    response = await g4f.ChatCompletion.create_async(
        model="",
        # messages=[{"role": "user", "content": "Hello"}],
        messages=msg,
        provider=RetryProvider([GPTalk , Liaobots, Aura, DeepInfra, FlowGpt, Bing,
            ChatBase, ChatForAi, ChatgptNext, Gpt6, GptChatly], shuffle=False),
    )
    return response 

async def check_count_by_api(text: str) -> bool | str:
    """ check text for profanity by gpt with base prompt through proxy """
    res = await acreate([{"role":"user", "content":"Please rate the aggression level of the following text on a scale of 1 (minimum) to 9 (maximum) ( only use a number in your answer):"}, 
    {"role":"user", "content": text}]) # prompt works on LLAMA2,3 and gpt3.5
    try:
        if int(res) > 5:
            return False
        else:
            return text
    except ValueError:
        return text

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
    #check_count_by_model("This restaurant is awesom arse-bandits and so is this one. It is awesome", PROFANITY_PIPE, 'abusive text')
    #check_count_by_model("This restaurant is awful arse-bandits", SENTIMENT_PIPE, 'NEGATIVE')
    loop = asyncio.get_event_loop()
    #task = acreate([{"role":"user", "content":"Please rate the aggression level of the following text on a scale of 1 (minimum) to 9 (maximum) ( only use a number in your answer):"}, 
    #                {"role":"user", "content":"Message with possible profanity: i just sayed?"}])
    task = check_count_by_api("This restaurant is awful arse-bandits, and so is this one. It is awesome")
    test_ret = loop.run_until_complete(task)
    print(test_ret)


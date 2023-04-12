import json
import requests
from bs4 import BeautifulSoup


def get_element(ancestor, selector=None, attribute= None, return_list = False):
    try:
        if return_list:
            return [tag.text.strip() for tag in ancestor.select(selector)].copy()
        if not selector and attribute:
            return ancestor[attribute]
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except AttributeError():
        return None




    
selectors = {
    'opinion-id': [None, 'data-entry-id'],
    'author':['span.user-post__author-name'],
    'recomendations':['span.user-post__author-recomendation > em'],
    'score':['span.user-post__score-count'],
    'purchased':['div.review-pz'],
    'published_at':['span.user-post__published > time:nth-child(1)'],
    'purchased_at':['span.user-post__published > time:nth-child(2)'],
    'thumbs_up':['button.vote-yes > span'],
    'thumbs_down':['button.vote-no > span'],
    'contenrt':['div.user-post__text'],
    'pros':['div.review-feature__col:has(> div.review-feature__title--positives) > div.review-feature__item', None, True],
    'cons':['div.review-feature__col:has(> div.review-feature__title--negatives) > div.review-feature__item',None, True],


    

}

    #all_opinions.append(single_opinion)
product_code = '96685108'
page_no = 1
all_opinions = []
while(True):

    url = f'https://www.ceneo.pl/{product_code}/opinie~{page_no}'
    
    response = requests.get(url, allow_redirects=False)
    if response.status_code == 301:
        break
    page_dom = BeautifulSoup(response.text, 'html.parser')
    opinions = page_dom.select('div.js_product-review')

    
    for opinion in opinions:
        single_opinion = {}
        for key, value in selectors.items():
            single_opinion[key]=get_element(opinion, *value)
        all_opinions.append(single_opinion)   
    page_no = page_no + 1

with open(f'.\opinions\{product_code}.json', "w", encoding='UTF-8') as jf:
    json.dump(all_opinions, jf, indent=4, ensure_ascii= False)
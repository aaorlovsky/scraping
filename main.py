import requests
from bs4 import BeautifulSoup
import pprint


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.a.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


def get_texts_susbtext(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    # css selectors . - class, # - id
    texts = soup.select('.titleline')
    subtext = soup.select('.subtext')
    return texts, subtext


res = requests.get('https://news.ycombinator.com/news')
texts, subtext = get_texts_susbtext(res)
res2 = requests.get('https://news.ycombinator.com/news?p=2')
texts2, subtext2 = get_texts_susbtext(res2)
texts = texts + texts2
subtext = subtext + subtext2
pprint.pprint(create_custom_hn(texts, subtext))



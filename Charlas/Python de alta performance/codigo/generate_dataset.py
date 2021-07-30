# -*- coding: utf-8 -*-

import requests
import bs4

WIKI_PAGES = [
    "https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm",
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
]

GITHUB_PAGES = ["https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"]


def get_words_from_wikipages():
    words = set()
    for page in WIKI_PAGES:
        response = requests.get(page)
        bs = bs4.BeautifulSoup(response.content)

        body_content = bs.find("div", {"id": "bodyContent"})
        body_words = body_content.get_text().split()
        # make sure that the words are clanned
        body_words = [word.strip() for word in body_words]
        # remove the words that include comma because
        # they will break the parser
        body_words = [word for word in body_words if word and "," not in word]
        words.update(body_words)

    return words


def get_words_from_github():
    words = set()
    for page in GITHUB_PAGES:
        response = requests.get(page)
        body_words = response.text.split()
        body_words = [word.strip() for word in body_words]
        # remove the words that include comma because
        # they will break the parser
        body_words = [word for word in body_words if word and "," not in word]
        words.update(body_words)

    return words


words = get_words_from_github()
for step_size in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15):
    with open("dataset.%s.txt" % step_size, "w") as output:
        lwords = list(words)
        for i in range(0, len(lwords) - step_size, step_size + 1):
            output.write("%s,%s\n" % (lwords[i], lwords[i + step_size]))

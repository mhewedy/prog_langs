from urllib import request
from lxml import etree

base_url = 'https://en.wikipedia.org'
visited = []


def get_lang(lang_url):
    if lang_url in visited:
        return

    visited.append(lang_url)

    with request.urlopen(base_url + lang_url) as response:
        html = response.read()
        tree = etree.HTML(html)
        print(lang_url)
        get_influenced(tree)
        get_influenced_by(tree)


def get_influenced(tree):
    get_xpath_by_text(tree, 'Influenced')


def get_influenced_by(tree):
    get_xpath_by_text(tree, 'Influenced by')


def get_xpath_by_text(tree, text):
    try:
        influenced = tree.xpath(f"//*[text() = '{text}']")[0]
        influenced_langs = influenced.getparent().getnext().getchildren()[0].getchildren()

        influenced_lang_urls = []

        for influenced_lang in influenced_langs:
            if influenced_lang.text is not None:
                new_lang_url = influenced_lang.get("href")
                influenced_lang_urls.append(new_lang_url)

        for ll in influenced_lang_urls:
            get_lang(ll)
    except Exception as e:
        # print(e)
        pass


get_lang('/wiki/Python_(programming_language)')

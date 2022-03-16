from urllib import request
from lxml import etree

BASE_URL = 'https://en.wikipedia.org'
visited = []


def get_lang(lang_url):
    if lang_url in visited:
        return

    visited.append(lang_url)

    with request.urlopen(BASE_URL + lang_url) as response:
        html = response.read()
        tree = etree.HTML(html)
        influenced = get_influenced(tree)
        influenced_by = get_influenced_by(tree)

        print("language: " + lang_url +
              " ,influenced: " + str(influenced) +
              " ,influenced_by: " + str(influenced_by))


def get_influenced(tree):
    return get_xpath_by_text(tree, 'Influenced')


def get_influenced_by(tree):
    return get_xpath_by_text(tree, 'Influenced by')


def get_xpath_by_text(tree, text):
    try:
        influenced = tree.xpath(f"//*[text() = '{text}']")[0]
        influenced_langs = influenced.getparent().getnext().findall(".//a")

        urls = []

        for influenced_lang in influenced_langs:
            if influenced_lang.getparent().tag != 'sup' and influenced_lang.text is not None:
                url = influenced_lang.get("href")
                urls.append(url)
                get_lang(url)

        return urls
    except:
        return []


def main():
    get_lang('/wiki/Python_(programming_language)')


if __name__ == '__main__':
    main()

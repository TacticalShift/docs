from pathlib import Path
import re
import codecs
import json
import dropdowns


def makedropdowns(navbardict: dict):
    articles = []
    config = dropdowns.SECTION_CONFIGURATION
    for key, value in navbardict.items():
        for item in value:
            filename, meta = item
            article = {'title': None, "section": None, "url": None}
            article['title'] = meta['Title']
            article['section'] = config[key]['src']
            article['url'] = "/"+filename+".html"
            articles.append(article)
            if 'Subpages' in meta:
                for subfilename, submeta in meta['Subfolder']:
                    article = {'title': None, "section": None, "url": None}
                    article['title'] = submeta['Title']
                    article['section'] = [config[key]['src'], meta['Subpages']]
                    article['url'] = "/"+subfilename+".html"
                    articles.append(article)
    print(articles)
    return dropdowns


makedropdowns(dropdowns.makenavbardict())

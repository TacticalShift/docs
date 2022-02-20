import json
import dropdowns

ARTCILE_TEMPLATE = '''
const articles = 
    {articles}
'''
KEYWORDS_TEMPLATE = '''
const KEYWORDS  =
{keywords}
'''


def makekeywords(navbardict: dict):
    articles = []
    keywords = {}
    config = dropdowns.SECTION_CONFIGURATION
    for key, value in navbardict.items():
        for item in value:
            filename, meta = item
            article = {'title': None, "section": None,
                       "url": None, "keywords": None}
            article['title'] = meta['Title']
            article['section'] = config[key]['src']
            article['url'] = "/"+filename+".html"
            article['keywords'] = meta["Keywords"]
            for keyword in meta['Keywords']:
                if keyword in keywords:
                    keywords[keyword] = keywords[keyword] + 1
                else:
                    keywords[keyword] = 1
            articles.append(article)
            if 'Subpages' in meta:
                for subfilename, submeta in meta['Subfolder']:
                    article = {'title': None, "section": None, "url": None}
                    article['title'] = submeta['Title']
                    article['section'] = [config[key]['src'], meta['Subpages']]
                    article['url'] = "/"+config[key]['src'] + \
                        "/"+subfilename+".html"
                    article['keywords'] = submeta["Keywords"]
                    articles.append(article)
                    for keyword in submeta['Keywords']:
                        if keyword in keywords:
                            keywords[keyword] = keywords[keyword] + 1
                        else:
                            keywords[keyword] = 1

    return (articles, keywords)


def keywordsmaker():
    outputart, outputkeys = makekeywords(dropdowns.makenavbardict())
    articlestr = ARTCILE_TEMPLATE.format(articles=json.dumps(
        outputart, indent=4, ensure_ascii=False))
    keywordstr = KEYWORDS_TEMPLATE.format(
        keywords=json.dumps(outputkeys, indent=4))
    with open("../src/keywords.js", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(articlestr)
        output_file.write(keywordstr)
        output_file.close()


keywordsmaker()

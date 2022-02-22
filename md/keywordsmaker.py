import json
import dropdowns

ARTCILE_TEMPLATE = '''
const ARTICLES = 
    {articles}
'''
KEYWORDS_TEMPLATE = '''
const KEYWORDS  =
{keywords}
'''


def make_keywords(navbardict: dict):
    articles = []
    keywords = {}
    config = dropdowns.SECTION_CONFIGURATION
    for key, value in navbardict.items():
        for item in value:
            filename, meta = item
            article = {'title': None, "section": None,
                       "url": None, "keywords": None}
            article['title'] = meta['Title']
            article['section'] = [config[key]['src']]
            article['url'] = "/".join(["/docs", config[key]
                                      ['src'], filename+".html"])
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
                    article['url'] = "/".join(["/docs", config[key]
                                              ['src'], meta['Subpages'], subfilename+".html"])
                    article['keywords'] = submeta["Keywords"]
                    articles.append(article)
                    for keyword in submeta['Keywords']:
                        if keyword in keywords:
                            keywords[keyword] = keywords[keyword] + 1
                        else:
                            keywords[keyword] = 1

    return (articles, keywords)


def keywords_maker():
    output_article, output_keys = make_keywords(dropdowns.make_navbardict())
    article_str = ARTCILE_TEMPLATE.format(articles=json.dumps(
        output_article, indent=4, ensure_ascii=False))
    keyword_str = KEYWORDS_TEMPLATE.format(
        keywords=json.dumps(output_keys, indent=4))
    with open("../src/keywords.js", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(article_str)
        output_file.write(keyword_str)
        output_file.close()

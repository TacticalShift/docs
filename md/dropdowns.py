
from pathlib import Path
from turtle import title
import bs4
import xml.etree.ElementTree as etree
import templatehtml
import re
import json
import codecs

SECTION_CONFIGURATION = {
    # Порядок следования секций в navbar'е
    "order": ["_docs", "_sop", "_tco", "_mmo", "_srv"],

    # Описание секции
    "_sop": {
        "title": "SOPs",  # Отображаемое название секции в navbar'e
        # Текст для всплывающего текста при наведении (опционально), html-свойство title
        "tooltip": "Standard Operation Procedures",
        "src": "SOP"  # Имя папки первого уровня где хранятся страницы
    },
    "_docs": {
        "title": "Документация",
        "src": "Docs",
        "tooltip": "Documantation"
    },
    "_tco": {
        "title": "TCO",
        "tooltip": "Training Center Office",
        "src": "TCO"
    },
    "_mmo": {
        "title": "MMO",
        "tooltip": "Mission Making Office",
        "src": "MMO"
    },
    "_srv": {
        "title": "SRV",
        "tooltip": "Server magic",
        "src": "SRV"
    }
}

# @Meta(key1=value1, key2=value2, key3=value3)


def readmeta(filepath: str):
    file = codecs.open(
        filepath, 'r', "utf_8_sig")
    line = file.readline(10000)
    i = re.search("@Meta\((.*?)\)", line)
    meta = {}
    if i:
        for item in i.group(1).split(','):
            key, value = item.split('=')
            meta[key.strip()] = value.strip()
    return meta


def readtitle(filepath: str):
    file = codecs.open(
        filepath, 'r', "utf_8_sig")
    title = "None"
    line = file.readline(10000)
    while line:
        n = re.search("(<=\s|^)#{1}[^#](.*?)$", line)
        if n:
            title = n.group(2).strip()
            break
        line = file.readline(10000)
    return title


def makesubfolderdict(pathstr: str):
    path = Path(pathstr)
    subfolderdict = {}
    for x in path.iterdir():
        if x.is_file():
            filename = x.name.split(".")[0]
            meta = {}
            meta = readmeta(x)
            if not 'Title' in meta:
                meta['Title'] = readtitle(x)
            if not 'Position' in meta:
                meta['Position'] = 1000
            subfolderdict[filename] = meta
    return subfolderdict


def makefolderdict(pathstr: str):
    path = Path(pathstr)
    folderdict = {}
    for x in path.iterdir():
        if x.is_file():
            filename = x.name.split(".")[0]
            meta = {}
            meta = readmeta(x)
            if not 'Title' in meta:
                meta['Title'] = readtitle(x)
            if not 'Position' in meta:
                meta['Position'] = 1000
            if 'Subpages' in meta:
                subdict = makesubfolderdict(
                    "\\".join([x, meta['Subpages']]))
                sublist = subdict.items()
                sublist = sorted(
                    sublist,
                    key=lambda x: int(x[1]['Position']),
                    reverse=False
                )
                folderdict['Subpages'] = sublist
            folderdict[filename] = meta
    folderlist = folderdict.items()
    folderlist = sorted(
        folderlist,
        key=lambda x: int(x[1]['Position']),
        reverse=False
    )
    return folderlist


def makesubpages(fileslist: list):
    subpages = []
    for file in fileslist:
        filename, meta = file
        subpages.append(templatehtml.HTML_DROPDOWN_ELEMENT.
                        format(url=(".\\"+filename+".html"),
                               title=meta['Title'])
                        )


def makedropdowns(navbardict: dict):
    config = SECTION_CONFIGURATION
    dropdowns = []
    for key, value in navbardict.items():
        elements = []
        for item in value:
            filename, meta = item
            element = ""
            if 'Subfolder' in meta:
                subpages = makesubpages(meta['Subfolder'])
                if 'Hide' in meta and int(meta['Hide']) == 1:
                    element = templatehtml.HTML_DROPDOWN_EXTENDED_INACTIVE.format(
                        title=meta['Title'],
                        subpages=subpages
                    )
                else:
                    element = templatehtml.HTML_DROPDOWN_EXTENDED.format(
                        url=".\\"+filename+".html",
                        title=meta['Title'],
                        subpages=subpages
                    )
            else:
                element = templatehtml.HTML_DROPDOWN_ELEMENT.format(url=(filename+".html"),
                                                                    title=meta['Title']
                                                                    )
            elements.append(element)
        dropdowns.append(templatehtml.HTML_DROPDOWN_SECTION.format(tooltip=config[key]['tooltip'],
                                                                   title=config[key]['title'],
                                                                   elements="".join(
                                                                       elements)
                                                                   )
                         )
    return dropdowns


def makenavbarlist():
    config = SECTION_CONFIGURATION
    navbardict = {}
    for section in config["order"]:
        folder = config[section]['src']
        navbardict[section] = makefolderdict(folder)
    return navbardict


def makenavbar():
    dropdowns = makedropdowns(makenavbarlist())
    navbar = templatehtml.HTML_NAVBAR_SECTION.format(
        dropdowns="".join(dropdowns))
    soup = bs4.BeautifulSoup(navbar, "html.parser")
    return soup.prettify()


print(makenavbar())

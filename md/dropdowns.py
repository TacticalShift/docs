from pathlib import Path
import templatehtml
import re
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
        "tooltip": "Documentation"
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


def read_meta(filepath: str):
    file = codecs.open(
        filepath, 'r', "utf_8_sig")
    line = file.readline(10000)
    i = re.search("@Meta\((.*?)\)", line)
    meta = {}
    while line:
        if i:
            for item in i.group(1).split(','):
                key, value = item.split('=')
                meta[key.strip()] = value.strip()
            break
        line = file.readline(10000)
    return meta


def read_keywords(filepath: str):
    file = codecs.open(
        filepath, 'r', "utf_8_sig")
    line = file.readline(10000)
    keywords = []
    while line:
        i = re.search("@Keywords\((.*?)\)", line)
        if i:
            for item in i.group(1).split(','):
                keywords.append(item.strip())
            break
        line = file.readline(10000)

    return keywords


def read_title(filepath: str):
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


def make_folderlist(pathstr: str):
    path = Path(pathstr)
    folderdict = {}

    print('[Dropdowns.make_folderlist] Checking for', path)
    if not path.exists():
        print('[Dropdowns.make_folderlist] Not found', path)
        return folderdict
    for x in path.iterdir():
        print('[Dropdowns.make_folderlist] ', x)
        if x.is_file():
            filename = x.name.split(".")[0]
            meta = {}
            meta = read_meta(x)
            meta['Keywords'] = read_keywords(x)
            meta.setdefault('Title', read_title(x))
            meta.setdefault('Position', 1000)
            folderdict[filename] = meta
            if 'Subpages' in meta:
                print(
                    '[Dropdowns.make_folderlist] Found subfolder', meta['Subpages'], 'in meta')
                subpath = "/".join([path.name, meta['Subpages']])
                sublist = make_folderlist(subpath)
                folderdict[filename]['Subfolder'] = sublist

    folderlist = folderdict.items()
    folderlist = sorted(
        folderlist,
        key=lambda x: int(x[1]['Position']),
        reverse=False
    )
    return folderlist


def make_subpages(folder: str, subfolder: str, files_list: list):
    subpages = []
    for file in files_list:
        filename, meta = file
        filepath = "/".join(["docs", folder, subfolder, filename])
        subpages.append(templatehtml.HTML_DROPDOWN_ELEMENT.
                        format(url=("/"+filepath+".html"),
                               title=meta['Title'])
                        )
    return subpages


def make_dropdowns(navbar_dict: dict):
    config = SECTION_CONFIGURATION
    dropdowns = []
    for key, value in navbar_dict.items():
        elements = []
        for filename, meta in value:
            
            element = ""
            if 'Subpages' in meta:
                subpages = make_subpages(
                    config[key]['src'], meta['Subpages'], meta['Subfolder'])
                if 'Hide' in meta and int(meta['Hide']) == 1:
                    element = templatehtml.HTML_DROPDOWN_EXTENDED_INACTIVE.format(
                        title=meta['Title'],
                        subpages="".join(subpages)
                    )
                else:
                    element = templatehtml.HTML_DROPDOWN_EXTENDED.format(
                        url="/".join(["/docs", config[key]
                                     ['src'], filename+".html"]),
                        title=meta['Title'],
                        subpages="".join(subpages)
                    )
            elif 'Hide' in meta and int(meta['Hide']) == 1:
                continue
            else:
                filepath = "/".join(["docs", config[key]['src'], filename])
                element = templatehtml.HTML_DROPDOWN_ELEMENT.format(url="/"+filepath + ".html",
                                                                    title=meta['Title']
                                                                    )
            elements.append(element)
        dropdowns.append(templatehtml.HTML_DROPDOWN_SECTION.
                         format(
                             tooltip=config[key]['tooltip'],
                             title=config[key]['title'],
                             elements="".join(
                                 elements)
                         )
                         )
    return dropdowns


def make_navbardict():
    config = SECTION_CONFIGURATION
    navbar_dict = {}
    for section in config["order"]:
        folder = config[section]['src']
        navbar_dict[section] = make_folderlist(folder)
    return navbar_dict


def make_navbar(navbardict: dict = None):
    dropdowns = make_dropdowns(navbardict if navbardict else make_navbardict())
    navbar = templatehtml.HTML_NAVBAR_SECTION.format(
        dropdowns="".join(dropdowns))
    return navbar

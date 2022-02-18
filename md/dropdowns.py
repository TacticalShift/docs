
from pathlib import Path
import bs4
import xml.etree.ElementTree as etree
import templatehtml
import re
import json

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
        "src": "Docs"
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


def makefolderdict(pathstr: str):
    path = Path(pathstr)

    dropdowndict = {}
    for x in path.iterdir():
        if x.is_dir():
            dropdowndict[x.name] = {}
            i = 0
            for y in x.iterdir():
                if y.is_file():
                    filename = y.name.split(".")[0]
                    dropdowndict[x.name][i] = filename+'.html'
                if y.is_dir():
                    dropdowndict[x.name][y.name] = {}
                    k = 0
                    for z in y.iterdir():
                        if z.is_file():
                            filename = z.name.split(".")[0]
                            dropdowndict[x.name][y.name][k] = filename+'.html'
                            k += 1
                i += 1
    print(dropdowndict)
    return dropdowndict


for folder, value in SECTION_CONFIGURATION.items():
    print(folder)
    print(value)


def makedropdowns(dropdowndict: dict):
    # outpath = Path("output")
    # outpath.mkdir(exist_ok=True)
    dropdowns = []
    for folder, item in dropdowndict.items():
        folderelements = []
        dropdownsl2 = []
        for subfolder, element in item.items():
            if (type(element) == dict):
                subfolderelements = []
                for subkey, subelement in element.items():
                    title = subelement.split('.')[0]
                    url = templatehtml.ELEMENT_URL.format(filename=title)
                    subfolderelements.append(templatehtml.DROPDOWN_ELEMENT.format(
                        url=url, title=title))
                subhrefs = "\n".join(subfolderelements)
                url = templatehtml.ELEMENT_URL.format(filename=subfolder)
                dropdownsl2.append(templatehtml.TEMPLATE_DROPDOWN_LEVEL2.format(url=url,
                                                                                section=subfolder, elements=subhrefs))
            else:
                title = element.split('.')[0]
                url = templatehtml.ELEMENT_URL.format(filename=title)
                folderelements.append(templatehtml.DROPDOWN_ELEMENT.format(
                    url=url, title=title))
        elhrefs = "\n".join(folderelements)
        dropl2 = "\n".join(dropdownsl2)
        dropdowns.append(templatehtml.TEMPLATE_DROPDOWN.format(
            section=folder, elements=elhrefs, level2=dropl2))
    text_file = "\n".join(dropdowns)
    soup = bs4.BeautifulSoup(text_file, "html.parser")
    return soup.prettify()


# with open("output.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
#     output_file.write(handledropdowns({}))

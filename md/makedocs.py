from markdown import Markdown
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
from markdown.extensions.toc import TocExtension
from markdown.inlinepatterns import InlineProcessor

import re
from pathlib import Path
import xml.etree.ElementTree as etree

from tablepreprocessor import TablesPreprocessor as dznTablesPreproc

import keywordsmaker
import templatehtml
import dropdowns


class ColorInlineProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        attrib = {"style": "color:" + m.group(2)}
        el = etree.Element('span', attrib)
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class KeyboardInlineProcessor(InlineProcessor):
    def __init__(self, pattern, tag):
        InlineProcessor.__init__(self, pattern)
        self.tag = tag

    def handleMatch(self, m, data):  # pragma: no cover
        el = etree.Element(self.tag)
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class TagsExtension(Extension):
    def extendMarkdown(self, md):
        COLOR_PATTERN = r'\^(.*?)\^\[(.*?)]'
        KEYBOARD_PATTERN = r'\~(.*?)\~'
        TAGMARK_PATTERN = r'\^(.*?)\^'
        HIGHTLIGHT_PATTERN = r'\^\^(.*?)\^\^'
        WARN_PATTERN = r'\!(.*?)\!'
        md.inlinePatterns.register(KeyboardInlineProcessor(
            KEYBOARD_PATTERN, 'kbd'), 'kbd', 175)
        md.inlinePatterns.register(KeyboardInlineProcessor(
            TAGMARK_PATTERN, 'mark'), 'mark', 176)
        md.inlinePatterns.register(KeyboardInlineProcessor(
            HIGHTLIGHT_PATTERN, 'highlight'), 'highlight', 177)
        md.inlinePatterns.register(KeyboardInlineProcessor(
            WARN_PATTERN, 'warn'), 'warn', 178)
        md.inlinePatterns.register(
            ColorInlineProcessor(COLOR_PATTERN, md), 'coloring', 179)


class TitleFinderPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []

        for line in lines:
            n = re.search("(<=\s|^)#{1}[^#](.*?)$", line)
            if n:
                j = re.search("\{menu:(.*?)}", line)
                if j:
                    self.md.title = j.group(1)
                else:
                    self.md.title = n.group(2)
                self.md.articletitle = n.group(2).split('{')[0]
            else:
                new_lines.append(line)
        return new_lines


class TitleFinderExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.title = "PlaceHolder"
        md.articletitle = "Placeholder"
        md.preprocessors.register(
            TitleFinderPreprocessor(md), 'title_finder', 25)


class NoRenderPreprocessor(Preprocessor):
    def run(self, lines):
        new_lines = []

        for line in lines:
            n = re.search("NORENDER", line)
            if not n:
                new_lines.append(line)
        return new_lines


class NoRenderExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(
            NoRenderPreprocessor(md), 'no_render', 26)


class TablePreprocessorWrapper(Preprocessor):
    def run(self, lines):
        wrp = dznTablesPreproc(self.md, log_level=0)
        return wrp.preprocess(lines)


class TablePreprocessorExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        md.preprocessors.register(
            TablePreprocessorWrapper(md), 'TablePreproc', 10)


def make_page(input_text, title: str, dropdown: str):

    md = Markdown(
        extensions=[
            TitleFinderExtension(),
            'fenced_code',
            TagsExtension(),
            TocExtension(
                marker=None,
                toc_depth="2-6"),
            TablePreprocessorExtension(),
            NoRenderExtension()
        ]
    )
    article_text = md.convert(input_text)
    page = md.toc
    body = templatehtml.HTML_BODY.format(navbar=dropdown,
                                         article=article_text, toc=md.toc,
                                         title=title)
    head = templatehtml.HTML_HEAD.format(title=title)
    page = templatehtml.HTML_PAGE.format(head=head, body=body)
    md.reset()
    return page


def make_htmlfile(inputpath: str, filename: str, dropdown: str, title: str):
    with open("."+inputpath, "r", encoding="utf-8") as input_file:
        input_text = input_file.read()
        input_file.close()
    # wrp = dznTablesPreproc()
    # input_text = wrp.preprocess(input_text)
    # input_text = "".join(input_text)
    html_page = make_page(input_text, title, dropdown)
    with open(filename, "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(html_page)
        output_file.close()


def make_searh_page(filename: str, dropdown: str):
    body = templatehtml.HTML_BODY_SEARCH_PAGE.format(navbar=dropdown)
    head = templatehtml.HTML_HEAD_SEARCH_PAGE
    html_page = templatehtml.HTML_PAGE.format(head=head, body=body)
    with open(filename, "w", encoding="utf-8") as output_file:
        output_file.write(html_page)
        output_file.close()


if __name__ == "__main__":
    rootdir = ""
    config = dropdowns.SECTION_CONFIGURATION
    dropdown_dict = dropdowns.make_navbardict()
    dropdown = dropdowns.make_navbar()
    keywordsmaker.keywords_maker()
    for section, item in dropdown_dict.items():
        for filename, meta in item:
            folder = config[section]['src']
            output_path = "/".join([folder, filename])
            pathfolder = Path("../"+folder)
            pathfolder.mkdir(exist_ok=True)
            make_htmlfile(
                "/".join([rootdir, folder, filename+".md"]),
                "../"+output_path+".html",
                dropdown,
                meta['Title']
            )
            if 'Subfolder' in meta:
                for subfilename, submeta in meta['Subfolder']:
                    pathfolder = Path("../" + folder+"/" + meta['Subpages'])
                    pathfolder.mkdir(exist_ok=True)
                    output_path = "/".join([folder,
                                            meta['Subpages'], subfilename])
                    make_htmlfile(
                        "/".join([rootdir, folder, filename,
                                 subfilename+".md"]),
                        "../"+output_path+".html",
                        dropdown,
                        submeta['Title']
                    )
    make_htmlfile("/index.md", "../index.html", dropdown, "tsDocs")
    make_searh_page("../search.html", dropdown)

from markdown import Markdown
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
from markdown.extensions.toc import TocExtension
from markdown.inlinepatterns import InlineProcessor

import sys
import traceback
import re
from pathlib import Path
import xml.etree.ElementTree as etree

from tablepreprocessor import TablesPreprocessor as dznTablesPreproc

import keywordsmaker
import templatehtml
import dropdowns


class ColorInlineProcessor(InlineProcessor):
    def getCompiledRegExp(self):
        return re.compile(self.pattern)
    def handleMatch(self, m, data):
        attrib = {"style": "color:" + m.group(2)}
        el = etree.Element('span', attrib)
        el.text = m.group(1)
        return el, m.start(0), m.end(0)


class KeyboardInlineProcessor(InlineProcessor):
    def __init__(self, pattern, tag):
        InlineProcessor.__init__(self, pattern)
        self.tag = tag
    def getCompiledRegExp(self):
        return re.compile(self.pattern)
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
    def __init__(self, md=None):
        super().__init__(md)
        self.inside_code_block = False
    def run(self, lines):
        new_lines = []

        for line in lines:
            if line.strip().startswith("```"):
                # Toggle the inside_code_block flag when encountering code block markers
                self.inside_code_block = not self.inside_code_block
            if not self.inside_code_block:
                n = re.search("NORENDER", line)
                if not n:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        return new_lines


class NoRenderExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(
            NoRenderPreprocessor(md), 'no_render', 26)


class TablePreprocessorWrapper(Preprocessor):
    def run(self, lines):
        wrp = dznTablesPreproc(log_level=0)
        return wrp.preprocess(lines)


class TablePreprocessorExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        md.preprocessors.register(
            TablePreprocessorWrapper(md), 'TablePreproc', 10)


class DocsMaker:
    def __init__(self, log_level):
        self.LOG_LEVEL = log_level  # 0 - None, 1 - Enable, 2 - Verbose

    def make_page(self, input_text, title: str, dropdown: str):
        LOG = True and self.LOG_LEVEL > 0
        VERBOSE = LOG and self.LOG_LEVEL > 1

        LOG and print('[DocsMaker.make_page] Invoked for', title)
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
        VERBOSE and print('[DocsMaker.make_page]    Parsing markdown')
        article_text = md.convert(input_text)
        page = md.toc

        VERBOSE and print('[DocsMaker.make_page]    Composing HTML')
        header = templatehtml.HTML_HEADER.format(navbar=dropdown)
        body = templatehtml.HTML_BODY.format(header=header,
                                             article=article_text, toc=md.toc,
                                             title=title)
        head = templatehtml.HTML_HEAD.format(title=title)
        page = templatehtml.HTML_PAGE.format(head=head, body=body)
        LOG and print('[DocsMaker.make_page]    HTML Composed')

        md.reset()
        VERBOSE and print('[DocsMaker.make_page]    Markdown reset')

        return page

    def make_htmlfile(self, inputpath: str, filename: str, dropdown: str, title: str):
        LOG = True and self.LOG_LEVEL > 0
        VERBOSE = LOG and self.LOG_LEVEL > 1

        LOG and print('[DocsMaker.make_htmlfile] Invoked for', inputpath)

        with open("."+inputpath, "r", encoding="utf-8") as input_file:
            input_text = input_file.read()
            input_file.close()
        VERBOSE and print(
            '[DocsMaker.make_htmlfile]    File read successfully!')

        html_page = self.make_page(input_text, title, dropdown)

        VERBOSE and print(
            '[DocsMaker.make_htmlfile]    Writing HTML to %s' % filename)
        with open(filename, "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
            output_file.write(html_page)
            output_file.close()
        LOG and print(
            '[DocsMaker.make_htmlfile] File %s created successfully!' % filename)

    def make_searh_page(self, filename: str, dropdown: str):
        LOG = True and self.LOG_LEVEL > 0
        VERBOSE = LOG and self.LOG_LEVEL > 1

        LOG and print('[DocsMaker.make_searh_page] Invoked for', filename)
        header = templatehtml.HTML_HEADER.format(navbar=dropdown)
        body = templatehtml.HTML_BODY_SEARCH_PAGE.format(header=header)
        head = templatehtml.HTML_HEAD_SEARCH_PAGE
        html_page = templatehtml.HTML_PAGE.format(head=head, body=body)
        VERBOSE and print(
            '[DocsMaker.make_searh_page]    HTML formatted, writing to file')
        with open(filename, "w", encoding="utf-8") as output_file:
            output_file.write(html_page)
            output_file.close()

        LOG and print(
            '[DocsMaker.make_searh_page] File %s created successfully!' % filename)


if __name__ == "__main__":
    rootdir = ""
    config = dropdowns.SECTION_CONFIGURATION

    try:
        dropdown_dict = dropdowns.make_navbardict()
        dropdown = dropdowns.make_navbar()
        keywordsmaker.keywords_maker()
    except Exception:
        print(traceback.format_exc())
        print('[ERROR] Error occured during data preparation!')
        input('Press Enter to close...')
        sys.exit(-1)

    try:
        dm = DocsMaker(log_level=2)
        for section, item in dropdown_dict.items():
            for filename, meta in item:
                folder = config[section]['src']
                output_path = "/".join([folder, filename])
                pathfolder = Path("../"+folder)
                pathfolder.mkdir(exist_ok=True)
                dm.make_htmlfile(
                    "/".join([rootdir, folder, filename+".md"]),
                    "../"+output_path+".html",
                    dropdown,
                    meta['Title']
                )
                if 'Subfolder' in meta:
                    for subfilename, submeta in meta['Subfolder']:
                        pathfolder = Path(
                            "../" + folder+"/" + meta['Subpages'])
                        pathfolder.mkdir(exist_ok=True)
                        output_path = "/".join([folder,
                                                meta['Subpages'], subfilename])
                        dm.make_htmlfile(
                            "/".join([rootdir, folder, filename,
                                      subfilename+".md"]),
                            "../"+output_path+".html",
                            dropdown,
                            submeta['Title']
                        )

        dm.make_htmlfile("/index.md", "../index.html", dropdown, "tsDocs")
        dm.make_searh_page("../search.html", dropdown)
    except Exception:
        print(traceback.format_exc())
        print('[ERROR] Error occured on converting pages!')
        input('Press Enter to close...')
        sys.exit(-1)

    input("\n\n" + 25*'-' + "\nAll done! Have a nice day!")

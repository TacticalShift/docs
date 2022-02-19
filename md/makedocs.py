from msilib.schema import Extension
from markdown import Markdown
from markdown.inlinepatterns import SimpleTagInlineProcessor
import markdown
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
from markdown.extensions.toc import TocExtension
import re
from markdown.inlinepatterns import InlineProcessor
import xml.etree.ElementTree as etree
from tablepreprocessor import TablesPreprocessor as dznTablesPreproc
import templatehtml
import dropdowns
import bs4
from pathlib import Path


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
            NoRenderPreprocessor(md), 'prio_finder', 26)


class TablePreprocessorWrapper(Preprocessor):
    def run(self, lines):
        wrp = dznTablesPreproc()
        return wrp.preprocess(lines)


class TablePreprocessorExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        md.preprocessors.register(
            TablePreprocessorWrapper(), 'TablePreproc', 1)


def makepage(input_text: str, title: str, dropdown: str):

    md = markdown.Markdown(
        extensions=[
            TitleFinderExtension(),
            'tables',
            TagsExtension(),
            TocExtension(
                marker=None,
                toc_depth="2-6"),
            TablePreprocessorExtension(),
            'attr_list',
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
    soup = bs4.BeautifulSoup(page, "html.parser")
    return soup.prettify()


def makehtmlfile(inputpath: str, filename: str, dropdown: str, title: str):
    with open("."+inputpath, "r", encoding="utf-8") as input_file:
        input_text = input_file.read()
        input_file.close()
    htmlpage = makepage(input_text, title, dropdown)
    with open(filename, "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(htmlpage)
        output_file.close()


if __name__ == "__main__":
    rootdir = ""
    config = dropdowns.SECTION_CONFIGURATION
    dropdowndict = dropdowns.makenavbardict()
    dropdown = dropdowns.makenavbar()
    for section, item in dropdowndict.items():
        for filename, meta in item:
            folder = config[section]['src']
            outputpath = "/".join([folder, filename])
            pathfolder = Path("../"+folder)
            pathfolder.mkdir(exist_ok=True)
            makehtmlfile(
                "/".join([rootdir, folder, filename+".md"]),
                "../"+outputpath+".html",
                dropdown,
                meta['Title']
            )
            if 'Subfolder' in meta:
                for subfilename, submeta in meta['Subfolder']:
                    pathfolder = Path("../" + folder+"/" + meta['Subpages'])
                    pathfolder.mkdir(exist_ok=True)
                    outputpath = "/".join([folder,
                                          meta['Subpages'], subfilename])
                    makehtmlfile(
                        "/".join([rootdir, folder, filename,
                                 subfilename+".md"]),
                        "../"+outputpath+".html",
                        dropdown,
                        submeta['Title']
                    )

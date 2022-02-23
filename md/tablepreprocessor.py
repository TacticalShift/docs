from dataclasses import dataclass, field
import os


class TablesPreprocessor():
    # Markdown extension syntax
    STYLE_MACRO_OPEN = "{:"
    STYLE_MACRO_CLOSE = ":}"
    STYLE_TABLE_PREFIX = "table."
    STYLE_ROW_PREFIX = "row."

    # HTML templates
    HTML_TABLE = '<table{attrs}>{rows}</table>'
    HTML_TABLE_ROW = '<tr{attrs}>{cells}</tr>'
    HTML_TABLE_CELL = '<td{attrs}>{cell}</td>'
    HTML_TABLE_HEADER_CELL = '<th{attrs}>{cell}</th>'

    HTML_ATTR_ID = 'id="%s"'
    HTML_ATTR_CLASS = 'class="%s"'
    HTML_ATTR_CELL_COLSPAN = 'colspan="%s"'
    HTML_ATTR_STYLE = 'style="%s"'

    @dataclass
    class Attributes:
        """
        Element (cell/row/table) html and css attributes.
        _id     -- html ID attribute (string)
        classes -- list of classes assigned (list of strings)
        css     -- list of css attributes applied (list of
                   strings in key:value pairs)
        """
        _id: str = field(default_factory=lambda: None)
        classes: list = field(default_factory=lambda: [])
        css: list = field(default_factory=lambda: [])

        # Updates Attributes using given Attributes object
        # CSS and classes will be added, ID will be overwritten
        def update(self, attributes):
            self.css += attributes.css
            self.classes += attributes.classes
            self._id = attributes._id

        # Parses attributes from given line
        # CSS and classes will be added, ID will be overwritten
        def parse(self, line):
            if line.startswith('class:'):
                self.classes.append(line.replace('class:', ''))
            elif line.startswith('id:'):
                self._id = line.replace('id:', '')
            else:
                self.css.append(line)

    @dataclass
    class Table:
        starts_at: int
        ends_at: int = -1
        header_border_at: int = -1
        raw_lines: list = field(default_factory=lambda: [])
        rows: list = field(default_factory=lambda: [])
        html: str = field(default_factory=lambda: None)

        def __post_init__(self):
            self.attributes = TablesPreprocessor.Attributes()

    @dataclass
    class Row:
        cells: list = field(default_factory=lambda: [])

        def __post_init__(self):
            self.attributes = TablesPreprocessor.Attributes()

    @dataclass
    class Cell:
        content: str
        attributes: list
        colspan: int = 1

    def __init__(self, log_level=0):
        self.LOG_LEVEL = log_level  # 0 - None, 1 - Enable, 2 - Verbose

    """Main public method.
    Reads markdown tables and replace it with raw HTML table.
    Parse and applies styles/class/id to td/tr/table elements.
    Params:
    0: lines -- list of lines of raw markdown (list of strings)

    Return: list of lines (same list as was given)
    """
    def preprocess(self, lines):
        self.lines = lines
        self.pointer_offset = 0

        self.tables = self.__find_tables()
        for i, t in enumerate(self.tables):
            self.__parse_table(t)
            self.__convert_to_html(t)
            self.__replace_in_lines(t)

        return self.lines

    # Finds markdown tables in content
    def __find_tables(self):
        LOG = True and self.LOG_LEVEL > 0  # Toggles log for method
        VERBOSE = LOG and self.LOG_LEVEL > 1

        LOG and print('[Preprocess table] Started')

        tables = []
        nested_in_codeblock = False
        for i, line in enumerate(self.lines):
            line = line.strip()
            VERBOSE and print('[Preprocess table] Read line %s: %s' % (i, line))

            if line.startswith('```'):
                nested_in_codeblock = not nested_in_codeblock
            if nested_in_codeblock:
                continue

            if line.startswith("|") and line.endswith("|") and len(line) > 1:
                VERBOSE and print('[Preprocess table]    Line is a table row!')
                if tables and tables[-1].ends_at == -1:
                    VERBOSE and print('[Preprocess table]    Adding line to existing table')
                    tables[-1].raw_lines.append(line)
                else:
                    VERBOSE and print('[Preprocess table]    Found a new table at line %s' % i)
                    table = TablesPreprocessor.Table(starts_at=i)
                    table.raw_lines.append(line)
                    tables.append(table)

                if i == len(self.lines) - 1:
                    VERBOSE and print('[Preprocess table]    Finalizing table at EOF (line %s)' % (i))
                    tables[-1].ends_at = i
            else:
                if tables and tables[-1].ends_at == -1:
                    VERBOSE and print('[Preprocess table]    Finalizing table at line %s' % (i - 1))
                    tables[-1].ends_at = i - 1

        LOG and print('[Preprocess table] Found %s tables!' % len(tables))
        return tables

    # Parses found table, it's structure and applied styles
    def __parse_table(self, table):
        LOG = True and self.LOG_LEVEL > 0  # Toggles log for method
        VERBOSE = LOG and self.LOG_LEVEL > 1

        for i, line in enumerate(table.raw_lines):
            LOG and print("[Parse table] Line: %s :: Columns in row: %s" % (line, line.count('|') - 1))

            if table.header_border_at < 0:
                stripped = line.replace('|', '').replace(' ','')
                is_border = stripped[0] == '-' and len(stripped) > 2 and stripped == len(stripped) * stripped[0]
                VERBOSE and print("[Parse table] Stripped line %s is a border? %s" % (stripped, is_border))
                if is_border:
                    table.header_border_at = i

            cells = line[1:-1].split("|")
            row = TablesPreprocessor.Row()
            for j, c in enumerate(cells):
                if len(c):
                    VERBOSE and print('[Parse table] Cell %s, content: %s' % (j, c))
                    cell, row_attributes, table_attributes = self.__parse_cell(c)
                    row.cells.append(cell)

                    if row_attributes:
                        row.attributes.update(row_attributes)
                    if table_attributes:
                        table.attributes.update(table_attributes)
                else:
                    VERBOSE and print('[Parse table] Cell %s is empty' % j)
                    if j > 0:
                        cell = row.cells[-1]
                        cell.colspan += 1
                        VERBOSE and print('[Parse table] Updating previous cell - content: %s, size: %s' % (cell.content, cell.colspan))
                    else:
                        print('[TablesPreprocessor.Parse Table] [WARNING] Incorrect table markdown! At line %s: %s' % (i, line))
            table.rows.append(row)

        LOG and print("[Parse table] Found %s rows in table" % len(table.rows))
        return

    # Parses cell content and nested style/attributes marco
    def __parse_cell(self, line):
        LOG = True and self.LOG_LEVEL > 0  # Toggles log for method
        VERBOSE = LOG and self.LOG_LEVEL > 1

        LOG and print("[Parse Cell] Parsing cell: %s" % line)

        cell_attributes = TablesPreprocessor.Attributes()
        row_attributes = None
        table_attributes = None

        attr_block_start = line.find(TablesPreprocessor.STYLE_MACRO_OPEN)
        attr_block_end = line.find(TablesPreprocessor.STYLE_MACRO_CLOSE)
        while attr_block_start > 0 and attr_block_end > 0:
            attrs = [a.strip() for a in line[attr_block_start + 2:attr_block_end].split(";")]
            for attr in attrs:
                VERBOSE and print("[Parse Cell] Attribute: %s" % attr)

                # Check for Table related attributes
                if attr.startswith(TablesPreprocessor.STYLE_TABLE_PREFIX):
                    VERBOSE and print("[Parse Cell] Table attribute found")
                    if not table_attributes:
                        table_attributes = TablesPreprocessor.Attributes()
                    table_attributes.parse(attr.replace(
                        TablesPreprocessor.STYLE_TABLE_PREFIX, ''))

                # Check for Row related attributes
                elif attr.startswith(TablesPreprocessor.STYLE_ROW_PREFIX):
                    VERBOSE and print("[Parse Cell] Row attribute found")
                    if not row_attributes:
                        row_attributes = TablesPreprocessor.Attributes()
                    row_attributes.parse(attr.replace(
                        TablesPreprocessor.STYLE_ROW_PREFIX, ""))

                # Check for Cell related attributes
                else:
                    VERBOSE and print("[Parse Cell] Cell attribute found")
                    cell_attributes.parse(attr)

            line = line[attr_block_end + 2:]
            attr_block_start = line.find(TablesPreprocessor.STYLE_MACRO_OPEN)
            attr_block_end = line.find(TablesPreprocessor.STYLE_MACRO_CLOSE)

        content = line.strip()
        cell = TablesPreprocessor.Cell(content=content, attributes=cell_attributes)
        LOG and print("[Parse Cell] Cell parsed.")
        VERBOSE and print("[Parse Cell] Cell read: %s, Row style: %s, Table style: %s" % (cell, row_attributes, table_attributes))

        return cell, row_attributes, table_attributes

    # Converts parsed table to raw html, applying html/css attributes if found
    def __convert_to_html(self, table):
        LOG = True and self.LOG_LEVEL > 0  # Toggles log for method
        VERBOSE = LOG and self.LOG_LEVEL > 1

        LOG and print('[Table2HTML] Converting to HTML')
        header_size = table.header_border_at

        rows_html = []
        for i, row in enumerate(table.rows):
            if header_size == i:
                VERBOSE and print('[Table2HTML] Row is header border - skipping...')
                continue

            cell_template = TablesPreprocessor.HTML_TABLE_CELL if i > header_size else TablesPreprocessor.HTML_TABLE_HEADER_CELL
            cells_html = []
            for cell in row.cells:
                cspan = ''
                if cell.colspan > 1:
                    cspan = ' ' + TablesPreprocessor.HTML_ATTR_CELL_COLSPAN % cell.colspan

                attrs = self.__format_html_attributes(cell.attributes) + cspan
                VERBOSE and print('[Table2HTML] Final cell attributes: %s' % attrs)
                cells_html.append(cell_template.format(
                    cell=cell.content,
                    attrs=attrs))

            row_attrs = self.__format_html_attributes(row.attributes)
            VERBOSE and print('[Table2HTML] Final row attributes: %s' % row_attrs)
            row_html = TablesPreprocessor.HTML_TABLE_ROW.format(
                                                    cells=''.join(cells_html),
                                                    attrs=row_attrs)
            rows_html.append(row_html)

        table_attrs = self.__format_html_attributes(table.attributes)
        VERBOSE and print('[Table2HTML] Final table attributes %s:' % table_attrs)
        table.html = TablesPreprocessor.HTML_TABLE.format(
                                                    rows=''.join(rows_html),
                                                    attrs=table_attrs)

        LOG and print('[Table2HTML] Table processed')
        return

    # Formats HTML/CSS attributes into raw html
    def __format_html_attributes(self, attributes):
        LOG = True and self.LOG_LEVEL > 0  # Toggles log for method
        VERBOSE = LOG and self.LOG_LEVEL > 1

        attrs = []
        if attributes._id:
            attrs.append(TablesPreprocessor.HTML_ATTR_ID % attributes._id)

        if attributes.classes:
            classes = " ".join(attributes.classes)
            attrs.append(TablesPreprocessor.HTML_ATTR_CLASS % classes)

        if attributes.css:
            css = ";".join(attributes.css)
            attrs.append(TablesPreprocessor.HTML_ATTR_STYLE % css)

        attr_line = ' '.join(attrs)
        if not attr_line:
            VERBOSE and print('[Attributes2HTML] Attributes are empty', attr_line)
            return ''

        VERBOSE and print('[Attributes2HTML] Attributes:', attr_line)
        return ' '  + attr_line

    # Modifies original lines, deletes markdown table and
    # replaces it with raw html
    def __replace_in_lines(self, table):
        LOG = True and self.LOG_LEVEL > 0  # Toggles log for method
        VERBOSE = LOG and self.LOG_LEVEL > 1

        VERBOSE and print('[Replace table]', table)

        pointer = table.starts_at - self.pointer_offset
        table_ends_at = table.ends_at - self.pointer_offset
        table_size = table_ends_at - pointer

        VERBOSE and print('[Replace table] Line to replace %s (offset: %s):\n%s\n--with--\n%s' % (pointer, self.pointer_offset, self.lines[pointer], table.html))
        self.lines[pointer] = table.html + "\n"
        pointer += 1

        LOG and print('[Replace table] Deleting lines from %s to %s' % (pointer, pointer + table_size))
        VERBOSE and print('[Replace table] Lines to cut:\n%s' % "\n".join(self.lines[pointer : pointer + table_size]))
        del self.lines[pointer:pointer + table_size]

        self.pointer_offset += table_size
        VERBOSE and print('[Replace table] New offset is: %s (diff +%s)' % (self.pointer_offset, table_size))

        return


if __name__ == "__main__":
    # Testing
    filename = "tS Docs.md"
    lines = []
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, filename), "r", encoding="UTF-8") as doc:
        lines = doc.readlines()
        doc.close()

    # Table preprocessing
    TablesPreprocessor(log_level=2).preprocess(lines)
    
    print('\n'.join(lines[-10:]))


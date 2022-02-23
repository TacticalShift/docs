HTML_PAGE = '''<!DOCTYPE html>
<html>
    <head>
        {head}
    </head>
    <body>
        {body}
    </body>
</html>'''

HTML_HEAD = '''
    <meta charset="utf-8"/>
    <title>tS Docs - {title}</title>

    <link rel="icon" href="/docs/src/img/ts_icon.png">
    <link id="main-css" rel="stylesheet" href="/docs/src/style.css">

    <script src="/docs/src/keywords.js"></script>
    <script src="/docs/src/ruleEnum.js"></script>
    <script src="/docs/src/autocompleter.js"></script>
    <script src="/docs/src/searchWidget.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function () {{
            let url = new URL(window.location.href)
            if (url.protocol !== "file:") return
            let localCssPath = "src/style.css" 
			let urlPath = url.pathname.split("/")
            let rootPosition = urlPath.indexOf("docs")
			for (let i = rootPosition + 1; i < urlPath.length - 1; ++i) {{
				localCssPath = "../" + localCssPath
			}}
            document.getElementById("main-css").href = localCssPath
        }})
    </script>
'''

HTML_HEAD_SEARCH_PAGE = '''
    <meta charset="utf-8"/>
    <title>tS Docs - Поиск</title>

    <link rel="icon" href="/docs/src/img/ts_icon.png">
    <link rel="stylesheet" href="/docs/src/style.css">

    <script src="/docs/src/keywords.js"></script>
    <script src="/docs/src/ruleEnum.js"></script>
    <script src="/docs/src/autocompleter.js"></script>
    <script src="/docs/src/searchWidget.js"></script>
    <script src="/docs/src/search.js"></script>
'''

HTML_BODY = '''
    <div id="header">
        <div id="header-title">
            <span><a href="https://tacticalshift.ru" style="text-decoration: none; color: inherit;">tS</a></span> <tt id='header-sans'>Docs</tt>
        </div>
        {navbar}
    </div>
    <div id="wrapper">
        <div class="title"><h1>{title}</h1></div>
            {toc}
        <div class="article">
        {article}
        </div>
    </div>
'''

HTML_BODY_SEARCH_PAGE = '''
    <div id="header">
        <div id="header-title">
            <span><a href="https://tacticalshift.ru" style="text-decoration: none; color: inherit;">tS</a></span> <tt id='header-sans'>Docs</tt>
        </div>
        {navbar}
    </div>
    <div id="wrapper">
        <div class="title"><h1>Результат поиска: <small></small></h1></div>
        <div class="toc"></div>
        <div class="article"></div>
    </div>
'''

HTML_NAVBAR_SECTION = '''
    <div class="navbar">
        {dropdowns}

        <div id="search-bar">
            <input id="search-field" placeholder="Поиск по ключевым словам..."></input>
            <button id="search-button"><img src="/docs/src/img/search.png"></button>
        </div>
    </div>
'''

HTML_DROPDOWN_SECTION = '''
    <div class="dropdown">
        <button class="dropbtn" title="{tooltip}">{title}</button>
        <div class="dropdown-content">
          {elements}
        </div>
    </div>
'''

HTML_DROPDOWN_ELEMENT = '''<a href="{url}">{title}</a>'''

HTML_DROPDOWN_EXTENDED = '''
    <div class="dropdown-2l">
        <a href="{url}">{title}<arrow>⇨</arrow></a>
        <div class="dropdown-2l-content">
            {subpages}
        </div>
    </div>
'''

HTML_DROPDOWN_EXTENDED_INACTIVE = '''
    <div class="dropdown-2l">
        <span>{title}<arrow>⇨</arrow></span>
        <div class="dropdown-2l-content">
            {subpages}
        </div>
    </div>
'''



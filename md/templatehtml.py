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
		
	<link rel="icon" href="docs/src/img/ts_icon.png">
	<link rel="stylesheet" href="docs/src/style.css">
	<script src="https://code.jquery.com/jquery-3.4.1.min.js"
	integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo="
	crossorigin="anonymous"></script>
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

HTML_NAVBAR_SECTION = '''
	<div class="navbar">
		{dropdowns}
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

PAGE = '''<!DOCTYPE html>
<html>
    <head>
    {head}
    </head>
    <body>
    {body}
    </body>
</html>'''

PAGE_HEAD = '''
	<meta charset="utf-8" />

	<title>{title}</title>

	<link rel="icon" href="src/img/ts_icon.png">
	<link rel="stylesheet" href="src/style.css">
	<script src="https://code.jquery.com/jquery-3.4.1.min.js"
		integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
	<script src="MissionInfo.txt"></script>
	<script src="src/validator.js"></script>
	<script src="src/app.js"></script>
'''

PAGE_BODY = '''<body>
	<div id="header">
		<div id="header-title">
			<span><a href="https://tacticalshift.github.io" style="text-decoration: none; color: inherit;">tS</a></span>
			<tt id='header-sans'>Docs</tt>
		</div>

		<div class="navbar">
			{dropdowns}
		</div>
	</div>

	<div id="wrapper">

		<div class="title">
        <h1>{articletitle}</h1>
		</div>
        {toc}
		<div class="article">
		{body}
		</div>
	</div>

</body>

</html>
'''
TEMPLATE_DROPDOWN = '''
            <div class="dropdown">
				<button class="dropbtn">{section}</button>
				<div class="dropdown-content">
					{elements}
                    {level2}
				</div>
			</div>
'''
TEMPLATE_DROPDOWN_LEVEL2 = '''
                    <div class="dropdown-2l">
						<a href="{url}">{section}<span style="text-align:right">></a>
						<div class="dropdown-2l-content">
						{elements}	
						</div>
					</div>
'''
DROPDOWN_ELEMENT = '''<a href="{url}">{title}</a>'''

ELEMENT_URL = "./{filename}.html"

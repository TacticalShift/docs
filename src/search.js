
class FilterRule {
    constructor(keyword, rule, exclude) {
        console.log(`[FilterRule.constructor] Keyword [${keyword}], rule [${rule.name}], exclude: [${exclude}]`)

        this.keyword = keyword
        this.rule = rule
        this.exclude = exclude
    }
}

class Article {
    constructor(article, matched_keywords, missing_keywords) {
        this.title = article.title
        this.sections = article.section
        this.url = article.url
        this.matched = matched_keywords
        this.missed = missing_keywords
        this.displayName = `<small>${this.sections.join(" > ")} ></small> ${this.title}`
    }
}

const Searcher = {
    filterRules: [],
    invalidKeywords: [],
    query: "",
    LOG_LEVEL: 0,
    LOG: {
        INFO: 1,
        VERBOSE: 2
    },
    constants: {
        PAGE_TITLE: "tS Docs - Поиск: {query}",
        URL_FORMAT: "/docs/search.html?search={url}",
        TOC_SECTION: "<ol>{list}</ol>",
        TOC_LIST_ITEM: "<li><a href='{url}'>{title} ({count})</a></li>",
        TOC_LIST_INVALID_ITEM: "<li>{title} ✕</li>",
        RESULT_SECTION: "<ol class='search-result'>{results}</ol>",
        RESULT_ITEM: "<li><div class='search-result-header'><a href='{url}'>{title}</a></div><div class='search-result-info'>{keywords}</div></li>",
        RESULT_KEYWORD_MATCHED: "<span class='keyword-included'>✓ {keyword}</span>",
        RESULT_KEYWORD_MISSED: "<span class='keyword-excluded'>✕ {keyword}</span>"
    },

    log: function (lvl, msg) {
        if (lvl > this.LOG_LEVEL) return
        console.log(msg)
    },
    init: function (logLevel) {
        this.LOG_LEVEL = logLevel
    },
    search: function () {
        // Starts searchning process
        this.log(this.LOG.INFO, '[Searcher.search] Parsing request')
        this._parseRequest()

        this.log(this.LOG.INFO, '[Searcher.search] Rendering ToC')
        this._renderKeywordsList()

        this.log(this.LOG.INFO, '[Searcher.search] Rendering articles list')
        let articles = this._selectArticles()
        this._renderSearchResults(articles)
    },

    _parseRequest: function () {
        // Parses search request from URL parameter
        let url = new URL(window.location.href);
        let searchQuery = url.searchParams.get('search')
        this.log(this.LOG.VERBOSE, `[Searcher.parseRequest] URL: ${url}, query: ${searchQuery}, is null?: ${searchQuery == null}`)

        // Empty query
        if (searchQuery == null || searchQuery == "") {
            this.log(this.LOG.VERBOSE, `[Searcher.parseRequest] Empty query!`)
            this.query = ''
            return
        }

        this.query = searchQuery

        // Remove extra spaces
        searchQuery = searchQuery.trim()
            .replace(/\s{2,}/g, ' ')
            .replace(/\s*\|\s*/g, '|')

        this.log(this.LOG.VERBOSE, `[Searcher.parseRequest] Normalized query: ${searchQuery}`)

        // Parse query to set of rules
        let rules = []
        searchQuery.split(Rule.AND.syntax).forEach(el => {
            this.log(this.LOG.VERBOSE, `[Searcher.parseRequest] Unwrapped by AND: [${el}]`)
            unwrapped = el.split(Rule.OR.syntax)

            for (let i = 0; i < unwrapped.length; ++i) {
                this.log(this.LOG.VERBOSE, `[Searcher.parseRequest] Unwrapped by OR: [${unwrapped[i]}]`)
                rules.push(new FilterRule(
                    unwrapped[i].replace(Rule.NOT.syntax, ''),
                    i == 0 ? Rule.AND : Rule.OR,
                    unwrapped[i].startsWith(Rule.NOT.syntax)
                ))
            }
        })
        this.log(this.LOG.VERBOSE, `[Searcher.parseRequest] ${rules.length} keywords rules found`)

        rules.forEach(kword => {
            this.log(this.LOG.VERBOSE, `[Searcher.parseRequest] FilteRule params: ${kword.keyword}`)
            let valid_keywords = (Autocompleter.autocomplete(kword.keyword)).proposals

            if (valid_keywords.length === 0) {
                this.log(this.LOG.VERBOSE, `[Searcher.parseRequest] Invalid keyword. Skipping rule...`)
                this.invalidKeywords.push(kword.keyword)
                return;
            }

            let firstKeywordProcessed = false
            valid_keywords.forEach(el => {
                this.log(this.LOG.VERBOSE, `[Searcher.parseRequest] Valid keyword found: ${el}`)
                this.filterRules.push(new FilterRule(
                    el,
                    this.filterRules.length == 0 ? Rule.AND : firstKeywordProcessed ? Rule.OR : kword.rule,
                    kword.exclude
                ))
                if (!firstKeywordProcessed) { firstKeywordProcessed = true }
            })
        })
        this.log(this.LOG.VERBOSE, `[Searcher.parseRequest] ${this.filterRules.length} valid keywords rules found`)
    },
    _renderKeywordsList: function () {
        // Renders the keywords listing
        let listing = []
        if (this.query === '') {
            // Render ALL keywords when query is empty
            listing = Object.keys(KEYWORDS)
        } else {
            // Render only specific words if query defined
            this.filterRules.forEach(rule => {
                listing.push(rule.keyword)
            })
        }

        let html = this._formatKeywordList(listing, this.invalidKeywords)
        let toc_element = document.getElementsByClassName("toc")[0]
        toc_element.innerHTML = html
    },
    _formatKeywordList: function (keywordsListing, invalidKeywords) {
        // Format HTML list from keywords
        let html = []
        keywordsListing.forEach(kword => {
            let articlesCount = KEYWORDS[kword]
            let url = this.constants.URL_FORMAT.replace("{url}", kword)
            let toc_item = this.constants.TOC_LIST_ITEM.replace("{url}", url)
                .replace("{title}", kword)
                .replace("{count}", articlesCount)
            html.push(toc_item)
        })

        invalidKeywords.forEach(kword => {
            html.push(this.constants.TOC_LIST_INVALID_ITEM.replace("{title}", kword))
        })

        return this.constants.TOC_SECTION.replace("{list}", html.join("\n"))
    },

    _selectArticles: function () {
        // Return list of articles selected by keywords and filtered
        /*
                    A && B      Each el with both A and B (intersection of A and B)
                    A && !B     Each el with A but not B (excludes B from A)
                    A || B      Each el with A or B (sum of a + b)
                    A || !B     Each el with A or every article without B... 
                    !A          All except !A
        */

        let filteredArticles = []
        ARTICLES.forEach(artcl => {
            let match = true
            let matchedKeywords = []
            let missedKeywords = []
            this.filterRules.forEach(rule => {
                let keywordMatch = artcl.keywords.includes(rule.keyword)
                if (keywordMatch) {
                    matchedKeywords.push(rule.keyword)
                    this.log(this.LOG.VERBOSE, `[Searcher._selectArticles] Keyword match: ${rule.keyword}`)
                } else {
                    missedKeywords.push(rule.keyword)
                    this.log(this.LOG.VERBOSE, `[Searcher._selectArticles] Keyword missed: ${rule.keyword}`)
                }

                // Update article filter
                if (rule.rule == Rule.AND && !rule.exclude) {
                    match = match && keywordMatch
                } else if (rule.rule == Rule.AND && rule.exclude) {
                    match = match && !keywordMatch
                } else if (rule.rule == Rule.OR && !rule.exclude) {
                    match = match || keywordMatch
                } else if (rule.rule == Rule.OR && rule.exclude) {
                    match = match || !keywordMatch
                } else {
                    this.log(this.LOG.VERBOSE, `[Searcher._selectArticles] WTF? Rule: ${rule.rule}, ${rule.keyword} ; Article ${artcl.title}: ${artcl.keywords}`)
                }
            })

            this.log(this.LOG.VERBOSE, `[Searcher._selectArticles] Article: ${artcl.title}, keywords: ${artcl.keywords} => Matched: ${match}`)

            if (!match) return

            filteredArticles.push(new Article(artcl, matchedKeywords, missedKeywords))
        })

        this.log(this.LOG.INFO, `[Searcher._selectArticles] Selected ${filteredArticles.length} articles`)
        return filteredArticles
    },
    _renderSearchResults: function (articles) {
        // Renders results on the HTML page
        this.log(this.LOG.VERBOSE, `[Searcher._renderSearchResults] Rendering started for ${articles.length} articles`)
        let html = this._formatSearchResults(articles)
        let results_element = document.getElementsByClassName("search-result")[0]
        results_element.innerHTML = html
    },
    _formatSearchResults: function (articles) {
        // Formats found results into valid HTML
        this.log(this.LOG.VERBOSE, `[Searcher._formatSearchResults] Formating ${articles.length} articles`)

        let queryTitle = this.query === '' ? "(список статей)" : this.query
        // Update title
        document.title = this.constants.PAGE_TITLE.replace("{query}", queryTitle)

        // Update header
        let headerElement = document.getElementsByClassName("title")[0].getElementsByTagName("small")[0]
        headerElement.innerHTML = queryTitle

        // Update page content
        let html = []
        articles.forEach(article => {
            this.log(this.LOG.VERBOSE, article)
            let kwordLabels = [];
            article.matched.forEach(kword => {
                kwordLabels.push(this.constants.RESULT_KEYWORD_MATCHED.replace("{keyword}", kword))
            })
            article.missed.forEach(kword => {
                kwordLabels.push(this.constants.RESULT_KEYWORD_MISSED.replace("{keyword}", kword))
            })

            html.push(
                this.constants.RESULT_ITEM.replace("{url}", article.url)
                    .replace("{title}", article.displayName)
                    .replace("{keywords}", kwordLabels.join(" "))

            )
        })

        return this.constants.RESULT_SECTION.replace("{results}", html.join("\n"))
    }
}

document.addEventListener('DOMContentLoaded', function () {
    Searcher.init(Searcher.LOG.INFO)
    Searcher.search()
})

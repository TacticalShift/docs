const SearchWidget = {
    LOG: {
        INFO: 1,
        VERBOSE: 2,
    },
    constants: {
        URL: "/docs/search.html?search={query}",
        SEARCH_BAR: "search-bar",
        SEARCH_BUTTON: "search-button",
        SEARCH_FIELD: "search-field",
        AUTO_ID: "search-autocomplete",
        AUTO_ITEM_MATCH: "<strong>{str}</strong>",
        AUTO_ITEM_FOCUSED_CLASS: "autocomplete-item-focused",
        KEYS: {
            KEY_ENTER: 13,
            KEY_UP: 38,
            KEY_DOWN: 40,
            KEY_ESCAPE: 27
        }
    },
    searchBar: document.getElementById("search-bar"),
    searchButton: document.getElementById("search-button"),
    searchInput: document.getElementById("search-field"),
    proposalsMenu: {
        shown: false,
        focused: false,
		focusedByClick: false,
        focusedId: -1
    },

    log: function (lvl, msg) {
        if (lvl > this.LOG_LEVEL) return
        console.log(msg)
    },

    init: function (log_level) {
        this.LOG_LEVEL = log_level
        this.log(this.LOG.INFO, '[SearchWidget] Initialization started...')

        this.searchBar = document.getElementById(this.constants.SEARCH_BAR)
        this.searchButton = document.getElementById(this.constants.SEARCH_BUTTON)
        this.searchInput = document.getElementById(this.constants.SEARCH_FIELD)

        document.addEventListener("click", (e) => {
			if (SearchWidget.proposalsMenu.focusedByClick) {
				SearchWidget.proposalsMenu.focusedByClick = false
				return
			}
            SearchWidget.hideProposals()
        })
        this.searchInput.addEventListener('keyup', (e) => {
            SearchWidget.onKeyUp(e)
        })
		this.searchInput.addEventListener('focus', (e) => {
            SearchWidget.onInputClick(e)
        })
        this.searchButton.addEventListener('click', (e) => {
            SearchWidget.onButtonClick()
        })

        this.log(this.LOG.INFO, '[SearchWidget] Initialized!')
    },

    onButtonClick: function () {
        let query = this.getSearchQuery()
        let url = this.constants.URL.replace("{query}", encodeURI(query))
        window.open(url, "_self")
    },
	onInputClick: function(e) {		
		e.preventDefault()
		this.proposalsMenu.focusedByClick = true
		this.onQueryChange()
	},
    onKeyUp: function (e) {
        let key = e.keyCode
        this.log(this.LOG.VERBOSE, `[SearchWidget.onKeyUp] Key code ${key}`)

        if (key === this.constants.KEYS.KEY_ENTER) {
            e.preventDefault()
            if (this.proposalsMenu.focused) {
                this.selectProposal()
            } else {
                this.searchButton.click()
            }
			
        } else if (key === this.constants.KEYS.KEY_DOWN) {
            if (!this.proposalsMenu.shown) return
            this.focusOnProposal(++this.proposalsMenu.focusedId)

        } else if (key === this.constants.KEYS.KEY_UP) {
            if (!this.proposalsMenu.shown) return
            this.focusOnProposal(--this.proposalsMenu.focusedId)

        } else if (key == this.constants.KEYS.KEY_ESCAPE) {
            if (!this.proposalsMenu.shown) return
            e.preventDefault()
            this.hideProposals()

        } else {
            this.onQueryChange(true)
        }
    },
    onQueryChange: function (changeByKey = false) {
        let query = this.getSearchQuery()
        let autocomplete = Autocompleter.autocomplete(query)

        this.lastWord = autocomplete.word
        if (autocomplete.proposals.length > 10 || autocomplete.proposals.length === 0) {
            // Too much proposals - skip
            this.log(this.LOG.VERBOSE, '[SearchWidget.onQueryChange] Too much words/no words - skip')
            this.hideProposals()
            return
        }

        // Show autocompletion...
        this.log(this.LOG.VERBOSE, '[SearchWidget.onQueryChange] Showing proposals')
		if (changeByKey) this.hideProposals()
        this.showProposals(autocomplete.word, autocomplete.proposals)
    },
    getSearchQuery: function () {
        return this.searchInput.value
    },

    showProposals: function (word, proposals) {
        // this.hideProposals()

        let dropdown = document.createElement("div")
        dropdown.setAttribute("id", this.constants.AUTO_ID)
        this.searchBar.appendChild(dropdown)

        proposals.forEach(proposal => {
            let proposedPart = proposal.replace(word, '')

            let item = document.createElement("div")
            item.setAttribute("value", proposal)
            item.innerHTML = this.constants.AUTO_ITEM_MATCH.replace("{str}", word)
            item.innerHTML += proposedPart

            dropdown.appendChild(item)
			
            item.addEventListener("click", (e) => {
                SearchWidget.selectProposal(e.target)
            })
        })

        this.proposalsMenu.shown = true
    },
    hideProposals: function () {
        this.proposalsMenu.focused = false
		this.proposalsMenu.focusedByClick = false
        this.proposalsMenu.focusedId = -1
        this.proposalsMenu.shown = false

        let el = document.getElementById(this.constants.AUTO_ID)
        if (el === null) {
            return
        }
        el.remove()
    },
    getProposal: function (idx) {
        this.log(this.LOG.VERBOSE, `[SearchWidget.getProposal] By index ${idx}`)
        let items = document.getElementById(this.constants.AUTO_ID).getElementsByTagName("div")
        if (idx > items.length - 1) {
            idx = items.length - 1
            this.log(this.LOG.VERBOSE, `[SearchWidget.getProposal] Max index reached, correction = ${idx}`)
        } else if (idx < 0) {
            idx = 0
            this.log(this.LOG.VERBOSE, `[SearchWidget.getProposal] Min index reached, correction = ${idx}`)
        }
        this.proposalsMenu.focusedId = idx

        this.log(this.LOG.VERBOSE, `[SearchWidget.getProposal] Found ${items[idx]}\nItems: ${items}`)

        return {
            selected: items[idx],
            list: items
        }
    },
    focusOnProposal: function (idx) {
        this.proposalsMenu.focused = true
        let items = this.getProposal(idx)

        for (let i = 0; i < items.list.length; ++i) {
            items.list[i].removeAttribute("class")
        }
        items.selected.setAttribute("class", this.constants.AUTO_ITEM_FOCUSED_CLASS)
    },
    selectProposal: function (item) {		
        if (item == null) {
            item = this.getProposal(this.proposalsMenu.focusedId).selected
        } else {
			// When clicking on text itself - text node is passed in function
			// so we selecting parent
			if (!(item instanceof HTMLDivElement)) {
				item = item.parentElement
			}
		}
        let fullword = item.getAttribute("value")
        let currentValue = this.searchInput.value
        currentValue = currentValue.substring(0, currentValue.length - this.lastWord.length)

        this.searchInput.value = currentValue + fullword;

        this.hideProposals()
    }
}

document.addEventListener('DOMContentLoaded', function () {
    SearchWidget.init(SearchWidget.LOG.INFO)
})

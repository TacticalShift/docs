const Autocompleter = {
    keywords: Object.keys(KEYWORDS),

    autocomplete: function(text) {
        let words = this._split(text)
        let word = this._strip(words.pop())
        let proposals = []
        this.keywords.forEach(el => {
            if (el.startsWith(word) && !words.includes(el)) {
                proposals.push(el)
            }
        })

        return {
            word: word, 
            proposals: proposals
        }
    },
    _strip: function(text) {
        return text.trim()
                   .replace(Rule.NOT.syntax,"")
    },
    _split: function(text) {
        let words = text.replace(Rule.AND.syntax,",")
                        .replace(Rule.OR.syntax,",")
                        .split(",")
        return words
    }
}

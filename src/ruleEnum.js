class Rule {
    static AND = new Rule("and")
    static OR = new Rule("or")
    static NOT = new Rule("not")

    constructor(name) {
        this.name = name
        this.syntax = ''
        switch (name) {
            case "and": 
                this.syntax = " "
                break
            case "or":
                this.syntax = "|"
                break
            case "not":
                this.syntax = "!"
                break
        }
    }
}

SAMPLE_SCHEMA = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "glossary": {
      "type": "object",
      "properties": {
        "title": {
          "type": "string"
        },
        "GlossDiv": {
          "type": "object",
          "properties": {
            "title": {
              "type": "string"
            },
            "GlossList": {
              "type": "object",
              "properties": {
                "GlossEntry": {
                  "type": "object",
                  "properties": {
                    "ID": {
                      "type": "string"
                    },
                    "SortAs": {
                      "type": "string"
                    },
                    "GlossTerm": {
                      "type": "string"
                    },
                    "Acronym": {
                      "type": "string"
                    },
                    "Abbrev": {
                      "type": "string"
                    },
                    "GlossDef": {
                      "type": "object",
                      "properties": {
                        "para": {
                          "type": "string"
                        },
                        "GlossSeeAlso": {
                          "type": "array",
                          "items": {
                            "type": "string"
                          }
                        }
                      }
                    },
                    "GlossSee": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
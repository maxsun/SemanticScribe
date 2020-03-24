
# Text Tool
Goal: build a tool for quick & weak semantic analysis and transformation of text.

The tool is built on 3 main types:
1. `Data`: are ordered lists of symbols
2. `Token`: are typed sets of symbols, potentially tied to a location or region in the Data.
3. `Automata`: are algorithms which can be gradually applied to Data and return resulting Data.

## Automata
**Automata** are ordered structurings of Token Types, and definitions of other Automata, representing [algorithms](https://en.wikipedia.org/wiki/Algorithm).
When applied to Data and processed, Automata generate corresponding Data -- which is *informative* relative to the input Data.

Since Automata can generate more than one potential match, they are *ambiguous*.

## Queries
**Queries** are textual representations of Automata, which are interpreted into formal models.

1. **Order**: `Hello` corresponds to the symbols, in linear order, "Hello"
2. **Or**: `|` can be used to describe a union type:
3. **Grouping**
3. **Negation**
3. **Definition**: Types can be defined with `=`:
4. **Reference**: Types can then be used in patten matches: `$greeting Max` corresponds to "Hello", "Hi", or "Aloha Max".


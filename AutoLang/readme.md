
# Find-Transform Loop (FTL)

Information is the product of a transformation on data.
(Reducing its entropy relative to some interpretive context)

```python
Transform :: arg: Data, ctx: Data -> Data
```

A Transform is a mapping between pieces of data.
e.g. `to_caps("hello") => "HELLO"`

Transforms are carried out by **processes**, which are computation instances operating over computational resources such as Time & Space.

Principles:

1. Time over space
2. Practicality

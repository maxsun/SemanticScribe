# Resource Sensitivity

By definition, algorithms are composed of sequences of instructions.

Even in the purely metaphysical sense, algorithms have a corresponding *complexity*, which refers to the quantity of computational *resources*, such as time and space, required for running it. [^1]

Because of this, any algorithmic process must be sensitive to the resources available for its computation. For this reason, algorithmic processes are *resource-sensitive*.

Any complete representational model of algorithmic processes must account for resource-sensitivity.

This is pretty unsurprising, in most representations of algorithmic processes, we account for things like time and space. When we consider how a flower blooms, we don't consider it at a single moment in time, we consider its growth. Turing machines -- devices capable of computing algorithm any algorithm a human can -- operate over memory tapes (space) and states (time).

## In Language & Semantics

Any adequate model of language and semantics should provide tools for describing the words, their meanings, and relationships between them. Formally, let $\text{cat}$ represent the string of symbols "cat". Let $[\text{cat}]_C$ denote the meaning of the word "cat" in context C.

A common principle of formal models of language is *context-sensitivity*: the notion that an expression's meaning is determined relative to existing contextual information. The word "that" for example, has no real meaning without context. Formally, we might represent the context-sensitive meaning of a word:

$$
[\text{bridge}]\_\text{boat} \neq [\text{bridge}]_\text{cards}
$$

However, I believe that the context-sensitive nature of such models entails that the models also be sensitive to the availability of computational resources such as Time and Space. Consequently, any context-sensitive interpretation of a linguistic expression is subject to the resources spent on its interpretation.  Formally, let $[x]^{R}_{C}$ represent the meaning of the word $x$ relative to context $C$ after exhausting $R$ computational resources. The word "justice", for example, often becomes more meaningful and complex upon further consideration:

$$
[\text{justice}]^x_C > [\text{justice}]^y_C \iff x > y
$$


[^1]: *Time complexity* refers to the amount of time required to run an algorithm. Typically, "time" refers to the number of basic operations needed. *Space complexity* refers to the amount of memory space required to run an algorithm. "Space" is usually measured in terms of the number of bits needed.
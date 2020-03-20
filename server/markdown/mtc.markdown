

# Mathematical Theory of Communication (MTC)

The *Mathematical Theory of Communication* studies the quanitifable properties of information.
Created by Claude Shannon, MTC later became known as *information theory*, which is slightly misleading since Shannon's MTC is primarily concerned with syntactic, rather than semantic, information.

MTC treats information like a physical phenomena, deeply related to the thermodynamics notion of entropy.
Consequently, MTC is concerned with the data that makes up information, not necessarily the semantic content of information itself.
Because of this, MTC essentially analyzes information at the level of syntax.

Shannon's Noiseless and Discrete channel theorems explicate the limits of what can be transmit over a channel of communication.
(Like a phone system or radio signals)

MTC considers information in terms of Entropy ($H$), which is a measure of 3 equivalent quanities:
1. the average information per produced symbol produced by the informer
2. the average uncertainty (or data deficit) of the informee before recieving data
3. the information potentionality of the information source

Generally, Entropy is a measurement of how random or "mixed-up" an information-bearing system is.
Entropy can be considered an indicator of reversibility; if a process has no effect on entropy, then it can be reversed.
Entropy peaks in the case of a uniform distribution; a glass of water contains more entropy than a glass of ice.

### Shannon's Fundamental Theorem of the Noiseless Channel:
Let a source have entropy $H$ (bits per symbol) and a channel have a capacity $C$ (bits per second).
Then it is possible to encode the output of the source in such a way as to transmit at the average rate of $C/H−\epsilon$ symbols per second over the channel where $\epsilon$ is arbitrarily small.
It is not possible to transmit at an average rate greater than $C/H$.
(Shannon and Weaver [1949], 59) 

### Shannon's Fundamental Theorem for a Discrete Channel:
Let a discrete channel have the capacity $C$ and a discrete source the entropy per second $H$.
If $H \leq C$ there exists a coding system such that the output of the source can be transmitted over the channel with an arbitrarily small frequency of errors (or an arbitrarily small equivocation).
If $H > C$ it is possible to encode the source so that the equivocation is less than $H−C+\epsilon$ where $\epsilon$ is arbitrarily small.
There is no method of encoding which gives an equivocation less than $H−C$.
(Shannon and Weaver [1949], 71)

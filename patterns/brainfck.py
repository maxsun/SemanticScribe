'''
A Description of Brainfuck Interpretation in SpEx

> = moves the pointer to the right 1 block.
< = moves the pointer to the left 1 block.
+ = increases value stored at the block pointed to
- = decreases value stored at the block pointed to
[ = like c while(cur_block_value != 0) loop.
] = if block currently pointed to's value is not zero, jump back to [
, = like c getchar(). input 1 character.
. = like c putchar(). print 1 character to the console
'''
import spex_automata as A
import spex as P
import re

code_text = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'

# 1. Describe the Context Space, in this case, a Memory Tape
# memory is a string of textS

memory_text = ' '.join(['%s: 0' % i for i in range(250)])
print(memory_text)
memory_pats = {
    'value': re.compile(r'\d+')
}

memory = A.Ruleset('memory')
memory.add_instance('v', 'value')
memory.add_instance
 
pointer_index_text = ('0')
pointer_pats = {
    'value': re.compile(r'\d+')
}

# things are tokenized by index (maybe split by spaces)
# its a string of numbers spaced apart.
# the Nth number = the value of the block pointed to at index N.

# 2. First-pass Tokenize the code

reg_pats = {
    'right': re.compile(r'>'),
    'left': re.compile(r'<'),
    'plus': re.compile(r'\+'),
    'minus': re.compile(r'\-'),
    'open_b': re.compile(r'\['),
    'close_b': re.compile(r'\]'),
    'comma': re.compile(r','),
    'period': re.compile(r'\.'),
}

# 3. Describe the Semantics of the Code

# + = memory value # (pointer_index) += 1

# Pointer.find(context) = the value being pointed to
# PointerValue.find(context) = the value of the pointer



# 4. Higher-order Tokenization + Queries


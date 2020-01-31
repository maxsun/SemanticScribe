import os
from pprint import pprint
from itertools import chain

from flask import Flask, jsonify, render_template
from flask_cors import CORS

from lark import tree as larkTree
from networkx.drawing.nx_agraph import graphviz_layout, to_agraph

from lark import Lark, Token, Transformer, Tree
from lark.indenter import Indenter

NOTES_FOLDER = './note_files/'

GRAMMAR = open('./grammar.lark').read()

class TreeIndenter(Indenter):
    """A lexical processor for indentation"""
    NL_type = '_NL'
    OPEN_PAREN_types = ["OPEN_REF"]
    CLOSE_PAREN_types = ["CLOSE_REF"]
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8


class TreeTransformer(Transformer):
    """Pos-processing to modify the lark generated tree"""
    @staticmethod
    def text(items):
        """Join words under text nodes in the AST"""
        return Token('TXT', ' '.join(items))

    @staticmethod
    def reference(items):
        """Join words under reference nodes in the AST"""
        return Token('REF', ' '.join(items))

NOTES_FOLDER = './note_files/'

GRAMMAR = open('./grammar.lark').read()

class TreeIndenter(Indenter):
    """A lexical processor for indentation"""
    NL_type = '_NL'
    OPEN_PAREN_types = ["OPEN_REF"]
    CLOSE_PAREN_types = ["CLOSE_REF"]
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8


class TreeTransformer(Transformer):
    """Pos-processing to modify the lark generated tree"""
    @staticmethod
    def text(items):
        """Join words under text nodes in the AST"""
        return Token('TXT', ' '.join(items))

    @staticmethod
    def reference(items):
        """Join words under reference nodes in the AST"""
        return Token('REF', ' '.join(items))

PARSER = Lark(
    GRAMMAR,
    parser='lalr',
    postlex=TreeIndenter(),
    transformer=TreeTransformer)


def ast_from_text(text):
    """Parse text into an array of block ASTs"""
    return PARSER.parse(text)

ast = ast_from_text('''
- [[Max]] is 20 years old
- Hello [[World]]
  - Hola [[World]]
  - Ni Hao [[World]]
- Goodbye [[Moon]]
- [[World]]
  - also called Earth
  - Has a [[Moon]]
- the [[Moon]] orbits the [[World]]
''')

all_blocks = list(ast.find_data('block'))

id_to_block = {}
block_to_id = {}
for i, block in enumerate(all_blocks):
    _id = str(i)
    id_to_block[_id] = block
    block_to_id[block] = _id

all_blocks = list(ast.find_data('block'))          

# get blocks containing a reference with <value>
def get_blocks_with_ref(value, blocks):
    results = []
    for block in blocks:
        for token in block.children[0].children:
            if token.type == 'REF' and token.value == value:
                results.append(block)
    return results

# add artificial blocks
all_refs = set([])
for block in all_blocks:
    for token in block.children[0].children:
        if token.type == 'REF':
            all_refs.add(token)

for ref in all_refs:
    bs = get_blocks_with_ref(ref, all_blocks)
    if len([x for x in bs if len(x.children[0].children) == 1]) == 0:
        print('filler block', ref)
        t = Tree('block', [
            Tree('content', [ref]),
            Tree('blocks', [])
        ])
        all_blocks.append(t)

# assign IDs to each block
id_to_block = {}
block_to_id = {}
for i, block in enumerate(all_blocks):
    _id = str(i)
    id_to_block[_id] = block
    block_to_id[block] = _id

# Get immediate children blocks of <parent> block
def get_immediate_children(parent):
    return list(parent.children[1].children)

# get immediate parent block of <child> block
def get_immediate_parent(child, blocks):
    for block in blocks:
        if child in block.children[1].children:
            return block

def token_to_json(token):
    data = None
    if token.type == 'REF':
        data = ref_to_id(token.value, all_blocks)
    return {
        'type': token.type,
        'value': token.value,
        'data': data
    }

def block_to_json(block):
    return {
        'content': [token_to_json(x) for x in block.children[0].children],
        'children': [block_to_json(x) for x in block.children[1].children],
        'id': block_to_id[block]
    }

def block_by_id(id):
    block = id_to_block[id]
    return block_to_json(block)

def occurences_by_id(id, blocks):
    block = id_to_block[id]        
    parent = get_immediate_parent(block, blocks)
    refs = get_blocks_with_ref(id, blocks)
    if len(block.children[0].children) == 1 and block.children[0].children[0].type == 'REF':
        refs += get_blocks_with_ref(block.children[0].children[0].value, blocks)
    results = refs + [parent]
    return [x for x in results if x is not None]

def ref_to_id(ref, blocks):
    occurences = get_blocks_with_ref(ref, blocks)
    for blk in blocks:
        if len(blk.children[0].children) == 1 and blk.children[0].children[0].type == 'REF' and blk.children[0].children[0].value == ref:
            return block_to_id[blk]
    print('>>', ref)


app = Flask(__name__, static_folder="./webclient/dist/", template_folder='./webclient/dist')
CORS(app)

@app.route('/')
def index():
    # return jsonify(parse_notefiles('./note_files/').to_dict())
    return render_template('index.html')

@app.route('/b/<id>')
def block_by_id(id):
    block = id_to_block[id]
    return jsonify(block_to_json(block))

@app.route('/o/<id>')
def occ(id):
    results = occurences_by_id(id, all_blocks)
    return jsonify([block_to_json(x) for x in results])

@app.route('/r/<ref>')
def ref_to_id_route(ref):
    return block_by_id(ref_to_id(ref, all_blocks))


app.run(debug=True)

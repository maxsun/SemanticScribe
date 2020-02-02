from flask import Flask, jsonify, render_template
from flask_cors import CORS
import functional_parser as parser
import re


app = Flask(__name__, static_folder="./webclient/dist/", template_folder='./webclient/dist')
CORS(app)

ALL_LINKS = {
    'references': parser.resolve_block_references,
    'children': parser.resolve_immediate_children
}

BLOCKS = parser.parse(re.split(r'(\s*\-.*\n)', '''
- [[G.W.]]
    - crossed the Delaware
    - was the first [[President]]
    - led the [[American Revolution]]
- [[President]]
    - the highest ranking American government position
    - **not** a king!
        - America was founded to escape monarchy/tyranny
- The [[American Revolution]] began in 1765
    - the [[War]] didn't start until 1775 though
'''))

id_to_block = {}
for b in BLOCKS:
    id_to_block[b.id] = b


@app.route('/r/<ref_value>')
def block_by_ref(ref_value):
    return jsonify(parser.resolve_reference(ref_value, BLOCKS))


@app.route('/out/<id>')
def block_out(id):
    blk = id_to_block[id]
    return jsonify(parser.get_links_out(blk, BLOCKS, ALL_LINKS))


@app.route('/in/<id>')
def block_in(id):
    blk = id_to_block[id]
    return jsonify(parser.get_links_in(blk, BLOCKS, ALL_LINKS))


app.run(debug=True)

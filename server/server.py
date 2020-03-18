from flask import Flask, jsonify, render_template
from flask_cors import CORS
import parser as parser
import re

from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__, static_folder="./webclient/dist/", template_folder='./webclient/dist')
CORS(app)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


@app.route('/r/<ref_value>')
def block_by_ref(ref_value):
    return jsonify(parser.resolve_reference(ref_value, parser.BLOCKS))


@app.route('/i/<id>')
def block_by_id(id):
    return jsonify(parser.block_by_id(id))


@app.route('/out/<id>')
def block_out(id):
    blk = parser.block_by_id(id)
    return jsonify(parser.get_links_out(blk, parser.BLOCKS, parser.ALL_LINKS))


@app.route('/in/<id>')
def block_in(id):
    blk = parser.block_by_id(id)
    return jsonify(parser.get_links_in(blk, parser.BLOCKS, parser.ALL_LINKS))


def build_tree(id, depth=2):
    blk = parser.block_by_id(id)
    nxt = []
    if depth > 0:
        nxt = [build_tree(x.id, depth - 1) for x in parser.resolve_immediate_children(blk, parser.BLOCKS)]
    return {
        'data': blk,
        'next': nxt,
    }

@app.route('/g/<id>/<depth>')
def tree_by_id(id, depth=2):
    return jsonify(build_tree(id, int(depth)))
    # return jsonify(parser.get_links_in(blk, BLOCKS, ALL_LINKS))


app.run(debug=True)

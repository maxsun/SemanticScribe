from flask import Flask, jsonify, render_template
from flask_cors import CORS
import re
import markdown

from spex_types import *

app = Flask(__name__, static_folder='./static', template_folder='./templates')
CORS(app)

CORS(app)


def plaintext_tokenize(text: str) -> Data:
    return [Token('plaintext', text, Range(0, len(text)))]


def read(filename) -> Data:
    text = open('./markdown/' + filename + '.markdown').read()
    return plaintext_tokenize(text)


@app.route('/read/<filename>')
def read_route(filename):
    return jsonify([x._asdict() for x in read(filename)])


@app.route('/')
def index():
    md = open('./markdown/mtc.markdown').read()
    html = markdown.markdown(md, extensions=['fenced_code', 'codehilite', 'footnotes'])
    return render_template('page.html', content=html)


app.run(debug=True)

from flask import Flask, jsonify, render_template
from parser import parse_notefiles
from flask_cors import CORS

app = Flask(__name__, static_folder="./infopanel/dist/", template_folder='./infopanel/dist')
CORS(app)

@app.route('/')
def hello_world():
    # return jsonify(parse_notefiles('./note_files/').to_dict())
    return render_template('index.html')

@app.route('/r/<ref>')
def get_ref(ref):
    ref = ref.replace('.', '/') # quick hack to allow paths in url- change this!
    data = parse_notefiles('./note_files/')
    data = data.resolve_ref_block(ref)
    return jsonify(data.to_dict(path=ref))

@app.route('/o/<ref>')
def ref_occurences(ref):
    ref = ref.replace('.', '/') # quick hack to allow paths in url- change this!
    print(ref)
    data = parse_notefiles('./note_files/')
    data = data.get_by_ref(ref, recursive=True)
    return jsonify([x.to_dict() for x in data])


app.run(debug=True)

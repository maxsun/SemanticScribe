from flask import Flask, jsonify, render_template
from parser import parse_notefiles
from flask_cors import CORS

app = Flask(__name__, static_folder="./webclient/dist/", template_folder='./webclient/dist')
CORS(app)

@app.route('/')
def index():
    # return jsonify(parse_notefiles('./note_files/').to_dict())
    return render_template('index.html')

@app.route('/r/<ref>')
def get_ref(ref):
    ref = ref.replace('.', '/') # quick hack to allow paths in url- change this!
    data = parse_notefiles('./note_files/')
    data = data.get_by_path(ref)
    return jsonify(data.to_dict(path=ref))

@app.route('/o/<ref>')
def ref_occurences(ref):
    ref = ref.replace('.', '/') # quick hack to allow paths in url- change this!
    data = parse_notefiles('./note_files/')
    data = data.get_by_ref(ref, recursive=True)
    print(data)
    return jsonify([x.to_dict() for i, x in enumerate(data)])


app.run(debug=True)

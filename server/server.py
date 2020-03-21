from flask import Flask, jsonify, render_template
from flask_cors import CORS
import parser as parser
import re
import markdown

# from flask_graphql import GraphQLView
# from schema import schema

app = Flask(__name__, static_folder='./static', template_folder='./templates')
CORS(app)

# app.astatic_folder="./", ate_folder='./templates')
CORS(app)

# app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

# app.add_url_rule('/favicon.ico',
#                  redirect_to=url_for('static', filename='favicon.ico'))


@app.route('/')
def index():
    md = open('./markdown/mtc.markdown').read()
    html = markdown.markdown(md, extensions=['fenced_code', 'codehilite', 'footnotes'])
    return render_template('page.html', content=html)


app.run(debug=True)

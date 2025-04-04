from flask import Flask, request, jsonify
from main import option_chain
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='*')

@app.route("/option_chain")
def get_option_chain():
    name = request.args.get("index")
    response = option_chain(name)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)

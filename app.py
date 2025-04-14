from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])

def hello():
    return jsonify({"message": "Hello, world!"})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, request, jsonify
from model import get_recommendation

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Receive JSON data
    result = get_recommendation(data)  # Get recommendation from model
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

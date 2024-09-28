from flask import Flask, request, jsonify
from model import get_recommendation

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    user_id = data.get('user_id')

    # Ensure user_id is an integer
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "Invalid user ID"}), 400

    # Get recommendation from the model
    recommendations = get_recommendation(user_id)

    return jsonify({"recommendations": recommendations})

if __name__ == '__main__':
    app.run(debug=True)

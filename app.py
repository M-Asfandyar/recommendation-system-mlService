from flask import Flask, request, jsonify
from model import get_recommendation  # Import the recommendation model logic

app = Flask(__name__)

# Feedback storage (in-memory for now)
feedback_data = []

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "No user ID provided"}), 400

    try:
        # Log the received user ID
        print(f"Received user_id: {user_id}")

        # Get recommendations from the model (pass only user_id, feedback handled internally)
        recommendations = get_recommendation(user_id)  # Pass only user_id
        
        # Log the generated recommendations
        print(f"Generated recommendations for user_id {user_id}: {recommendations}")
        
        return jsonify({"recommendations": recommendations})
    except Exception as e:
        # Log the exact error message
        print(f"Error generating recommendations: {str(e)}")
        return jsonify({"error": "Error generating recommendations"}), 500

# Add the /feedback route to handle feedback
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    user_id = data.get('user_id')
    feedback = data.get('feedback')

    if not user_id or not feedback:
        return jsonify({"error": "Missing user_id or feedback"}), 400

    try:
        # Log the received feedback
        print(f"Received feedback for user_id {user_id}: {feedback}")

        # Store feedback in-memory (could be stored in a database)
        feedback_data.append({'user_id': user_id, 'feedback': feedback})
        
        # Log the current state of the feedback_data
        print(f"Updated feedback_data: {feedback_data}")
        
        return jsonify({"message": "Feedback received"}), 200
    except Exception as e:
        # Log the exact error message
        print(f"Error processing feedback: {str(e)}")
        return jsonify({"error": "Error processing feedback"}), 500

if __name__ == '__main__':
    app.run(debug=True)

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Sample user interaction data
data = {
    'user_id': [1, 1, 1, 2, 2, 3, 3, 4],
    'content_id': [101, 102, 103, 101, 104, 102, 105, 103],
    'interaction': [5, 3, 2, 4, 1, 5, 4, 2]
}

# Create a DataFrame to represent the data
df = pd.DataFrame(data)

# Feedback storage
feedback_data = []

# Recommendation logic based on user similarity
def get_recommendation(user_id):
    # Create a user-content interaction matrix
    user_content_matrix = df.pivot_table(index='user_id', columns='content_id', values='interaction').fillna(0)

    # Check if the user exists in the matrix
    if user_id not in user_content_matrix.index:
        print(f"User ID {user_id} not found in data")
        return []

    # Calculate similarity between users using cosine similarity
    user_similarity = cosine_similarity(user_content_matrix)

    # Create a DataFrame of the similarities
    similarity_df = pd.DataFrame(user_similarity, index=user_content_matrix.index, columns=user_content_matrix.index)

    try:
        # Get the most similar user to the given user
        most_similar_user = similarity_df[user_id].sort_values(ascending=False).index[1]
        print(f"Most similar user to {user_id}: {most_similar_user}")

        # Get the data of the most similar user and the target user
        user_data = user_content_matrix.loc[user_id]
        similar_user_data = user_content_matrix.loc[most_similar_user]

        # Adjust recommendations based on feedback
        global feedback_data
        for feedback in feedback_data:
            if feedback['user_id'] == user_id and feedback['feedback'] == 'no':
                # If the user disliked the recommendation, reduce its weight
                similar_user_data = similar_user_data * 0.5

        # Recommend content that the user hasn't interacted with
        recommendations = similar_user_data[user_data == 0].sort_values(ascending=False)

        # Return the recommended content IDs
        return recommendations.index.tolist()

    except Exception as e:
        print(f"Error generating recommendations: {str(e)}")
        return []

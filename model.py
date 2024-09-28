import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Sample user interaction data
data = {
    'user_id': [1, 1, 1, 2, 2, 3, 3, 4],
    'content_id': [101, 102, 103, 101, 104, 102, 105, 103],
    'interaction': [5, 3, 2, 4, 1, 5, 4, 2]
}

df = pd.DataFrame(data)

def get_recommendation(user_id):
    # Create a user-content matrix
    user_content_matrix = df.pivot_table(index='user_id', columns='content_id', values='interaction').fillna(0)

    # Check if the user exists in the matrix
    if user_id not in user_content_matrix.index:
        return []

    # Calculate similarity between users using cosine similarity
    user_similarity = cosine_similarity(user_content_matrix)

    # Create a DataFrame of the similarities
    similarity_df = pd.DataFrame(user_similarity, index=user_content_matrix.index, columns=user_content_matrix.index)

    # Get the most similar user to the given user
    most_similar_user = similarity_df[user_id].sort_values(ascending=False).index[1]

    # Find content the similar user has interacted with but the given user has not
    user_data = user_content_matrix.loc[user_id]
    similar_user_data = user_content_matrix.loc[most_similar_user]

    recommendations = similar_user_data[user_data == 0].sort_values(ascending=False)

    return recommendations.index.tolist()  # Return the recommended content IDs

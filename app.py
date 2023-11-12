import os
import numpy as np
from flask import Flask, render_template, request, jsonify, send_from_directory
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["bot_db"]
collection = db["bot_data"]

vectorizer = TfidfVectorizer()


# Function to retrieve content from MongoDB
def get_content_from_mongodb():
    documents = collection.find()
    content_list = [doc["content"] for doc in documents]
    return content_list


# TF-IDF Vectorization
def vectorize_text(text_list):
    vectors = vectorizer.fit_transform(text_list)
    return vectors


# Function to get the most similar document based on user query
def get_most_similar_document(query, vectors, text_list):
    query_vector = vectorizer.transform([query])
    similarity_scores = cosine_similarity(query_vector, vectors)
    most_similar_index = similarity_scores.argmax()

    # Additional logging
    predicted_answer = text_list[most_similar_index]
    confidence_score = np.max(similarity_scores)

    print(f"User Query: {query}")
    print(f"Predicted Answer: {predicted_answer}")
    print(f"Confidence Score: {confidence_score}")

    return predicted_answer


# Serve static files (images in this case)
@app.route('/static/<path:filename>')
def static_files(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), filename)


# Endpoint for the main chat page
@app.route('/')
def chat():
    return render_template('chat.html')


# Endpoint for question answering
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    user_query = data['question']

    content_list = get_content_from_mongodb()
    vectors = vectorize_text(content_list)

    answer = get_most_similar_document(user_query, vectors, content_list)

    return jsonify({'answer': answer})


if __name__ == '__main__':
    app.run(debug=True)

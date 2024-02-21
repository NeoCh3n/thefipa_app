from flask import Flask, request, jsonify
import joblib
import pandas as pd
from pymongo import MongoClient
import os


app = Flask(__name__)

# MongoDB setup
mongo_uri = os.environ.get('MONGO_URI')  # Replace with your actual MongoDB URI
client = MongoClient(mongo_uri)
db = client['cat_blood_tests']  # Replace 'cat_blood_tests' with your actual database name
collection = db['tests']  # Replace 'tests' with your actual collection name

# Define the column names globally
columns = [
    "RBC", "HCT", "HGB", "MCV", "MCH", "MCHC", "RDW", "RETIC", "Rchem", "WBC", 
    "NEU", "LYM", "MONO", "EOS", "BASO", "PLT", "MPV", "PCT", "GLU", "CREA", 
    "BUN", "PHOS", "CA", "TP", "ALB", "GLOB", "ALT", "ALKP", "GGT", "TBIL", 
    "CHOL", "AMYL", "LIPA", "Na", "K", "CL"
]

# Load the model only once when the application starts
model = joblib.load('/Users/chaoyanchen/Desktop/FIP Case Study/thefipa_app/rf_model.joblib')  # Update the path to your model

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data sent to the endpoint
        data_received = request.get_json(force=True)
        
        # Extract the input data
        input_data = data_received.get("input")
        
        # Convert input data into DataFrame or the required format for your model
        df = pd.DataFrame([input_data], columns=columns)
        
        # Make prediction
        prediction = model.predict(df)
        
        # Store input data and prediction result in MongoDB
        data_received['prediction'] = prediction.tolist()
        collection.insert_one(data_received)
        
        # Return prediction as JSON
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Define the column names globally
columns = [
    "RBC", "HCT", "HGB", "MCV", "MCH", "MCHC", "RDW", "RETIC", "Rchem", "WBC", 
    "NEU", "LYM", "MONO", "EOS", "BASO", "PLT", "MPV", "PCT", "GLU", "CREA", 
    "BUN", "PHOS", "CA", "TP", "ALB", "GLOB", "ALT", "ALKP", "GGT", "TBIL", 
    "CHOL", "AMYL", "LIPA", "Na", "K", "CL"
]

# Load the model only once when the application starts
model = joblib.load('/Users/chaoyanchen/Desktop/FIP Case Study/thefipa_app/rf_model.joblib')

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
        
        # Return prediction as JSON
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

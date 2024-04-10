from flask import Flask, request, jsonify
import joblib
import pandas as pd
from pymongo import MongoClient
import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False


# Assuming the model is in the same directory as this script
model_path = os.path.join(os.path.dirname(__file__), 'rf_model.joblib')

# MongoDB setup
mongo_uri = os.environ.get('MONGO_URI')  # Ensure this environment variable is set in your Azure environment
client = MongoClient(mongo_uri)
db = client['CatDB']  # Accessing the CatDB database
collection = db['bloodtest']  # Accessing the bloodtest collection

# Define the column names globally
columns = [
    "RBC", "HCT", "HGB", "MCV", "MCH", "MCHC", "RDW", "RETIC", "Rchem", "WBC", 
    "NEU", "LYM", "MONO", "EOS", "BASO", "PLT", "MPV", "PCT", "GLU", "CREA", 
    "BUN", "PHOS", "CA", "TP", "ALB", "GLOB", "ALT", "ALKP", "GGT", "TBIL", 
    "CHOL", "AMYL", "LIPA", "Na", "K", "CL"
]

# Load the model only once when the application starts
model = joblib.load(model_path)  # Load the model

@app.before_first_request
def insert_test_data():
    test_data = {
        "input": ["0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2"],
        "prediction": 1
    }
    collection.insert_one(test_data)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data sent to the endpoint
        data_received = request.get_json(force=True)
        
        # Extract the input data
        input_data_raw = data_received.get("input")
        
        # Convert input data into a list of integers
        input_data = [int(item) for item in input_data_raw]
        
        # Convert input data into DataFrame or the required format for your model
        df = pd.DataFrame([input_data], columns=columns)
        
        # Make prediction
        prediction = model.predict(df)
        
        # Store input data and prediction result in MongoDB
        result_to_store = {"input": input_data_raw, "prediction": int(prediction[0])}  # Store raw input and prediction
        collection.insert_one(result_to_store)
        
        # Return prediction as JSON
        return jsonify({'prediction': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test_db')
def test_db():
    try:
        # 查询测试数据
        test_data = collection.find_one({"prediction": 1})
        if test_data:
            return jsonify({"message": "Database connection successful", "data": test_data})
        else:
            return jsonify({"message": "Test data not found"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test_model', methods=['POST'])
def test_model():
    try:
        # 准备测试数据
        test_input = ["0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2", "0", "1", "2"]
        
        # 调用预测函数
        response = predict_helper(test_input)
        
        return jsonify({"message": "Model prediction successful", "response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def predict_helper(input_data):
    # 将输入数据转换为整数列表
    input_data = [int(item) for item in input_data]
    
    # 将输入数据转换为 DataFrame 或模型所需的格式
    df = pd.DataFrame([input_data], columns=columns)
    
    # 进行预测
    prediction = model.predict(df)
    
    return int(prediction[0])

if __name__ == '__main__':
    app.run(debug=True)
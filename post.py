import requests

# Provided input data directly as a list in the expected order
input_data = [1,1,1,1,1,1,2,1,1,1,2,1,1,0,0,0,2,0,1,1,0,1,1,2,1,2,1,1,1,2,1,1,1,0,1,0]

# Prepare the data for the Flask app
data_to_send = {"input": input_data}

# The URL to your Flask application's predict endpoint
url = "http://127.0.0.1:5000/predict"

# Send POST request to Flask app
response = requests.post(url, json=data_to_send)

# Check if the request was successful
if response.status_code == 200:
    # Print the response from Flask app
    print(response.json())
else:
    print(f"Error {response.status_code}: {response.text}")

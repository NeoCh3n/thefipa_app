import pandas as pd
import joblib

# Provided input data in the correct format
input_data = [1,1,1,1,1,1,2,1,1,1,2,1,1,0,0,0,2,0,1,1,0,1,1,2,1,2,1,1,1,2,1,1,1,0,1,0]

# Assuming the column names based on your first message
columns = [
    "RBC", "HCT", "HGB", "MCV", "MCH", "MCHC", "RDW", "RETIC", "Rchem", "WBC", 
    "NEU", "LYM", "MONO", "EOS", "BASO", "PLT", "MPV", "PCT", "GLU", "CREA", 
    "BUN", "PHOS", "CA", "TP", "ALB", "GLOB", "ALT", "ALKP", "GGT", "TBIL", 
    "CHOL", "AMYL", "LIPA", "Na", "K", "CL"
]

# Convert the list of input data into a DataFrame with appropriate column names
df = pd.DataFrame([input_data], columns=columns)

# Output the DataFrame to a CSV file if needed
df.to_csv('/Users/chaoyanchen/Desktop/FIP Case Study/thefipa_app/data.csv', index=False)

# Load the model from the file
rf_model = joblib.load('/Users/chaoyanchen/Desktop/FIP Case Study/thefipa_app/rf_model.joblib')

# Use the model for prediction
prediction = rf_model.predict(df)

# Print the prediction
print(f"The prediction is: {prediction}")

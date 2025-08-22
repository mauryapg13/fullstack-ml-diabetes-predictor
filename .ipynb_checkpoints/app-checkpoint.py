from flask import Flask, request, jsonify 
import joblib
import pandas as pd
import numpy as np

# --- Load the Trained Machine Learning Pipeline ---
pipeline_path = 'diabetes_pipeline.joblib'
loaded_pipeline = joblib.load(pipeline_path)
print(f"Model pipeline from '{pipeline_path}' loaded successfully.")

# --- Create the Flask App Instance ---
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    # This function is executed when someone navigates to the base URL (e.g., http://127.0.0.1:5000)
    # It provides a simple welcome message and confirms the API is running.
    return jsonify({
        "message": "Welcome to the Diabetes Prediction API!",
        "description": "This is a machine learning service to predict the likelihood of diabetes.",
        "endpoints": {
            "/predict": {
                "method": "POST",
                "description": "Send patient data in JSON format to get a prediction.",
                "example_payload": {
                    "Pregnancies": 6,
                    "Glucose": 148,
                    "BloodPressure": 72,
                    "SkinThickness": 35,
                    "Insulin": 0,
                    "BMI": 33.6,
                    "DiabetesPedigreeFunction": 0.627,
                    "Age": 50
                }
            }
        }
    })

    
# --- Define API Endpoints ---
@app.route('/predict', methods=['POST'])
def predict():
    # ... (code to get and process data remains the same) ...
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No JSON data received"}), 400

        input_df = pd.DataFrame([data])
        
        prediction = loaded_pipeline.predict(input_df)
        prediction_probabilities = loaded_pipeline.predict_proba(input_df)

    except Exception as e:
        return jsonify({"error": f"Error during prediction: {e}"}), 400

    final_prediction_class = int(prediction[0])
    probabilities = prediction_probabilities[0]

    final_prediction_label = 'Diabetic' if final_prediction_class == 1 else 'Non-Diabetic'

    response_data = {
        "prediction_class": final_prediction_class,
        "prediction_label": prediction_label,
        "confidence_scores": {
            "Non-Diabetic": float(probabilities[0]),
            "Diabetic": float(probabilities[1])
        }
    }
    print(f"Sending response: {response_data}")

    # --- Return the JSON response using jsonify ---
    # The jsonify function handles the conversion to a JSON string and sets the
    # appropriate Content-Type header to 'application/json'.
    return jsonify(response_data)
    
if __name__ == '__main__':
    # app.run() starts the Flask development web server.
    # debug=True enables debug mode, which provides helpful error messages and automatically
    # reloads the server when you make changes to the code. This is great for development.
    app.run(debug=True)
    
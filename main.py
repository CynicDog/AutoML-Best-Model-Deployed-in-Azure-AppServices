import os
import logging
import json
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)
model = None

# Define column names that match the training data
COLUMN_NAMES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

def init():
    global model
    # Set the model path to the current directory
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    model = joblib.load(model_path)
    logging.info("Model initialized successfully.")


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'


# Endpoint for predictions
@app.route('/predict', methods=['POST'])
def predict():
    global model
    if model is None:
        return jsonify({"error": "Model is not initialized."}), 500

    try:
        # Parse and format data with column names
        raw_data = request.data
        data = json.loads(raw_data)["data"]
        data_df = pd.DataFrame(data, columns=COLUMN_NAMES)

        # Predict and return the result
        result = model.predict(data_df)

        return jsonify({"predictions": result.tolist()})

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    init()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

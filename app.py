from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

app = Flask(__name__)

# Load the trained machine learning model and encoders
model = pickle.load(open('crop_model.pkl', 'rb'))
state_encoder = pickle.load(open('label_encode.pkl', 'rb'))

# Feature transformation based on the user's input
def transform_input_data(N_SOIL, P_SOIL, K_SOIL, TEMPERATURE, HUMIDITY, ph, RAINFALL, STATE):
    if STATE is None:
        raise ValueError("State cannot be None")

    try:
        state_value = state_encoder.transform([STATE])[0]
    except ValueError:
        raise ValueError(f"State '{STATE}' is not valid. Please select a valid state.")
    
    input_data = np.array([N_SOIL, P_SOIL, K_SOIL, TEMPERATURE, HUMIDITY, ph, RAINFALL, state_value])
    return input_data


@app.route('/')
def index():
    # Render the HTML page when the user visits the homepage
    return render_template('index.html')

@app.route('/get-recommendation', methods=['POST'])
def recommend_crop():
    # Extract data from the POST request
    data = request.get_json()

    N_SOIL = data.get('N_SOIL')
    P_SOIL = data.get('P_SOIL')
    K_SOIL = data.get('K_SOIL')
    TEMPERATURE = data.get('TEMPERATURE')
    HUMIDITY = data.get('HUMIDITY')
    ph = data.get('ph')
    RAINFALL = data.get('RAINFALL')
    STATE = data.get('STATE')

    # Transform the input data into the format the model expects
    input_data = transform_input_data(N_SOIL, P_SOIL, K_SOIL, TEMPERATURE, HUMIDITY, ph, RAINFALL, STATE)
    # Reshape input_data to be 2D (1 sample with multiple features)
    input_data = input_data.reshape(1, -1)

    # Get the prediction from the model
    recommended_crop = model.predict(input_data)[0]  # Get the first prediction

    # Return the result as JSON
    return jsonify({'recommended_crop': recommended_crop})

if __name__ == '__main__':
    app.run(debug=True)
    

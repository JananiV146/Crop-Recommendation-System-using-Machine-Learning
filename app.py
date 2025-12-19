import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import LabelEncoder

# Page configuration
st.set_page_config(page_title="Crop Recommendation System", layout="wide")

# Title and description
st.title("🌾 Crop Recommendation System")
st.markdown("Predict the best crop based on soil and climate conditions")

# Load trained model and label encoder
@st.cache_resource
def load_model():
    if os.path.exists('crop_model.pkl') and os.path.exists('label_encode.pkl'):
        model = pickle.load(open('crop_model.pkl', 'rb'))
        label_encoder = pickle.load(open('label_encode.pkl', 'rb'))
        return model, label_encoder
    else:
        st.error("Model files not found. Please train the model first using the notebook.")
        return None, None

model, label_encoder = load_model()

# Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select a page:", ["Home", "About", "Data Info"])

if page == "Home":
    if model is not None:
        st.header("Make a Prediction")
        
        # Create two columns for input
        col1, col2 = st.columns(2)
        
        with col1:
            state = st.selectbox(
                "Select State",
                ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
                 "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
                 "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", 
                 "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", 
                 "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", 
                 "West Bengal"]
            )
            
            nitrogen = st.number_input(
                "Nitrogen (N) content",
                min_value=0.0,
                max_value=200.0,
                value=50.0,
                step=1.0
            )
            
            phosphorus = st.number_input(
                "Phosphorus (P) content",
                min_value=0.0,
                max_value=200.0,
                value=50.0,
                step=1.0
            )
            
            potassium = st.number_input(
                "Potassium (K) content",
                min_value=0.0,
                max_value=200.0,
                value=50.0,
                step=1.0
            )
        
        with col2:
            temperature = st.number_input(
                "Temperature (°C)",
                min_value=-10.0,
                max_value=60.0,
                value=25.0,
                step=0.1
            )
            
            humidity = st.number_input(
                "Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=50.0,
                step=0.1
            )
            
            ph = st.number_input(
                "Soil pH",
                min_value=0.0,
                max_value=14.0,
                value=7.0,
                step=0.1
            )
            
            rainfall = st.number_input(
                "Rainfall (mm)",
                min_value=0.0,
                max_value=500.0,
                value=100.0,
                step=1.0
            )
        
        # Prediction button
        if st.button("🔮 Get Crop Recommendation", use_container_width=True):
            try:
                # Encode state
                state_encoded = label_encoder.transform([state])[0]
                
                # Create input array
                input_data = np.array([[nitrogen, phosphorus, potassium, temperature, 
                                       humidity, ph, rainfall, state_encoded]])
                
                # Make prediction
                prediction = model.predict(input_data)[0]
                
                # Display result
                st.success(f"Recommended Crop: **{prediction}**")
                
                # Display input summary
                st.subheader("Input Summary")
                summary_df = pd.DataFrame({
                    "Parameter": ["State", "Nitrogen (N)", "Phosphorus (P)", "Potassium (K)", 
                                 "Temperature", "Humidity", "pH", "Rainfall"],
                    "Value": [state, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]
                })
                st.dataframe(summary_df, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error in prediction: {str(e)}")

elif page == "About":
    st.header("About This Application")
    st.markdown("""
    ### Crop Recommendation System
    
    This application uses a **Decision Tree Classifier** to recommend the best crop 
    based on various environmental and soil parameters.
    
    #### Features Used:
    - **Nitrogen (N)**: Essential macronutrient for plant growth
    - **Phosphorus (P)**: Important for root development and energy transfer
    - **Potassium (K)**: Aids in overall plant health and disease resistance
    - **Temperature**: Affects crop growth rates and seasonal suitability
    - **Humidity**: Influences disease susceptibility and plant hydration
    - **Soil pH**: Determines nutrient availability to plants
    - **Rainfall**: Critical for crop water requirements
    - **State**: Geographic location affecting climate and local agricultural practices
    
    #### How It Works:
    1. Collect soil and climate data
    2. Process and normalize the features
    3. Use the trained Decision Tree model to classify the most suitable crop
    4. Display the recommendation to the user
    
    #### Technologies Used:
    - **Streamlit**: Web application framework
    - **Scikit-learn**: Machine learning library
    - **Pandas & NumPy**: Data processing
    """)

elif page == "Data Info":
    st.header("Dataset Information")
    st.markdown("""
    #### Dataset Overview
    
    The model was trained on agricultural data including:
    - **Features**: Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall, State
    - **Target**: Crop type
    
    #### Model Performance
    - **Algorithm**: Decision Tree Classifier
    - **Train/Test Split**: 70% training, 30% testing
    
    #### Supported Crops
    The model can recommend from various crops including:
    - Rice, Wheat, Corn, Cotton
    - Sugarcane, Millets, Oilseeds
    - And many others based on the training data
    """)

# Footer
st.divider()
st.markdown("---")
st.markdown(
    "<div style='text-align: center'><p>Crop Recommendation System | Powered by Machine Learning</p></div>",
    unsafe_allow_html=True
)

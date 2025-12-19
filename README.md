# Crop Recommendation System - Streamlit Web Application

A web-based machine learning application for recommending crops based on soil and climate conditions.

## Features

- 🎯 Interactive crop prediction interface
- 📊 Real-time recommendations using Decision Tree ML model
- 🌍 Support for multiple Indian states
- 📈 Input validation and error handling
- 📱 Responsive web design

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Navigate to the project directory**
   ```bash
   cd "D:\Machine Learning project"
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### First Time Setup - Train the Model

Run the Jupyter notebook to train the model and generate the pickle files:
```bash
jupyter notebook "ML Project (1).ipynb"
```

Or use VS Code to run all cells in the notebook. This will generate:
- `crop_model.pkl` - Trained Decision Tree model
- `label_encode.pkl` - Label encoder for state encoding

### Start the Streamlit App

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## How to Use

1. **Select Navigation**: Use the sidebar to navigate between pages
2. **Home Page**: 
   - Select your state from the dropdown
   - Enter soil parameters (Nitrogen, Phosphorus, Potassium)
   - Enter climate parameters (Temperature, Humidity, pH, Rainfall)
   - Click "Get Crop Recommendation" button
3. **About Page**: Learn about the system and features
4. **Data Info Page**: View dataset and model information

## Input Parameters

| Parameter | Range | Unit | Description |
|-----------|-------|------|-------------|
| Nitrogen (N) | 0-200 | mg/kg | Soil nitrogen content |
| Phosphorus (P) | 0-200 | mg/kg | Soil phosphorus content |
| Potassium (K) | 0-200 | mg/kg | Soil potassium content |
| Temperature | -10 to 60 | °C | Average temperature |
| Humidity | 0-100 | % | Relative humidity |
| pH | 0-14 | - | Soil pH level |
| Rainfall | 0-500 | mm | Annual/seasonal rainfall |

## Project Structure

```
Machine Learning project/
├── ML Project (1).ipynb          # Original Jupyter notebook with model training
├── app.py                        # Streamlit web application
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── crop_model.pkl                # Trained Decision Tree model (generated)
└── label_encode.pkl              # Label encoder for states (generated)
```

## Technologies Used

- **Streamlit**: Web framework for building data applications
- **Scikit-learn**: Machine learning library
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Pickle**: Model serialization

## Model Information

- **Algorithm**: Decision Tree Classifier
- **Training Data Split**: 70% training, 30% testing
- **Input Features**: 8 (Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall, State)
- **Output**: Crop recommendation

## Troubleshooting

### "Model files not found" error
- Make sure you've run the Jupyter notebook first to generate `crop_model.pkl` and `label_encode.pkl`
- Verify these files exist in the same directory as `app.py`

### Streamlit not found
```bash
pip install streamlit
```

### CSV file not found error
- Update the CSV path in the notebook if needed
- Ensure `CropRecommendation.csv` is in the correct location

## Future Enhancements

- Add more ML algorithms (Random Forest, XGBoost, etc.)
- Model comparison feature
- Historical data visualization
- Export recommendations as PDF
- API endpoint for integration

## License

This project is for educational purposes.

## Support

For issues or questions, please refer to the Streamlit documentation:
- https://docs.streamlit.io/

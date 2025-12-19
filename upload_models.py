"""
Script to upload model files to Snowflake
Run this locally before deployment
"""

from snowflake.snowpark import Session
import os

# Snowflake connection config
config = {
    "account": "xy12345.us-east-1",  # Replace with your account
    "user": "STREAMLIT_USER",
    "password": "YourSecurePassword123!",
    "warehouse": "COMPUTE_WH",
    "database": "CROP_RECOMMENDATION",
    "schema": "ML_MODELS"
}

try:
    # Create session
    session = Session.builder.configs(config).create()
    print("✅ Connected to Snowflake")
    
    # Create stage if not exists
    session.sql("CREATE STAGE IF NOT EXISTS @MODEL_STAGE").collect()
    print("✅ Stage created/verified")
    
    # Upload model files
    if os.path.exists("crop_model.pkl"):
        session.file.put("crop_model.pkl", "@MODEL_STAGE", auto_compress=False, overwrite=True)
        print("✅ Uploaded crop_model.pkl")
    
    if os.path.exists("label_encode.pkl"):
        session.file.put("label_encode.pkl", "@MODEL_STAGE", auto_compress=False, overwrite=True)
        print("✅ Uploaded label_encode.pkl")
    
    # List uploaded files
    files = session.sql("LIST @MODEL_STAGE").collect()
    print("\n📁 Files in Snowflake stage:")
    for f in files:
        print(f"  - {f}")
    
    session.close()
    print("\n✅ Upload complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")

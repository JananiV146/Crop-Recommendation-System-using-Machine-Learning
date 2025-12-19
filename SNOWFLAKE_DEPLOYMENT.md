# Deploying to Snowflake - Complete Guide

## Method 1: Streamlit Community Cloud + Snowflake Backend (Recommended)

### Prerequisites
- Snowflake account (free tier available at https://www.snowflake.com/en/free-trial/)
- GitHub account
- Streamlit Community Cloud account

### Deployment Steps

#### 1. Prepare Snowflake

```sql
-- Connect to your Snowflake account
-- Run these SQL commands:

-- Create database
CREATE DATABASE CROP_RECOMMENDATION;
USE DATABASE CROP_RECOMMENDATION;

-- Create schema
CREATE SCHEMA ML_MODELS;

-- Create stage for storing models
CREATE STAGE MODEL_STAGE;

-- Upload model files
-- Use SnowSQL or Snowflake UI to upload crop_model.pkl and label_encode.pkl
```

#### 2. Prepare GitHub Repository

1. Push your code to GitHub (already done ✓)
2. Ensure `.streamlit/secrets.toml` is in `.gitignore` (DON'T push secrets!)

```bash
echo ".streamlit/secrets.toml" >> .gitignore
```

#### 3. Deploy on Streamlit Community Cloud

1. Go to https://streamlit.io/cloud
2. Sign up with your GitHub account
3. Click "New app"
4. Connect your GitHub repo
5. Select branch: `main`
6. Set main file path: `app_snowflake.py` (or `app.py`)
7. Click "Deploy"

#### 4. Add Secrets in Streamlit Cloud

1. In Streamlit Cloud dashboard, click your app's ⋮ menu
2. Click "Manage secrets"
3. Copy content from `.streamlit/secrets.toml` and paste it there:

```toml
[snowflake]
account = "your-account-id"
user = "your-username"
password = "your-password"
warehouse = "COMPUTE_WH"
database = "CROP_RECOMMENDATION"
schema = "ML_MODELS"
role = "ACCOUNTADMIN"
```

✅ Your app is now live!

---

## Method 2: Snowflake Native App Framework

### Setup Steps

#### 1. Create Manifest File

Create `manifest.yml`:
```yaml
manifest_version: 1

metadata:
  name: crop_recommendation_app
  title: Crop Recommendation System
  description: ML-based crop recommendation using Streamlit
  version: 1.0.0
  
artifacts:
  source_code:
    location: ./
  
app:
  name: crop_recommendation
  title: Crop Recommendation System
  owner:
    name: Your Name
    email: your-email@example.com
```

#### 2. Deploy

```bash
# Using Snowflake CLI
snow app create

# Or through Snowflake Console
# 1. Create application package
# 2. Upload manifest and app files
# 3. Create application from package
```

---

## Method 3: Docker Deployment on Snowflake Containers

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app_snowflake.py", "--server.port=8501"]
```

### Build and Push

```bash
# Build image
docker build -t crop-recommendation-app .

# Tag for Snowflake registry
docker tag crop-recommendation-app:latest your-registry.azurecr.io/crop-recommendation-app:latest

# Push to registry
docker push your-registry.azurecr.io/crop-recommendation-app:latest
```

---

## Setting up Snowflake Connection Locally

### Install Snowflake CLI

```bash
# Install Snowflake CLI
pip install snowflake-cli-labs

# Configure connection
snow connection add

# Test connection
snow sql -q "SELECT CURRENT_VERSION()"
```

### Local Testing

```bash
# Set Snowflake environment variables
$env:SNOWFLAKE_ACCOUNT = "your-account-id"
$env:SNOWFLAKE_USER = "your-username"
$env:SNOWFLAKE_PASSWORD = "your-password"
$env:SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
$env:SNOWFLAKE_DATABASE = "CROP_RECOMMENDATION"

# Run app
streamlit run app_snowflake.py
```

---

## Uploading Models to Snowflake

### Via SnowSQL

```bash
# Connect
snowsql -a your-account-id -u your-username

-- Create stage
CREATE STAGE IF NOT EXISTS @MODEL_STAGE;

-- Upload files
PUT file://crop_model.pkl @MODEL_STAGE;
PUT file://label_encode.pkl @MODEL_STAGE;

-- Verify
LIST @MODEL_STAGE;
```

### Via Python

```python
from snowflake.snowpark import Session

config = {
    "account": "your-account-id",
    "user": "your-username",
    "password": "your-password",
    "warehouse": "COMPUTE_WH",
    "database": "CROP_RECOMMENDATION",
    "schema": "ML_MODELS"
}

session = Session.builder.configs(config).create()

# Create stage
session.sql("CREATE STAGE IF NOT EXISTS @MODEL_STAGE").collect()

# Upload files
session.file.put("crop_model.pkl", "@MODEL_STAGE")
session.file.put("label_encode.pkl", "@MODEL_STAGE")
```

---

## Monitoring and Logging

### Query Prediction Logs

```sql
-- View recent predictions
SELECT * FROM PREDICTION_LOGS ORDER BY CURRENT_TIMESTAMP() DESC LIMIT 10;

-- Most recommended crops
SELECT PREDICTION, COUNT(*) as count 
FROM PREDICTION_LOGS 
GROUP BY PREDICTION 
ORDER BY count DESC;

-- Statistics by state
SELECT STATE, AVG(TEMPERATURE), AVG(HUMIDITY), COUNT(*) 
FROM PREDICTION_LOGS 
GROUP BY STATE;
```

---

## Troubleshooting

### "Connection refused" error
- Verify Snowflake account credentials
- Check if warehouse is running
- Ensure secrets are correctly set in Streamlit Cloud

### "Model files not found"
- Upload models to Snowflake stage
- Verify stage path in app code
- Check file permissions

### Slow load times
- Upgrade Snowflake warehouse size
- Cache queries using `@st.cache_resource`
- Optimize queries

---

## Security Best Practices

1. **Never commit secrets** - Use `.gitignore`
2. **Use service accounts** - Create dedicated Snowflake user for app
3. **Enable encryption** - Use Snowflake's encryption at rest
4. **Set proper roles** - Limit database access with RBAC
5. **Audit logs** - Monitor app usage with Snowflake's audit logs

---

## Quick Start Summary

```bash
# 1. Push to GitHub
git add .
git commit -m "Add Snowflake integration"
git push origin main

# 2. Deploy to Streamlit Cloud
# - Go to https://streamlit.io/cloud
# - Connect GitHub repo
# - Add Snowflake secrets

# 3. Access your app at:
# https://your-app-name.streamlit.app
```

**Your app is now live with Snowflake backend!** 🚀

#!/bin/bash
# Quick deployment script for Q360 to Google Cloud Run

echo "=========================================="
echo "Q360 Deployment to Google Cloud Run"
echo "=========================================="

# Set variables
PROJECT_ID="gen-lang-client-0256721605"
REGION="us-central1"
SERVICE_NAME="q360-api"

# Step 1: Authenticate
echo "[1/5] Authenticating with Google Cloud..."
gcloud auth login
gcloud config set project $PROJECT_ID

# Step 2: Set environment variables
echo "[2/5] Collecting environment variables..."
read -p "Enter JIRA API Token: " JIRA_TOKEN
read -p "Enter JIRA Email: " JIRA_EMAIL

# Step 3: Deploy to Cloud Run
echo "[3/5] Deploying to Google Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GCP_PROJECT_ID=$PROJECT_ID \
  --set-env-vars GCP_REGION=$REGION \
  --set-env-vars JIRA_URL=https://saipratap.atlassian.net \
  --set-env-vars JIRA_EMAIL=$JIRA_EMAIL \
  --set-env-vars JIRA_API_TOKEN=$JIRA_TOKEN \
  --memory 512Mi \
  --cpu 1 \
  --timeout 3600

# Step 4: Get service URL
echo "[4/5] Getting service URL..."
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
echo "API URL: $SERVICE_URL"

# Step 5: Test deployment
echo "[5/5] Testing deployment..."
curl $SERVICE_URL/health

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo "API URL: $SERVICE_URL"
echo ""
echo "Next steps:"
echo "1. Deploy frontend to Vercel"
echo "2. Set REACT_APP_API_URL=$SERVICE_URL in Vercel"
echo "3. Access dashboard at your Vercel URL"
echo ""
echo "View logs: gcloud run logs read $SERVICE_NAME --region $REGION"
echo "Monitor: https://console.cloud.google.com/run?project=$PROJECT_ID"

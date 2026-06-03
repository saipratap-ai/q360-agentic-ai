#!/bin/bash
# Setup Google Cloud Secret Manager for Q360

PROJECT_ID="gen-lang-client-0256721605"

echo "=========================================="
echo "Setting up Secret Manager"
echo "=========================================="

# Enable Secret Manager API
echo "[1/6] Enabling Secret Manager API..."
gcloud services enable secretmanager.googleapis.com --project=$PROJECT_ID

# Create secrets
echo "[2/6] Creating JIRA_EMAIL secret..."
echo -n "saipratap.vr@gmail.com" | gcloud secrets create jira-email \
  --replication-policy="automatic" \
  --data-file=- \
  --project=$PROJECT_ID 2>/dev/null || \
gcloud secrets versions add jira-email --data-file=- --project=$PROJECT_ID

echo "[3/6] Creating JIRA_URL secret..."
echo -n "https://saipratap.atlassian.net" | gcloud secrets create jira-url \
  --replication-policy="automatic" \
  --data-file=- \
  --project=$PROJECT_ID 2>/dev/null || \
gcloud secrets versions add jira-url --data-file=- --project=$PROJECT_ID

echo "[4/6] Creating JIRA_API_TOKEN secret..."
read -sp "Enter JIRA API Token: " JIRA_TOKEN
echo -n "$JIRA_TOKEN" | gcloud secrets create jira-api-token \
  --replication-policy="automatic" \
  --data-file=- \
  --project=$PROJECT_ID 2>/dev/null || \
gcloud secrets versions add jira-api-token --data-file=- --project=$PROJECT_ID

echo ""
echo "[5/6] Creating GOOGLE_API_KEY secret..."
read -sp "Enter Google API Key: " GOOGLE_API_KEY
echo -n "$GOOGLE_API_KEY" | gcloud secrets create google-api-key \
  --replication-policy="automatic" \
  --data-file=- \
  --project=$PROJECT_ID 2>/dev/null || \
gcloud secrets versions add google-api-key --data-file=- --project=$PROJECT_ID

echo ""
echo "[6/6] Granting Cloud Run access to secrets..."
# Get Cloud Run service account
SERVICE_ACCOUNT=$(gcloud iam service-accounts list \
  --filter="displayName:Cloud Run" \
  --format="value(email)" \
  --project=$PROJECT_ID)

if [ -z "$SERVICE_ACCOUNT" ]; then
  SERVICE_ACCOUNT="$(gcloud config get-value project)@appspot.gserviceaccount.com"
fi

# Grant access to all secrets
for secret in jira-email jira-url jira-api-token google-api-key; do
  gcloud secrets add-iam-policy-binding $secret \
    --member=serviceAccount:$SERVICE_ACCOUNT \
    --role=roles/secretmanager.secretAccessor \
    --project=$PROJECT_ID 2>/dev/null || true
done

echo ""
echo "=========================================="
echo "Secrets created successfully!"
echo "Service Account: $SERVICE_ACCOUNT"
echo "=========================================="
echo ""
echo "Secrets created:"
gcloud secrets list --project=$PROJECT_ID --format="table(name)"

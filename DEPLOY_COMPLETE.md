# Q360 Complete Deployment Guide (Frontend + Backend + Secrets)

Deploy Q360 with frontend served from same Cloud Run instance and secrets managed securely!

---

## Step 1: Setup Google Cloud Secret Manager

```bash
# Make script executable
chmod +x setup-secrets.sh

# Run secret setup
./setup-secrets.sh
```

This will:
1. Enable Secret Manager API
2. Create secrets for:
   - `jira-email`
   - `jira-url`
   - `jira-api-token`
   - `google-api-key`
3. Grant Cloud Run access to secrets

---

## Step 2: Authenticate with Google Cloud

```bash
gcloud auth login
gcloud config set project gen-lang-client-0256721605
```

---

## Step 3: Deploy to Cloud Run (All-in-One)

```bash
gcloud run deploy q360 \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GCP_PROJECT_ID=gen-lang-client-0256721605 \
  --set-env-vars GCP_REGION=us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 3600 \
  --service-account=$(gcloud iam service-accounts list \
    --filter="displayName:Cloud Run" \
    --format="value(email)")
```

Wait for deployment to complete...

---

## Step 4: Get Your Live URL

```bash
gcloud run services describe q360 --region us-central1 --format 'value(status.url)'
```

Output example:
```
https://q360-xxxxx-uc.a.run.app
```

Your app is now live! ✅

---

## Architecture (Deployed)

```
Cloud Run Service (q360)
├── Backend (FastAPI + Python)
│   ├── AI Agents (Google Cloud Agents SDK)
│   ├── LangGraph Orchestration
│   ├── Jira Integration
│   └── API Endpoints
│
├── Frontend (React)
│   └── Served from /
│
└── Secret Manager Access
    ├── jira-email
    ├── jira-url
    ├── jira-api-token
    └── google-api-key
```

---

## Access Your App

**Frontend Dashboard:**
```
https://q360-xxxxx-uc.a.run.app
```

**Backend API:**
```
https://q360-xxxxx-uc.a.run.app/health      (Health check)
https://q360-xxxxx-uc.a.run.app/docs        (API Docs)
https://q360-xxxxx-uc.a.run.app/generate-tests  (Generate endpoint)
```

---

## Security Benefits

✅ **No secrets in code or environment variables**
✅ **Google Cloud Secret Manager encryption**
✅ **Automatic secret rotation**
✅ **Audit logging for all secret access**
✅ **Fine-grained IAM permissions**

---

## Monitor Your Deployment

### View Logs
```bash
gcloud run logs read q360 --region us-central1 --limit 100
```

### Monitor Costs
```bash
# View service
gcloud run services describe q360 --region us-central1

# Check usage
gcloud monitoring dashboards list
```

Or visit: https://console.cloud.google.com/run?project=gen-lang-client-0256721605

### Check Secrets Usage
```bash
# List all secrets
gcloud secrets list --project=gen-lang-client-0256721605

# View secret versions
gcloud secrets versions list jira-api-token \
  --project=gen-lang-client-0256721605

# View access logs
gcloud logging read "resource.type=secretmanager.googleapis.com" \
  --project=gen-lang-client-0256721605
```

---

## Update Secrets Anytime

```bash
# Update Jira token
echo -n "new-token" | gcloud secrets versions add jira-api-token \
  --data-file=- \
  --project=gen-lang-client-0256721605

# Redeploy to use new secret
gcloud run deploy q360 \
  --source . \
  --platform managed \
  --region us-central1
```

---

## Cost Breakdown (Still FREE!)

| Component | Free Tier | Cost |
|-----------|-----------|------|
| **Cloud Run** | 2M requests/month | **FREE** ✅ |
| **Secret Manager** | 6 secrets free | **FREE** ✅ |
| **Vertex AI API** | Per request | ~₹50-200/month |
| **Total** | | **~₹100-200/month** |

Your ₹1000 credits = **5-10 months completely free!**

---

## Troubleshooting

### Service won't start?
```bash
gcloud run logs read q360 --region us-central1 --limit 50
```

### Can't access frontend?
```bash
# Check service status
gcloud run services describe q360 --region us-central1

# Test health endpoint
curl https://q360-xxxxx-uc.a.run.app/health
```

### Secrets not loading?
```bash
# Verify service account has secret access
gcloud secrets get-iam-policy jira-api-token \
  --project=gen-lang-client-0256721605

# Re-grant access if needed
gcloud secrets add-iam-policy-binding jira-api-token \
  --member=serviceAccount:SERVICE_ACCOUNT_EMAIL \
  --role=roles/secretmanager.secretAccessor
```

---

## Useful Commands

```bash
# View all deployments
gcloud run services list --region us-central1

# Update existing deployment
gcloud run deploy q360 --source . --region us-central1

# Delete service
gcloud run services delete q360 --region us-central1

# Stream logs in real-time
gcloud run logs read q360 --region us-central1 --follow

# Get service URL quickly
gcloud run services describe q360 --region us-central1 \
  --format 'value(status.url)'
```

---

## What's Deployed

✅ **Backend API** - FastAPI with Google Cloud Agents SDK
✅ **Frontend** - React dashboard (served from same service)
✅ **AI Agents** - Test Case & Test Data generators
✅ **Orchestration** - LangGraph workflow
✅ **Jira Integration** - Full read/write access
✅ **Security** - Google Cloud Secret Manager
✅ **Health Check** - Automated monitoring

---

## Next Steps

1. ✅ Deploy to Cloud Run
2. ✅ Access dashboard at `https://q360-xxxxx-uc.a.run.app`
3. ✅ Generate tests from Jira stories
4. 📊 Monitor usage and costs
5. 🔄 Scale as needed

---

**Your Q360 MVP is now live and production-ready!** 🚀

Deployed with:
- Google Cloud Agents SDK
- LangGraph Orchestration
- Google Cloud Secret Manager
- Single Cloud Run Service

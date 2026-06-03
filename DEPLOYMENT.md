# Q360 Deployment Guide

Deploy Q360 to Google Cloud Run with free trial credits!

## Prerequisites

1. **Google Cloud Project:** gen-lang-client-0256721605
2. **Billing Account:** Activated with trial credits
3. **Google Cloud CLI:** Installed locally
4. **Docker:** Installed locally (optional if using Cloud Build)

---

## Quick Deployment (Recommended)

### Step 1: Authenticate with Google Cloud

```bash
gcloud auth login
gcloud config set project gen-lang-client-0256721605
```

### Step 2: Create Environment Configuration

Create `.env.production` in project root:

```bash
GCP_PROJECT_ID=gen-lang-client-0256721605
GCP_REGION=us-central1
JIRA_URL=https://saipratap.atlassian.net
JIRA_EMAIL=saipratap.vr@gmail.com
JIRA_API_TOKEN=<your_jira_token>
API_HOST=0.0.0.0
API_PORT=8000
```

### Step 3: Deploy to Cloud Run (Option A - Recommended)

```bash
# Deploy directly from source
gcloud run deploy q360-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GCP_PROJECT_ID=gen-lang-client-0256721605 \
  --set-env-vars GCP_REGION=us-central1 \
  --set-env-vars JIRA_URL=https://saipratap.atlassian.net \
  --set-env-vars JIRA_EMAIL=saipratap.vr@gmail.com \
  --set-env-vars JIRA_API_TOKEN=<your_token> \
  --memory 512Mi \
  --cpu 1 \
  --timeout 3600
```

### Step 4: Get the API URL

```bash
# Get your deployed service URL
gcloud run services describe q360-api --region us-central1
```

Output example:
```
Service URL: https://q360-api-xxxxx-uc.a.run.app
```

---

## Deploy Frontend (Vercel)

### Step 1: Push code to GitHub
```bash
git push origin main
```

### Step 2: Connect to Vercel
1. Go to https://vercel.com
2. Import project from GitHub
3. Set environment variables:
   ```
   REACT_APP_API_URL=https://q360-api-xxxxx-uc.a.run.app
   ```
4. Deploy

Your frontend will be available at `https://q360-xxx.vercel.app`

---

## Verify Deployment

### Test Backend API

```bash
# Health check
curl https://q360-api-xxxxx-uc.a.run.app/health

# Test generation endpoint
curl -X POST https://q360-api-xxxxx-uc.a.run.app/generate-tests \
  -H "Content-Type: application/json" \
  -d '{"jira_issue_key": "KAN-4"}'
```

### Access Frontend

Open: `https://q360-xxx.vercel.app`
- Enter issue key: `KAN-4`
- Click "Generate Tests"
- View results

---

## Cost Tracking

### Monitor Costs

1. Go to: https://console.cloud.google.com/billing
2. Check "Billing Overview"
3. Monitor API usage under "Services"

### Free Tier Limits (should stay within):
- Cloud Run: 2M requests/month
- Vertex AI: Based on API calls
- Storage: 5GB/month

---

## Troubleshooting

### Cloud Run not starting?

```bash
# Check logs
gcloud run logs read q360-api --region us-central1 --limit 50
```

### Environment variables not set?

```bash
# Update service with env vars
gcloud run deploy q360-api \
  --update-env-vars KEY=VALUE \
  --region us-central1
```

### Need to rebuild?

```bash
# Force rebuild and redeploy
gcloud run deploy q360-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --force-unlock
```

---

## Alternative: Deploy with Cloud Build (CI/CD)

```bash
# Deploy using Cloud Build pipeline
gcloud builds submit --config cloudbuild.yaml
```

This will:
1. Build Docker image
2. Push to Container Registry
3. Deploy to Cloud Run

---

## Scaling & Performance

### Adjust for traffic:

```bash
# Increase memory if needed
gcloud run deploy q360-api \
  --memory 1024Mi \
  --cpu 2 \
  --concurrency 100 \
  --region us-central1
```

### Auto-scaling settings:
- Min instances: 0 (scales to zero when idle)
- Max instances: 100
- Timeout: 3600 seconds

---

## Next Steps

1. ✅ Deploy backend to Cloud Run
2. ✅ Deploy frontend to Vercel
3. ✅ Test endpoints
4. ✅ Monitor costs
5. 🔄 Scale as needed

---

## Useful Commands

```bash
# List all deployments
gcloud run services list --region us-central1

# View service details
gcloud run services describe q360-api --region us-central1

# Update service
gcloud run services update q360-api --region us-central1

# Delete service
gcloud run services delete q360-api --region us-central1

# Stream logs
gcloud run logs read q360-api --region us-central1 --limit 100 --follow

# Check quotas
gcloud compute project-info describe --project=gen-lang-client-0256721605
```

---

## Support

- Cloud Run Docs: https://cloud.google.com/run/docs
- Pricing: https://cloud.google.com/run/pricing
- Free Tier: https://cloud.google.com/free

---

**Deployment completed! Your API is live and ready to use.** 🚀

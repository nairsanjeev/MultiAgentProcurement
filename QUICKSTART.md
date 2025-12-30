# Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Azure OpenAI or Microsoft Foundry account
- [ ] Model deployment (recommended: gpt-4o)
- [ ] Azure credentials (API key or Azure CLI configured)

## 5-Minute Setup

### Step 1: Clone and Setup Backend (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies (IMPORTANT: --pre flag required!)
pip install -r requirements.txt --pre

# Configure environment
cp .env.example .env
# Edit .env with your Azure credentials
```

### Step 2: Configure Azure Credentials (1 minute)

Edit `backend/.env`:

```env
# Choose ONE of these approaches:

# Option A: Azure OpenAI with API Key (Easiest)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
USE_AZURE_CREDENTIAL=false

# Option B: Microsoft Foundry with Azure Credential
FOUNDRY_PROJECT_ENDPOINT=https://your-project.cognitiveservices.azure.com/
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4o
USE_AZURE_CREDENTIAL=true
```

**Finding Your Credentials:**
- Azure OpenAI Endpoint: Azure Portal → Your OpenAI Resource → Keys and Endpoint
- Foundry Endpoint: AI Foundry → Your Project → Settings → Endpoint

### Step 3: Start Backend (30 seconds)

```bash
# From backend directory
python main.py
```

You should see:
```
Starting Procurement Agent API on port 8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Setup Frontend (1 minute)

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure environment (optional - defaults to localhost:8000)
cp .env.local.example .env.local

# Start development server
npm run dev
```

You should see:
```
> procurement-agent-frontend@1.0.0 dev
> next dev -p 3000

  ▲ Next.js 14.2.0
  - Local:        http://localhost:3000
```

### Step 5: Test the Application (30 seconds)

1. Open browser: `http://localhost:3000`
2. Upload a sample document from `sample_documents/sample_quote_1.txt`
3. Click "Process Document"
4. Watch the multi-agent workflow in action!

## Verification Checklist

After setup, verify:
- [ ] Backend API responding at http://localhost:8000/health
- [ ] Frontend loading at http://localhost:3000
- [ ] Can upload a document
- [ ] Document processing completes successfully
- [ ] See all 4 agent stages complete

## Common Quick Fixes

### Backend won't start?
```bash
# Reinstall with --pre flag
pip uninstall agent-framework-azure-ai
pip install agent-framework-azure-ai --pre
```

### Frontend build errors?
```bash
# Clean install
rm -rf node_modules .next
npm install
```

### Connection refused?
- Check backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in frontend/.env.local
- Try: `curl http://localhost:8000/health`

### Azure authentication errors?
- Verify your endpoint URL format
- Check API key is copied correctly (no spaces)
- Ensure model deployment name matches exactly
- For Foundry, try `az login` if using Azure Credential

## Next Steps

Once running successfully:
1. ✅ Try uploading different quote documents
2. ✅ Check the approved suppliers in `backend/data/approved_suppliers.json`
3. ✅ Modify supplier data and retest validation
4. ✅ Review the agent implementation in `backend/agents/`
5. ✅ Customize the workflow in `backend/workflow.py`

## Need Help?

Check the full README.md for:
- Detailed architecture explanation
- API endpoint documentation
- Customization guide
- Troubleshooting section
- Links to Microsoft Agent Framework docs

---

**🎉 You're ready to accelerate procurement with AI agents!**

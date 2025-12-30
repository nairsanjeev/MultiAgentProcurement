# 🚀 Getting Started - First Time Setup

Welcome to the AI-Powered Procurement System! This guide will get you up and running in **5 minutes**.

## ✅ Prerequisites Checklist

Before you begin, ensure you have:

- [ ] **Python 3.10+** installed ([Download](https://www.python.org/downloads/))
- [ ] **Node.js 18+** installed ([Download](https://nodejs.org/))
- [ ] **Azure OpenAI** or **Microsoft Foundry** account
- [ ] **Model deployed** (recommended: gpt-4o)
- [ ] **API Key** or **Azure CLI** configured

### Verify Prerequisites

```bash
# Check Python version
python --version
# Should show: Python 3.10.x or higher

# Check Node.js version
node --version
# Should show: v18.x.x or higher

# Check if Azure CLI is configured (optional)
az account show
```

## 🎯 Quick Start (5 Minutes)

### Option 1: Automated Setup (Recommended)

**Windows (PowerShell):**
```powershell
cd c:\ProcurementMagenticDemo
.\setup.ps1
```

**Linux/Mac (Bash):**
```bash
cd /path/to/ProcurementMagenticDemo
chmod +x setup.sh
./setup.sh
```

This script will:
1. ✅ Create Python virtual environment
2. ✅ Install backend dependencies (with `--pre` flag)
3. ✅ Install frontend dependencies
4. ✅ Create `.env` files from templates

### Option 2: Manual Setup

#### Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies (IMPORTANT: --pre flag required!)
pip install -r requirements.txt --pre
```

#### Step 2: Configure Azure (1 minute)

Edit `backend/.env` with your credentials:

```env
# OPTION A: Azure OpenAI (Easiest)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=paste-your-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
USE_AZURE_CREDENTIAL=false

# OPTION B: Microsoft Foundry
FOUNDRY_PROJECT_ENDPOINT=https://your-project.cognitiveservices.azure.com/
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4o
USE_AZURE_CREDENTIAL=true
```

**Where to find these values:**
1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your OpenAI resource
3. Click "Keys and Endpoint"
4. Copy the endpoint and key

#### Step 3: Frontend Setup (1 minute)

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Environment already configured by default
# (Optional) Create custom .env.local if needed
```

#### Step 4: Start the Application (1 minute)

**Terminal 1 - Backend:**
```bash
cd backend
# Activate venv if not already active
python main.py
```

You should see:
```
Starting Procurement Agent API on port 8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

You should see:
```
▲ Next.js 14.2.0
- Local:        http://localhost:3000
- Ready in 2.3s
```

## 🧪 Test the Application

1. **Open your browser:** `http://localhost:3000`

2. **Upload a test document:**
   - Click the upload area
   - Select `sample_documents/sample_quote_1.txt`
   - Click "Process Document"

3. **Watch the magic happen:**
   - ✅ Document Extraction
   - ✅ Supplier Validation
   - ✅ Competitive Analysis
   - ✅ Purchase Order Creation

4. **Review the results:**
   - Quote details with pricing
   - Supplier approval status
   - Competitive analysis
   - Generated purchase order

5. **Test approval flow:**
   - Enter an approver email
   - Click "Send for Approval"
   - See confirmation message

## 🎉 Success! What's Next?

### Try These:
- [ ] Upload the second sample document (`sample_quote_2.txt`)
- [ ] Create your own quote document
- [ ] Modify supplier data in `backend/data/approved_suppliers.json`
- [ ] Change agent prompts in `backend/agents/*.py`
- [ ] Customize the UI in `frontend/components/*.tsx`

### Learn More:
- 📖 Read the full [README.md](README.md)
- 🏗️ Understand the [ARCHITECTURE.md](ARCHITECTURE.md)
- 🚀 Plan your [DEPLOYMENT.md](DEPLOYMENT.md)

## ❗ Troubleshooting

### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'agent_framework'`

**Fix:**
```bash
pip uninstall agent-framework-azure-ai
pip install agent-framework-azure-ai --pre
```

**Error:** `401 Unauthorized` or `403 Forbidden`

**Fix:**
- Verify your API key is correct (no extra spaces)
- Check your endpoint URL format
- Ensure your Azure subscription is active
- Try: `az login` if using Azure Credential

### Frontend won't start

**Error:** Cannot find module errors

**Fix:**
```bash
rm -rf node_modules .next
npm install
```

**Error:** Cannot connect to backend

**Fix:**
- Verify backend is running: `curl http://localhost:8000/health`
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Ensure no firewall blocking port 8000

### Document processing fails

**Error:** PDF extraction fails

**Fix:**
```bash
pip install PyPDF2
```

**Error:** JSON parsing error from agents

**Fix:**
- This is usually a model response format issue
- Try processing a simpler document first
- Check your model deployment is active

## 📞 Need Help?

1. **Check the logs:**
   - Backend: Look at terminal output
   - Frontend: Open browser DevTools (F12)

2. **Verify configuration:**
   - `backend/.env` has correct values
   - Model deployment name matches exactly
   - Endpoint URLs are correct

3. **Test individually:**
   - Backend health: `http://localhost:8000/health`
   - Frontend loads: `http://localhost:3000`

4. **Common fixes:**
   - Restart both servers
   - Clear browser cache
   - Reinstall dependencies

## 🎓 Learning Path

### Beginner:
1. Run the application with sample documents
2. Review the results
3. Try different quote documents
4. Modify supplier database

### Intermediate:
1. Read through agent implementations
2. Modify agent prompts
3. Customize UI components
4. Add new suppliers

### Advanced:
1. Add new agents to the pipeline
2. Implement additional validation rules
3. Add database persistence
4. Deploy to Azure

## 🔄 Daily Development Workflow

```bash
# Start your day
cd backend
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
python main.py

# New terminal
cd frontend
npm run dev

# Make changes to code...
# Both servers auto-reload on file changes!

# End of day - just Ctrl+C both terminals
```

## 📚 Key Files to Know

- **Backend API:** `backend/main.py`
- **Workflow Logic:** `backend/workflow.py`
- **Agents:** `backend/agents/*.py`
- **Supplier Data:** `backend/data/approved_suppliers.json`
- **Main UI:** `frontend/app/page.tsx`
- **Components:** `frontend/components/*.tsx`

---

**🎯 Goal:** Get from zero to working app in 5 minutes!

**💪 You've got this! Let's build something amazing with AI agents!**

# AI-Powered Procurement System

A comprehensive procurement acceleration application built with **Microsoft Agent Framework** (Magentic Pattern) and **CopilotKit**, featuring intelligent multi-agent analysis for automated quote processing, supplier validation, and competitive analysis.

## 🌟 Features

### Multi-Agent Workflow
1. **Document Extraction Agent** - Extracts quote details (pricing, quantity) from uploaded documents
2. **Supplier Validation Agent** - Validates suppliers against approved supplier database
3. **Competitive Analysis Agent** - Analyzes quote competitiveness using market intelligence
4. **Purchase Order Agent** - Creates purchase orders and manages approval workflows

### Technology Stack


https://github.com/user-attachments/assets/dec56b27-3f57-42d0-b74b-b6ca083cd9ef


**Backend:**
- **Microsoft Agent Framework** (Python) - Multi-agent orchestration with Magentic pattern
- **Azure OpenAI** / **Microsoft Foundry** - LLM integration
- **FastAPI** - REST API server
- Synthetic supplier database for validation

**Frontend:**
- **Next.js 14** - React framework
- **CopilotKit** - Generative UI and chatbot patterns
- **TailwindCSS** - Styling
- **TypeScript** - Type safety

## 📋 Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Azure OpenAI or Microsoft Foundry account with model deployments
- Azure credentials configured (if using Azure Credential authentication)

## 🚀 Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   # IMPORTANT: --pre flag is REQUIRED while Agent Framework is in preview
   pip install -r requirements.txt --pre
   ```

4. **Configure environment variables:**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env with your Azure credentials
   ```

   Required environment variables:
   ```env
   # For AzureOpenAIChatClient (foundation patterns)
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
   
   # For AzureAIAgentClient (multi-agent workflows)  
   FOUNDRY_PROJECT_ENDPOINT=https://your-project.cognitiveservices.azure.com/
   FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4o
   
   # Or use Azure Credential (Managed Identity/Azure CLI)
   USE_AZURE_CREDENTIAL=false
   ```

5. **Run the backend server:**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure environment variables:**
   ```bash
   # Copy the example env file
   cp .env.local.example .env.local
   
   # Edit .env.local if needed (default: http://localhost:8000)
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```
   
   The app will be available at `http://localhost:3000`

## 📖 Usage

### Processing a Quote Document

1. **Upload Document:**
   - Open the web app at `http://localhost:3000`
   - Drag and drop or click to upload a quote document (PDF or TXT)

2. **Automatic Processing:**
   - The system automatically processes the document through the multi-agent pipeline
   - Watch real-time progress through the stages:
     - Document Extraction
     - Supplier Validation
     - Competitive Analysis
     - Purchase Order Creation

3. **Review Results:**
   - View extracted quote details
   - Check supplier validation status
   - Review competitive analysis
   - View generated purchase order

4. **Approval Workflow:**
   - If approval is required, enter approver email
   - Submit for approval
   - System sends approval request

### Sample Documents

Create a sample quote document (quote.txt):

```
QUOTE DOCUMENT

Supplier: TechSupply Inc.
Quote Number: Q-2024-001
Date: December 7, 2024

Items:
1. Dell Laptop XPS 15
   Quantity: 10 units
   Unit Price: $1,499.00
   Total: $14,990.00

2. Logitech MX Master Mouse
   Quantity: 10 units  
   Unit Price: $99.00
   Total: $990.00

Total Amount: $15,980.00
Currency: USD
```

## 🏗️ Architecture

### Magentic Pattern Implementation

The application uses Microsoft Agent Framework's Magentic pattern with the following workflow:

```python
workflow = (
    WorkflowBuilder()
    .set_start_executor(document_extraction)
    .add_edge(document_extraction, supplier_validation)
    .add_edge(supplier_validation, competitive_analysis)
    .add_edge(competitive_analysis, purchase_order)
    .build()
)
```

### Agent Executors

Each agent is implemented as an `Executor` with `@handler` methods:

```python
class DocumentExtractionAgent(Executor):
    @handler
    async def extract_from_text(
        self, 
        document_text: str, 
        ctx: WorkflowContext[dict]
    ) -> None:
        # Process document and extract quote information
        await ctx.send_message(extracted_data)
```

### API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /api/upload` - Upload and extract document text
- `POST /api/process` - Process document through workflow (non-streaming)
- `POST /api/process-stream` - Process with Server-Sent Events
- `POST /api/approve` - Submit purchase order for approval

## 🗂️ Project Structure

```
ProcurementMagenticDemo/
├── backend/
│   ├── agents/
│   │   ├── document_extraction.py    # Extract quote from documents
│   │   ├── supplier_validation.py    # Validate suppliers
│   │   ├── competitive_analysis.py   # Analyze competitiveness
│   │   └── purchase_order.py         # Create purchase orders
│   ├── data/
│   │   └── approved_suppliers.json   # Synthetic supplier database
│   ├── config.py                     # Configuration management
│   ├── models.py                     # Pydantic data models
│   ├── utils.py                      # Utility functions
│   ├── workflow.py                   # Workflow orchestrator
│   ├── main.py                       # FastAPI server
│   ├── requirements.txt              # Python dependencies
│   └── .env.example                  # Environment template
├── frontend/
│   ├── app/
│   │   ├── page.tsx                  # Main application page
│   │   ├── layout.tsx                # Root layout
│   │   └── globals.css               # Global styles
│   ├── components/
│   │   ├── FileUpload.tsx            # File upload component
│   │   ├── QuoteDisplay.tsx          # Quote display
│   │   ├── ValidationDisplay.tsx     # Validation results
│   │   ├── AnalysisDisplay.tsx       # Competitive analysis
│   │   └── PurchaseOrderDisplay.tsx  # PO display and approval
│   ├── lib/
│   │   ├── types.ts                  # TypeScript types
│   │   ├── api.ts                    # API client
│   │   └── utils.ts                  # Utility functions
│   ├── package.json                  # Node dependencies
│   ├── tsconfig.json                 # TypeScript config
│   └── .env.local.example            # Environment template
└── README.md
```

## 🔧 Configuration

### Approved Suppliers

Edit `backend/data/approved_suppliers.json` to manage the approved supplier list:

```json
{
  "suppliers": [
    {
      "id": "SUP001",
      "name": "TechSupply Inc.",
      "category": "Electronics",
      "rating": 4.8,
      "approved": true,
      "certifications": ["ISO 9001", "ISO 14001"],
      "contact_email": "procurement@techsupply.com"
    }
  ]
}
```

### Model Selection

The system uses GPT-4o by default for optimal performance with vision capabilities and JSON responses. You can configure different models in the `.env` file.

Recommended models for Microsoft Foundry:
- **gpt-5** - Best for complex reasoning
- **gpt-4o** - Balanced performance (recommended)
- **gpt-4.1** - Advanced coding and reasoning
- **o3-mini** - Cost-effective reasoning

## 🐛 Troubleshooting

### Backend Issues

1. **Import Error for agent_framework:**
   - Ensure you installed with `--pre` flag
   - Run: `pip install agent-framework-azure-ai --pre`

2. **Azure Authentication Errors:**
   - Verify your Azure credentials in `.env`
   - Check endpoint URLs are correct
   - Ensure model deployments exist

3. **PDF Extraction Fails:**
   - Install PyPDF2: `pip install PyPDF2`
   - Try converting PDF to text first

### Frontend Issues

1. **Cannot connect to backend:**
   - Verify backend is running on port 8000
   - Check `NEXT_PUBLIC_API_URL` in `.env.local`
   - Check CORS settings in backend

2. **Build errors:**
   - Delete `node_modules` and `.next` folders
   - Run `npm install` again
   - Ensure Node.js version is 18+

## 📚 Additional Resources

- [Microsoft Agent Framework Documentation](https://github.com/microsoft/agent-framework)
- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [CopilotKit Documentation](https://docs.copilotkit.ai/)
- [Next.js Documentation](https://nextjs.org/docs)

## 📝 License

This project is for demonstration purposes. Please review licenses for individual dependencies.

## 🤝 Contributing

This is a demonstration project. For production use, consider:
- Adding authentication and authorization
- Implementing database persistence
- Adding comprehensive error handling
- Setting up monitoring and logging
- Implementing actual email service
- Adding unit and integration tests

---

**Built with ❤️ using Microsoft Agent Framework and CopilotKit**

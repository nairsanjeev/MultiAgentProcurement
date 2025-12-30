# Project Summary: AI-Powered Procurement System

## Overview
A comprehensive procurement acceleration application demonstrating the power of **Microsoft Agent Framework** with the **Magentic Pattern** and **CopilotKit** for intelligent document processing and multi-agent workflows.

## Key Features Implemented

### ✅ Multi-Agent Architecture (Magentic Pattern)
1. **Document Extraction Agent** - Extracts quote information from uploaded documents
2. **Supplier Validation Agent** - Validates against approved supplier database
3. **Competitive Analysis Agent** - Analyzes quote competitiveness
4. **Purchase Order Agent** - Creates POs and manages approvals

### ✅ Technology Stack

**Backend:**
- Microsoft Agent Framework (Python) - Preview version with `--pre` flag
- FastAPI - REST API with streaming support
- Azure OpenAI / Microsoft Foundry integration
- Pydantic models for type safety
- Synthetic data for supplier validation

**Frontend:**
- Next.js 14 with TypeScript
- TailwindCSS for styling
- CopilotKit-ready architecture
- Responsive, modern UI with generative components
- Real-time processing feedback

### ✅ Complete Workflow Pipeline

```
User Upload → Document Extraction → Supplier Validation → 
Competitive Analysis → PO Creation → Approval Workflow
```

## Project Structure

```
ProcurementMagenticDemo/
├── backend/
│   ├── agents/                    # Multi-agent implementations
│   │   ├── document_extraction.py
│   │   ├── supplier_validation.py
│   │   ├── competitive_analysis.py
│   │   └── purchase_order.py
│   ├── data/
│   │   └── approved_suppliers.json  # 10 synthetic suppliers
│   ├── config.py                   # Configuration management
│   ├── models.py                   # Pydantic data models
│   ├── utils.py                    # Utility functions
│   ├── workflow.py                 # Magentic workflow orchestrator
│   ├── main.py                     # FastAPI server
│   ├── requirements.txt            # Python dependencies
│   └── .env.example                # Configuration template
├── frontend/
│   ├── app/
│   │   ├── page.tsx               # Main application
│   │   ├── layout.tsx             # Root layout
│   │   └── globals.css            # Styles
│   ├── components/                # React components
│   │   ├── FileUpload.tsx
│   │   ├── QuoteDisplay.tsx
│   │   ├── ValidationDisplay.tsx
│   │   ├── AnalysisDisplay.tsx
│   │   └── PurchaseOrderDisplay.tsx
│   ├── lib/
│   │   ├── types.ts               # TypeScript types
│   │   ├── api.ts                 # API client
│   │   └── utils.ts               # Utility functions
│   └── package.json
├── sample_documents/              # Test documents
│   ├── sample_quote_1.txt
│   └── sample_quote_2.txt
├── README.md                      # Full documentation
├── QUICKSTART.md                  # 5-minute setup guide
├── DEPLOYMENT.md                  # Production deployment guide
├── setup.ps1                      # Windows setup script
└── setup.sh                       # Linux/Mac setup script
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check endpoint
- `POST /api/upload` - Upload and extract document text
- `POST /api/process` - Process document through workflow (synchronous)
- `POST /api/process-stream` - Process with Server-Sent Events (streaming)
- `POST /api/approve` - Submit PO for approval

## Agents Implementation Details

### 1. Document Extraction Agent
- Uses GPT-4o with vision capabilities
- Extracts structured data from unstructured documents
- Returns JSON with quote details, items, pricing
- Handles both PDF and text documents

### 2. Supplier Validation Agent
- Loads synthetic supplier database (10 suppliers)
- Fuzzy matching for supplier names
- Validates approval status, ratings, certifications
- Returns detailed validation messages

### 3. Competitive Analysis Agent
- Simulates market research and competitive intelligence
- Analyzes pricing against market standards
- Provides confidence scores (0.0 - 1.0)
- Generates recommendations

### 4. Purchase Order Agent
- Aggregates all workflow results
- Generates unique PO numbers
- Determines approval requirements
- Prepares for email notifications

## Key Design Patterns

### Magentic Pattern (Agent Framework)
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

### Handler Pattern
```python
class Agent(Executor):
    @handler
    async def process(
        self, 
        input_data: InputType, 
        ctx: WorkflowContext[OutputType]
    ) -> None:
        # Process and forward
        await ctx.send_message(output_data)
```

### Streaming Events
```python
async for event in workflow.run_stream(input):
    if isinstance(event, WorkflowOutputEvent):
        # Handle output
    elif isinstance(event, WorkflowStatusEvent):
        # Handle status update
```

## Environment Configuration

### Backend (.env)
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
FOUNDRY_PROJECT_ENDPOINT=https://your-project.cognitiveservices.azure.com/
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4o
USE_AZURE_CREDENTIAL=false
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Setup Commands

### Quick Setup (Windows)
```powershell
.\setup.ps1
```

### Quick Setup (Linux/Mac)
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup
```bash
# Backend
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt --pre
cp .env.example .env
# Edit .env with your credentials
python main.py

# Frontend (new terminal)
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

## Testing

1. Start backend: `http://localhost:8000`
2. Start frontend: `http://localhost:3000`
3. Upload `sample_documents/sample_quote_1.txt`
4. Watch the multi-agent workflow process
5. Review results and submit for approval

## Production Considerations

### Security
- [ ] Add authentication (Azure AD)
- [ ] Implement API keys
- [ ] Enable HTTPS/SSL
- [ ] Add rate limiting
- [ ] Use Azure Key Vault

### Scalability
- [ ] Add database (Cosmos DB / Azure SQL)
- [ ] Implement caching (Redis)
- [ ] Use Azure API Management
- [ ] Configure auto-scaling
- [ ] Add load balancing

### Monitoring
- [ ] Application Insights integration
- [ ] Health check monitoring
- [ ] Cost tracking
- [ ] Performance metrics
- [ ] Error tracking

### Data Management
- [ ] Implement data persistence
- [ ] Add audit logging
- [ ] Configure backups
- [ ] Data retention policies
- [ ] GDPR compliance

## Customization Points

1. **Supplier Database** - Edit `backend/data/approved_suppliers.json`
2. **Agent Instructions** - Modify prompts in agent files
3. **Workflow Logic** - Update `backend/workflow.py`
4. **UI Components** - Customize `frontend/components/`
5. **Model Selection** - Change deployment names in `.env`

## Documentation

- **README.md** - Complete project documentation
- **QUICKSTART.md** - 5-minute setup guide
- **DEPLOYMENT.md** - Production deployment guide
- **Code Comments** - Inline documentation in all files

## Dependencies

### Backend (Python 3.10+)
- agent-framework-azure-ai (--pre required)
- fastapi, uvicorn
- python-dotenv
- pydantic
- PyPDF2, aiofiles, httpx

### Frontend (Node.js 18+)
- next@14, react@18
- @copilotkit/react-core, @copilotkit/react-ui
- axios
- tailwindcss
- lucide-react

## Success Criteria ✅

- [x] Multi-agent workflow using Microsoft Agent Framework
- [x] Magentic pattern implementation
- [x] Document extraction with vision models
- [x] Supplier validation with synthetic data
- [x] Competitive analysis simulation
- [x] Purchase order creation
- [x] Approval workflow
- [x] CopilotKit-ready frontend
- [x] Generative UI patterns
- [x] Environment configuration
- [x] Complete documentation
- [x] Sample documents
- [x] Setup automation

## Future Enhancements

1. **CopilotKit Chatbot** - Add conversational interface
2. **Real-time Streaming** - Implement SSE for live updates
3. **Email Integration** - Connect to actual email service
4. **OCR Support** - Add scanned document processing
5. **Multi-language** - Support for international quotes
6. **Analytics Dashboard** - Track procurement metrics
7. **Integration** - Connect to ERP systems
8. **Mobile App** - React Native frontend

## Resources

- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Microsoft Foundry](https://learn.microsoft.com/azure/ai-studio/)
- [CopilotKit](https://docs.copilotkit.ai/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)

---

**Built with ❤️ using Microsoft Agent Framework and CopilotKit**

*This project demonstrates enterprise-grade AI agent orchestration for procurement automation.*

# Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                    (Next.js + CopilotKit)                       │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ File Upload  │  │ Progress     │  │ Results      │        │
│  │ Component    │  │ Display      │  │ Display      │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │        CopilotKit Integration Layer (Future)              │ │
│  │  • Chatbot Interface                                      │ │
│  │  • Generative UI Components                               │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST API
                              │ axios client
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI SERVER                             │
│                    (Backend Orchestrator)                       │
│                                                                 │
│  Endpoints:                                                     │
│  • POST /api/process         → Sync processing                 │
│  • POST /api/process-stream  → SSE streaming                   │
│  • POST /api/upload          → Document upload                 │
│  • POST /api/approve         → PO approval                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Invokes
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              PROCUREMENT WORKFLOW ORCHESTRATOR                  │
│           (Microsoft Agent Framework - Magentic)                │
│                                                                 │
│  WorkflowBuilder()                                              │
│    .set_start_executor(document_extraction)                    │
│    .add_edge(document_extraction, supplier_validation)         │
│    .add_edge(supplier_validation, competitive_analysis)        │
│    .add_edge(competitive_analysis, purchase_order)             │
│    .build()                                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Executes Agents
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       AGENT PIPELINE                            │
│                    (4 Specialized Agents)                       │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  1. DOCUMENT EXTRACTION AGENT                             │ │
│  │     • Input: Raw document text                            │ │
│  │     • Process: GPT-4o extracts structured data            │ │
│  │     • Output: Quote object (supplier, items, prices)      │ │
│  │     • Handler: @handler async extract_from_text()         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  2. SUPPLIER VALIDATION AGENT                             │ │
│  │     • Input: Quote with supplier name                     │ │
│  │     • Process: Check approved suppliers DB                │ │
│  │     • Output: Validation status + details                 │ │
│  │     • Handler: @handler async validate_supplier()         │ │
│  │     • Data: approved_suppliers.json (10 suppliers)        │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  3. COMPETITIVE ANALYSIS AGENT                            │ │
│  │     • Input: Quote + validation results                   │ │
│  │     • Process: GPT-4o analyzes market competitiveness     │ │
│  │     • Output: Analysis with confidence score              │ │
│  │     • Handler: @handler async analyze_competitiveness()   │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  4. PURCHASE ORDER AGENT                                  │ │
│  │     • Input: All aggregated results                       │ │
│  │     • Process: Generate PO number, determine approval     │ │
│  │     • Output: Complete PO ready for approval              │ │
│  │     • Handler: @handler async create_purchase_order()     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Communicates with
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AZURE OPENAI / FOUNDRY                       │
│                                                                 │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │ Azure OpenAI     │   OR    │ Microsoft        │            │
│  │ Endpoint         │         │ Foundry Project  │            │
│  │                  │         │                  │            │
│  │ Model: gpt-4o    │         │ Model: gpt-4o    │            │
│  │ API Key Auth     │         │ Azure Credential │            │
│  └──────────────────┘         └──────────────────┘            │
│                                                                 │
│  Capabilities Used:                                             │
│  • Vision (document understanding)                              │
│  • JSON mode (structured extraction)                            │
│  • Function calling (tool use)                                  │
│  • Streaming responses                                          │
└─────────────────────────────────────────────────────────────────┘


## Data Flow Diagram

┌──────────┐
│  User    │
│  Uploads │
│ Document │
└────┬─────┘
     │
     ▼
┌─────────────────┐
│ Extract Text    │
│ (PDF/TXT)       │
└────┬────────────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│         Agent Pipeline (Magentic)           │
│                                             │
│  ┌──────────────────────────────┐          │
│  │ Document Extraction Agent    │          │
│  │ Extract: Quote Info          │          │
│  └──────────┬───────────────────┘          │
│             │                               │
│             ▼                               │
│  ┌──────────────────────────────┐          │
│  │ Supplier Validation Agent    │          │
│  │ Validate: Approved Supplier  │          │
│  └──────────┬───────────────────┘          │
│             │                               │
│             ▼                               │
│  ┌──────────────────────────────┐          │
│  │ Competitive Analysis Agent   │          │
│  │ Analyze: Price Competition   │          │
│  └──────────┬───────────────────┘          │
│             │                               │
│             ▼                               │
│  ┌──────────────────────────────┐          │
│  │ Purchase Order Agent         │          │
│  │ Create: PO + Approval Flow   │          │
│  └──────────┬───────────────────┘          │
│             │                               │
└─────────────┼───────────────────────────────┘
              │
              ▼
     ┌──────────────────┐
     │  Complete PO     │
     │  with:           │
     │  • Quote Details │
     │  • Validation    │
     │  • Analysis      │
     │  • Approval Info │
     └──────────────────┘


## Agent Communication Pattern

Each agent follows this pattern:

┌─────────────────────────────────────────────────┐
│              Executor (Agent)                   │
│                                                 │
│  @handler                                       │
│  async def process(                             │
│      input_data: InputType,                     │
│      ctx: WorkflowContext[OutputType]           │
│  ) -> None:                                     │
│      │                                           │
│      ├─► 1. Receive input from previous agent  │
│      │                                           │
│      ├─► 2. Process with LLM/Logic             │
│      │                                           │
│      ├─► 3. Format output                       │
│      │                                           │
│      └─► 4. Send to next agent                  │
│          await ctx.send_message(output)         │
│                                                 │
└─────────────────────────────────────────────────┘


## Technology Stack Layers

┌───────────────────────────────────────────────┐
│         PRESENTATION LAYER                    │
│  • Next.js 14 (React Framework)               │
│  • TailwindCSS (Styling)                      │
│  • TypeScript (Type Safety)                   │
│  • Lucide Icons (UI Icons)                    │
│  • CopilotKit (Future AI Integration)         │
└─────────────────┬─────────────────────────────┘
                  │
┌─────────────────┴─────────────────────────────┐
│         APPLICATION LAYER                     │
│  • FastAPI (REST API Server)                  │
│  • Uvicorn (ASGI Server)                      │
│  • Pydantic (Data Validation)                 │
│  • CORS Middleware                             │
└─────────────────┬─────────────────────────────┘
                  │
┌─────────────────┴─────────────────────────────┐
│         ORCHESTRATION LAYER                   │
│  • Microsoft Agent Framework                  │
│  • Magentic Pattern (WorkflowBuilder)         │
│  • Executor Classes                            │
│  • Handler Methods                             │
│  • Context Passing                             │
└─────────────────┬─────────────────────────────┘
                  │
┌─────────────────┴─────────────────────────────┐
│         AI/ML LAYER                           │
│  • Azure OpenAI Service                       │
│  • Microsoft Foundry                          │
│  • GPT-4o Model                               │
│  • Vision Capabilities                         │
│  • JSON Mode                                   │
└─────────────────┬─────────────────────────────┘
                  │
┌─────────────────┴─────────────────────────────┐
│         DATA LAYER                            │
│  • JSON Files (Supplier DB)                   │
│  • In-Memory Processing                        │
│  • Pydantic Models                             │
│  • (Future: Cosmos DB/SQL)                     │
└───────────────────────────────────────────────┘
```

## Workflow Execution Flow

```
START
  │
  ▼
┌─────────────────────────┐
│ User uploads document   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Backend extracts text   │
│ (PDF → text / TXT)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│ WorkflowBuilder creates agent pipeline  │
│ Sets start executor                     │
│ Links agents with edges                 │
└───────────┬─────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│ Workflow.run_stream(document_text)      │
│ • Emits events as processing occurs     │
│ • Each agent processes sequentially     │
└───────────┬─────────────────────────────┘
            │
            ├──► Event: WorkflowStatusEvent
            │    (IN_PROGRESS, IDLE, etc.)
            │
            ├──► Event: ExecutorInvokedEvent
            │    (Agent started)
            │
            ├──► Event: ExecutorCompletedEvent
            │    (Agent finished)
            │
            └──► Event: WorkflowOutputEvent
                 (Final result)
                      │
                      ▼
         ┌────────────────────────┐
         │ Return complete PO     │
         │ to frontend            │
         └────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │ Display results        │
         │ Allow user approval    │
         └────────────────────────┘
                      │
                      ▼
                    END
```

This architecture demonstrates:
- ✅ Separation of concerns (layered architecture)
- ✅ Loose coupling (agents communicate via messages)
- ✅ Scalability (agents can run in parallel)
- ✅ Extensibility (easy to add new agents)
- ✅ Observability (event streaming)
- ✅ Type safety (TypeScript + Pydantic)

"""
FastAPI Backend Server for Procurement Agent System
Provides REST API endpoints for the CopilotKit frontend.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import json
from typing import AsyncGenerator
from config import config
from workflow import ProcurementWorkflow
from utils import extract_text_from_pdf
from models import ProcessingStatus
from agent_framework import WorkflowOutputEvent, WorkflowStatusEvent, WorkflowRunState

# Initialize FastAPI app
app = FastAPI(
    title="Procurement Agent API",
    description="Multi-agent procurement system using Microsoft Agent Framework",
    version="1.0.0"
)

# Configure CORS
origins = [
    config.FRONTEND_URL,
    "http://localhost:3000",
    "http://localhost:3001",
    "https://*.azurewebsites.net"  # Allow Azure Web Apps
]

# In production, get allowed origins from environment or allow all Azure sites
import os
if os.getenv("AZURE_WEBAPP_NAME"):
    # Running in Azure, allow all origins for now (you should restrict this in production)
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize workflow (will be created on first request)
workflow: ProcurementWorkflow | None = None


def get_workflow() -> ProcurementWorkflow:
    """Get or create the workflow instance."""
    global workflow
    if workflow is None:
        workflow = ProcurementWorkflow()
    return workflow


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Procurement Agent API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "upload": "/api/upload",
            "process": "/api/process",
            "approve": "/api/approve"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "procurement-agent-api"}


@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and extract text from a procurement document.
    
    Supports PDF and text files.
    """
    try:
        # Read file content
        content = await file.read()
        
        # Extract text based on file type
        if file.filename.lower().endswith('.pdf'):
            document_text = extract_text_from_pdf(content)
        elif file.filename.lower().endswith('.txt'):
            document_text = content.decode('utf-8')
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload PDF or TXT files."
            )
        
        return {
            "success": True,
            "filename": file.filename,
            "text_length": len(document_text),
            "preview": document_text[:500] + ("..." if len(document_text) > 500 else "")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")


@app.post("/api/process")
async def process_document(file: UploadFile = File(...)):
    """
    Process a procurement document through the complete workflow.
    
    This is a non-streaming endpoint that returns the final result.
    """
    try:
        # Read and extract text from document
        content = await file.read()
        
        if file.filename.lower().endswith('.pdf'):
            document_text = extract_text_from_pdf(content)
        elif file.filename.lower().endswith('.txt'):
            document_text = content.decode('utf-8')
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload PDF or TXT files."
            )
        
        # Get workflow instance
        wf = get_workflow()
        
        # Process document
        result = await wf.process_document_sync(document_text)
        
        return JSONResponse(content={
            "success": True,
            "result": result
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.post("/api/process-stream")
async def process_document_stream(file: UploadFile = File(...)):
    """
    Process a procurement document with streaming updates.
    
    Returns Server-Sent Events (SSE) for real-time progress updates.
    """
    try:
        # Read and extract text from document
        content = await file.read()
        
        if file.filename.lower().endswith('.pdf'):
            document_text = extract_text_from_pdf(content)
        elif file.filename.lower().endswith('.txt'):
            document_text = content.decode('utf-8')
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload PDF or TXT files."
            )
        
        async def event_generator() -> AsyncGenerator[str, None]:
            """Generate SSE events from workflow."""
            try:
                wf = get_workflow()
                
                async for event in wf.process_document(document_text):
                    if isinstance(event, WorkflowOutputEvent):
                        # Send the final output
                        yield f"data: {json.dumps({'type': 'output', 'data': event.data})}\n\n"
                    elif isinstance(event, WorkflowStatusEvent):
                        # Send status updates
                        status = {
                            'type': 'status',
                            'state': event.state.value if hasattr(event.state, 'value') else str(event.state),
                            'executor': event.origin.value if hasattr(event.origin, 'value') else str(event.origin)
                        }
                        yield f"data: {json.dumps(status)}\n\n"
                    else:
                        # Send other events
                        event_data = {
                            'type': 'event',
                            'event_type': event.__class__.__name__,
                            'data': str(event)
                        }
                        yield f"data: {json.dumps(event_data)}\n\n"
                
                # Send completion event
                yield f"data: {json.dumps({'type': 'complete'})}\n\n"
                
            except Exception as e:
                error_data = {'type': 'error', 'message': str(e)}
                yield f"data: {json.dumps(error_data)}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.post("/api/approve")
async def approve_purchase_order(po_data: dict):
    """
    Approve a purchase order and send for processing.
    
    In a real system, this would:
    - Send email to approver
    - Update database
    - Trigger downstream systems
    """
    try:
        po_number = po_data.get("po_number")
        approver_email = po_data.get("approver_email", "approver@company.com")
        
        # Simulate approval process
        # In production, this would send actual emails and update systems
        
        return {
            "success": True,
            "message": f"Purchase order {po_number} has been submitted for approval",
            "approver_email": approver_email,
            "status": "pending_approval"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Approval failed: {str(e)}")


# Step-by-step processing with human validation
@app.post("/api/step/extract")
async def step_extract_document(file: UploadFile = File(...)):
    """Step 1: Extract quote from document and wait for user validation."""
    try:
        content = await file.read()
        
        if file.filename.lower().endswith('.pdf'):
            document_text = extract_text_from_pdf(content)
        elif file.filename.lower().endswith('.txt'):
            document_text = content.decode('utf-8')
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Direct extraction using Azure OpenAI
        from azure.core.credentials import AzureKeyCredential
        from agent_framework.azure import AzureOpenAIChatClient
        from agent_framework import ChatMessage, Role
        import json
        
        credential = AzureKeyCredential(config.AZURE_OPENAI_API_KEY)
        chat_client = AzureOpenAIChatClient(
            endpoint=config.AZURE_OPENAI_ENDPOINT,
            credential=credential,
            deployment_name=config.AZURE_OPENAI_DEPLOYMENT_NAME
        )
        
        # Create extraction agent
        agent = chat_client.create_agent(
            instructions="""You are an expert document parser specialized in extracting procurement quote information.

Extract the following from the document:
1. Supplier name and details
2. Quote number and date
3. List of items with quantities, prices
4. Total amount and currency

Return ONLY a valid JSON object with this structure:
{
    "supplier_name": "string",
    "supplier_id": "string or null",
    "quote_number": "string or null",
    "quote_date": "string or null",
    "currency": "USD",
    "items": [
        {
            "item_name": "string",
            "description": "string or null",
            "quantity": number,
            "unit_price": number,
            "total_price": number,
            "currency": "USD"
        }
    ],
    "total_amount": number
}"""
        )
        
        # Run extraction
        message = ChatMessage(
            role=Role.USER,
            text=f"Please extract the quote information from the following document:\n\n{document_text}"
        )
        
        response = await agent.run([message])
        extracted_text = response.text.strip()
        
        # Parse JSON response
        if extracted_text.startswith("```"):
            lines = extracted_text.split("\n")
            extracted_text = "\n".join(lines[1:-1])
        if extracted_text.startswith("json"):
            extracted_text = extracted_text[4:].strip()
        
        quote_data = json.loads(extracted_text)
        quote_data["raw_text"] = document_text[:500]
        
        return {
            "success": True,
            "step": "extraction",
            "data": quote_data
        }
        
    except Exception as e:
        import traceback
        print(f"Extraction error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@app.post("/api/step/validate")
async def step_validate_supplier(data: dict):
    """Step 2: Validate supplier and wait for user confirmation."""
    try:
        import json
        
        # Load approved suppliers
        with open("data/approved_suppliers.json", "r") as f:
            suppliers_data = json.load(f)
            approved_suppliers = suppliers_data.get("suppliers", [])
        
        supplier_name = data.get("supplier_name", "")
        
        # Find supplier (simple name matching)
        supplier_info = None
        for supplier in approved_suppliers:
            if supplier["name"].lower() == supplier_name.lower():
                supplier_info = supplier
                break
        
        # Build validation result
        if supplier_info:
            validation_data = {
                "supplier_name": supplier_info["name"],
                "is_approved": supplier_info["approved"],
                "supplier_id": supplier_info["id"],
                "rating": supplier_info["rating"],
                "certifications": supplier_info["certifications"],
                "validation_message": (
                    f"✓ {supplier_info['name']} is an approved supplier. "
                    f"Rating: {supplier_info['rating']}/5.0. "
                    f"Certifications: {', '.join(supplier_info['certifications']) if supplier_info['certifications'] else 'None'}."
                ) if supplier_info["approved"] else (
                    f"✗ {supplier_info['name']} is NOT an approved supplier. "
                    f"Rating: {supplier_info['rating']}/5.0."
                )
            }
        else:
            validation_data = {
                "supplier_name": supplier_name,
                "is_approved": False,
                "supplier_id": None,
                "rating": None,
                "certifications": [],
                "validation_message": (
                    f"✗ {supplier_name} is not found in our approved supplier database. "
                    f"This supplier has not been vetted."
                )
            }
        
        return {
            "success": True,
            "step": "validation",
            "data": validation_data
        }
        
    except Exception as e:
        import traceback
        print(f"Validation error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@app.post("/api/step/analyze")
async def step_analyze_competitiveness(data: dict):
    """Step 3: Analyze competitiveness and wait for user approval."""
    try:
        from azure.core.credentials import AzureKeyCredential
        from agent_framework.azure import AzureOpenAIChatClient
        from agent_framework import ChatMessage, Role
        import json
        
        credential = AzureKeyCredential(config.AZURE_OPENAI_API_KEY)
        chat_client = AzureOpenAIChatClient(
            endpoint=config.AZURE_OPENAI_ENDPOINT,
            credential=credential,
            deployment_name=config.AZURE_OPENAI_DEPLOYMENT_NAME
        )
        
        # Create analysis agent
        agent = chat_client.create_agent(
            instructions="""You are a quick procurement analyst. 
Analyze pricing competitiveness FAST. 
Be quick and concise. 
Make a fast decision.

Return ONLY a JSON object with this structure:
{
    "is_competitive": true/false,
    "price_comparison": "brief comparison",
    "recommendation": "approve/reject with brief reason",
    "confidence_score": 0.0-1.0
}"""
        )
        
        # Prepare analysis prompt
        supplier_name = data.get("supplier_name", "Unknown")
        total_amount = data.get("total_amount", 0)
        currency = data.get("currency", "USD")
        items = data.get("items", [])
        
        items_text = "\n".join([
            f"- {item['item_name']}: {item['quantity']} x {currency} {item['unit_price']} = {currency} {item['total_price']}"
            for item in items
        ])
        
        prompt = f"""Analyze this quote for competitiveness:

Supplier: {supplier_name}
Total: {currency} {total_amount}

Items:
{items_text}

Is this pricing competitive? Should we approve?"""
        
        message = ChatMessage(role=Role.USER, text=prompt)
        response = await agent.run([message])
        
        # Parse response
        extracted_text = response.text.strip()
        if extracted_text.startswith("```"):
            lines = extracted_text.split("\n")
            extracted_text = "\n".join(lines[1:-1])
        if extracted_text.startswith("json"):
            extracted_text = extracted_text[4:].strip()
        
        analysis_data = json.loads(extracted_text)
        
        return {
            "success": True,
            "step": "analysis",
            "data": analysis_data
        }
        
    except Exception as e:
        import traceback
        print(f"Analysis error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/step/create-po")
async def step_create_purchase_order(data: dict):
    """Step 4: Create purchase order after all validations."""
    try:
        from datetime import datetime
        import uuid
        
        # Generate PO number
        po_number = f"PO-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Build PO data
        po_data = {
            "po_number": po_number,
            "status": "pending_approval",
            "created_at": datetime.now().isoformat(),
            "approver_email": "procurement@company.com",
            "approval_required": True
        }
        
        return {
            "success": True,
            "step": "purchase_order",
            "data": po_data
        }
        
    except Exception as e:
        import traceback
        print(f"PO creation error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"PO creation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    config.validate()
    
    print(f"Starting Procurement Agent API on port {config.BACKEND_PORT}")
    print(f"Frontend URL: {config.FRONTEND_URL}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.BACKEND_PORT,
        reload=True
    )

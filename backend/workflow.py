"""
Procurement Workflow Orchestrator
Orchestrates the multi-agent procurement workflow using Magentic pattern.
"""
from agent_framework import WorkflowBuilder
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from config import config
from agents.document_extraction import DocumentExtractionAgent
from agents.supplier_validation import SupplierValidationAgent
from agents.competitive_analysis import CompetitiveAnalysisAgent
from agents.purchase_order import PurchaseOrderAgent


class ProcurementWorkflow:
    """
    Main workflow orchestrator for the procurement process.
    Implements the Magentic pattern with multiple specialized agents.
    """
    
    def __init__(self):
        """Initialize the workflow with all agents."""
        # Initialize chat client based on configuration
        if config.USE_AZURE_CREDENTIAL:
            credential = DefaultAzureCredential()
            self.chat_client = AzureOpenAIChatClient(
                endpoint=config.AZURE_OPENAI_ENDPOINT,
                credential=credential,
                deployment_name=config.AZURE_OPENAI_DEPLOYMENT_NAME
            )
        else:
            credential = AzureKeyCredential(config.AZURE_OPENAI_API_KEY)
            self.chat_client = AzureOpenAIChatClient(
                endpoint=config.AZURE_OPENAI_ENDPOINT,
                credential=credential,
                deployment_name=config.AZURE_OPENAI_DEPLOYMENT_NAME
            )
        
        # Create agent executors
        self.document_extraction = DocumentExtractionAgent(self.chat_client)
        self.supplier_validation = SupplierValidationAgent(self.chat_client)
        self.competitive_analysis = CompetitiveAnalysisAgent(self.chat_client)
        self.purchase_order = PurchaseOrderAgent(self.chat_client)
        
        # Build the workflow graph
        # Document -> Validation -> Analysis -> PO Creation
        self.workflow = (
            WorkflowBuilder()
            .set_start_executor(self.document_extraction)
            .add_edge(self.document_extraction, self.supplier_validation)
            .add_edge(self.supplier_validation, self.competitive_analysis)
            .add_edge(self.competitive_analysis, self.purchase_order)
            .build()
        )
    
    async def process_document(self, document_text: str):
        """
        Process a procurement document through the complete workflow.
        
        Args:
            document_text: Extracted text from the uploaded document
            
        Returns:
            Workflow output with purchase order and analysis
        """
        # Run the workflow with streaming to get all events
        events = []
        async for event in self.workflow.run_stream(document_text):
            events.append(event)
            yield event
    
    async def process_document_sync(self, document_text: str):
        """
        Process a document synchronously (non-streaming).
        
        Args:
            document_text: Extracted text from the uploaded document
            
        Returns:
            Final workflow output
        """
        result = await self.workflow.run(document_text)
        outputs = result.get_outputs()
        return outputs[0] if outputs else None

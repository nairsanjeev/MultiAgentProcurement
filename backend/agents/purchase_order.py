"""
Purchase Order Agent
Creates purchase orders and handles approval workflows.
"""
from agent_framework import Executor, WorkflowContext, handler
from agent_framework.azure import AzureOpenAIChatClient
from typing_extensions import Never
from models import PurchaseOrder, Quote, SupplierValidation, CompetitiveAnalysis
from utils import generate_po_number


class PurchaseOrderAgent(Executor):
    """
    Agent that creates purchase orders and manages approval workflow.
    """
    
    def __init__(self, chat_client: AzureOpenAIChatClient, id: str = "purchase_order"):
        self.chat_client = chat_client
        super().__init__(id=id)
    
    @handler
    async def create_purchase_order(
        self,
        data: dict,
        ctx: WorkflowContext[Never, dict]
    ) -> None:
        """Create a purchase order from validated quote and analysis."""
        
        quote_data = data.get("quote", {})
        validation_data = data.get("validation", {})
        analysis_data = data.get("analysis", {})
        
        # Create Quote object
        quote = Quote(**quote_data)
        
        # Create SupplierValidation object
        validation = SupplierValidation(**validation_data)
        
        # Create CompetitiveAnalysis object
        analysis = CompetitiveAnalysis(**analysis_data)
        
        # Generate PO number
        po_number = generate_po_number()
        
        # Create Purchase Order
        purchase_order = PurchaseOrder(
            po_number=po_number,
            quote=quote,
            supplier_validation=validation,
            competitive_analysis=analysis,
            status="pending_approval"
        )
        
        # Yield the final workflow output
        await ctx.yield_output({
            "type": "purchase_order_created",
            "purchase_order": purchase_order.model_dump(),
            "approval_required": not (validation.is_approved and analysis.is_competitive),
            "messages": data.get("messages", [])
        })

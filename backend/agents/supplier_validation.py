"""
Supplier Validation Agent
Validates if the supplier is in the approved supplier list.
"""
from agent_framework import Executor, WorkflowContext, handler, ChatMessage, Role
from agent_framework.azure import AzureOpenAIChatClient
from models import SupplierValidation
from utils import load_approved_suppliers, find_supplier_by_name


class SupplierValidationAgent(Executor):
    """
    Agent that validates suppliers against the approved supplier list.
    """
    
    def __init__(self, chat_client: AzureOpenAIChatClient, id: str = "supplier_validation"):
        self.chat_client = chat_client
        self.approved_suppliers = load_approved_suppliers()
        self.agent = chat_client.create_agent(
            instructions="""You are a supplier compliance validator.

Your task is to:
1. Check if the supplier is in the approved supplier list
2. Verify their rating and certifications
3. Provide a clear validation message

Be professional and thorough in your validation."""
        )
        super().__init__(id=id)
    
    @handler
    async def validate_supplier(
        self,
        data: dict,
        ctx: WorkflowContext[dict]
    ) -> None:
        """Validate the supplier from the extracted quote."""
        
        quote_data = data.get("quote", {})
        supplier_name = quote_data.get("supplier_name", "")
        
        # Find the supplier in approved list
        supplier_info = find_supplier_by_name(supplier_name, self.approved_suppliers)
        
        if supplier_info:
            # Supplier found in approved list
            validation = SupplierValidation(
                supplier_name=supplier_info["name"],
                is_approved=supplier_info["approved"],
                supplier_id=supplier_info["id"],
                rating=supplier_info["rating"],
                certifications=supplier_info["certifications"],
                validation_message=(
                    f"✓ {supplier_info['name']} is an approved supplier. "
                    f"Rating: {supplier_info['rating']}/5.0. "
                    f"Certifications: {', '.join(supplier_info['certifications']) if supplier_info['certifications'] else 'None'}."
                ) if supplier_info["approved"] else (
                    f"✗ {supplier_info['name']} is NOT an approved supplier. "
                    f"Rating: {supplier_info['rating']}/5.0. This supplier has not met our approval criteria."
                )
            )
        else:
            # Supplier not found
            validation = SupplierValidation(
                supplier_name=supplier_name,
                is_approved=False,
                validation_message=(
                    f"✗ {supplier_name} is not found in our approved supplier database. "
                    f"This supplier has not been vetted and cannot be used for procurement."
                )
            )
        
        # Prepare next message
        messages = data.get("messages", [])
        validation_msg = ChatMessage(
            role=Role.ASSISTANT,
            text=f"Supplier Validation Result:\n{validation.validation_message}"
        )
        messages.append(validation_msg)
        
        # Send validation result to next agent
        await ctx.send_message({
            "type": "supplier_validated",
            "quote": quote_data,
            "validation": validation.model_dump(),
            "messages": messages
        })

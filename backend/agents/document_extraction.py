"""
Document Extraction Agent
Extracts quote information from uploaded documents using vision-capable models.
"""
import json
from typing import List
from agent_framework import Executor, WorkflowContext, handler, ChatMessage, Role
from agent_framework.azure import AzureOpenAIChatClient
from models import Quote, QuoteItem
from utils import extract_text_from_pdf


class DocumentExtractionAgent(Executor):
    """
    Agent that extracts quote information from document text.
    Uses GPT-4o with vision capabilities to parse document content.
    """
    
    def __init__(self, chat_client: AzureOpenAIChatClient, id: str = "document_extraction"):
        self.chat_client = chat_client
        self.agent = chat_client.create_agent(
            instructions="""You are an expert document parser specialized in extracting procurement quote information.

Your task is to analyze the provided document text and extract:
1. Supplier name and details
2. Quote number and date
3. List of items with:
   - Item name/description
   - Quantity
   - Unit price
   - Total price
4. Total amount
5. Currency

IMPORTANT: Return the extracted information as a valid JSON object with this exact structure:
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
}

If you cannot extract certain information, use null for optional fields.
Ensure all prices are numeric values (not strings).
Return ONLY the JSON object, no additional text or markdown formatting."""
        )
        super().__init__(id=id)
    
    @handler
    async def extract_from_text(
        self, 
        document_text: str, 
        ctx: WorkflowContext[dict]
    ) -> None:
        """Extract quote information from document text."""
        
        # Create a message with the document text
        message = ChatMessage(
            role=Role.USER,
            text=f"Please extract the quote information from the following document:\n\n{document_text}"
        )
        
        # Run the agent to extract information
        response = await self.agent.run([message])
        extracted_text = response.text.strip()
        
        # Try to parse the JSON response
        try:
            # Remove markdown code blocks if present
            if extracted_text.startswith("```"):
                lines = extracted_text.split("\n")
                extracted_text = "\n".join(lines[1:-1])
            if extracted_text.startswith("json"):
                extracted_text = extracted_text[4:].strip()
            
            quote_data = json.loads(extracted_text)
            quote_data["raw_text"] = document_text[:500]  # Store first 500 chars
            
            # Send the extracted quote data to the next agent
            await ctx.send_message({
                "type": "quote_extracted",
                "quote": quote_data,
                "messages": [message] + response.messages
            })
            
        except json.JSONDecodeError as e:
            # If parsing fails, send error
            await ctx.send_message({
                "type": "extraction_error",
                "error": f"Failed to parse extracted quote: {str(e)}",
                "raw_response": extracted_text
            })

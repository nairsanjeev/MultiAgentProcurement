"""
Competitive Analysis Agent
Analyzes if the quote is competitive compared to market prices.
"""
import json
from agent_framework import Executor, WorkflowContext, handler, ChatMessage, Role
from agent_framework.azure import AzureOpenAIChatClient
from models import CompetitiveAnalysis


class CompetitiveAnalysisAgent(Executor):
    """
    Agent that performs competitive analysis on quotes.
    Simulates market research to determine if pricing is competitive.
    """
    
    def __init__(self, chat_client: AzureOpenAIChatClient, id: str = "competitive_analysis"):
        self.chat_client = chat_client
        self.agent = chat_client.create_agent(
            instructions="""You are a quick procurement analyst. Analyze pricing competitiveness FAST.

Provide ONLY a JSON object (no markdown):
{
    "is_competitive": boolean,
    "market_price_range": "brief range",
    "price_comparison": "1-2 sentences max",
    "recommendation": "1 sentence",
    "confidence_score": number 0.0-1.0
}

Be quick and concise. Make a fast decision based on item type and pricing."""
        )
        super().__init__(id=id)
    
    @handler
    async def analyze_competitiveness(
        self,
        data: dict,
        ctx: WorkflowContext[dict]
    ) -> None:
        """Analyze if the quote is competitive."""
        
        quote_data = data.get("quote", {})
        validation_data = data.get("validation", {})
        
        # Prepare the quote summary for analysis
        items_summary = []
        for item in quote_data.get("items", []):
            items_summary.append(
                f"- {item['item_name']}: {item['quantity']} units @ ${item['unit_price']} each = ${item['total_price']}"
            )
        
        quote_summary = f"""
Supplier: {quote_data.get('supplier_name')}
Total Amount: ${quote_data.get('total_amount')} {quote_data.get('currency', 'USD')}

Items:
{chr(10).join(items_summary)}

Supplier Validation: {'Approved' if validation_data.get('is_approved') else 'Not Approved'}
Supplier Rating: {validation_data.get('rating', 'Unknown')}
"""
        
        # Create message for analysis
        message = ChatMessage(
            role=Role.USER,
            text=f"Please analyze the competitiveness of this quote:\n\n{quote_summary}"
        )
        
        messages = data.get("messages", [])
        messages.append(message)
        
        # Run the agent to perform analysis
        response = await self.agent.run(messages)
        analysis_text = response.text.strip()
        
        try:
            # Remove markdown code blocks if present
            if analysis_text.startswith("```"):
                lines = analysis_text.split("\n")
                analysis_text = "\n".join(lines[1:-1])
            if analysis_text.startswith("json"):
                analysis_text = analysis_text[4:].strip()
            
            analysis_data = json.loads(analysis_text)
            
            messages.extend(response.messages)
            
            # Send analysis result to next step
            await ctx.send_message({
                "type": "analysis_complete",
                "quote": quote_data,
                "validation": validation_data,
                "analysis": analysis_data,
                "messages": messages
            })
            
        except json.JSONDecodeError as e:
            # If parsing fails, create a default analysis
            analysis_data = {
                "is_competitive": True,
                "market_price_range": "Unable to determine",
                "price_comparison": analysis_text[:200],
                "recommendation": "Manual review recommended",
                "confidence_score": 0.3
            }
            
            messages.extend(response.messages)
            
            await ctx.send_message({
                "type": "analysis_complete",
                "quote": quote_data,
                "validation": validation_data,
                "analysis": analysis_data,
                "messages": messages
            })

"""Test script to debug document extraction"""
import asyncio
from config import config
from azure.core.credentials import AzureKeyCredential
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import ChatMessage, Role
import json

async def test_extraction():
    try:
        print("Testing Azure OpenAI connection...")
        print(f"Endpoint: {config.AZURE_OPENAI_ENDPOINT}")
        print(f"Deployment: {config.AZURE_OPENAI_DEPLOYMENT_NAME}")
        
        credential = AzureKeyCredential(config.AZURE_OPENAI_API_KEY)
        client = AzureOpenAIChatClient(
            endpoint=config.AZURE_OPENAI_ENDPOINT,
            credential=credential,
            deployment_name=config.AZURE_OPENAI_DEPLOYMENT_NAME
        )
        
        print("\nCreating agent...")
        agent = client.create_agent(
            instructions="""You are a document parser. Extract quote information and return as JSON."""
        )
        
        print("\nSending test message...")
        test_document = """
        INVOICE #12345
        Supplier: Acme Corporation
        Date: 2025-01-15
        
        Items:
        1. Office Chairs - Qty: 10 @ $150.00 = $1,500.00
        2. Desk Lamps - Qty: 20 @ $45.00 = $900.00
        
        Total: $2,400.00 USD
        """
        
        msg = ChatMessage(
            role=Role.USER,
            text=f"Extract quote info as JSON: {test_document}"
        )
        
        response = await agent.run([msg])
        print("\n=== RESPONSE ===")
        print(response.text)
        print("\n=== SUCCESS ===")
        
    except Exception as e:
        print("\n=== ERROR ===")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_extraction())

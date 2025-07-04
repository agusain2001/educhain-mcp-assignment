#!/usr/bin/env python3
"""
Test script for the EduChain MCP Server

This script tests the MCP server functionality by calling its tools directly.
"""

import asyncio
import subprocess
import json
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def test_mcp_server():
    """Test the EduChain MCP server functionality."""
    
    print("Testing EduChain MCP Server...")
    
    # Start the MCP server as a subprocess
    server_params = StdioServerParameters(
        command="python3.11",
        args=["mcp_educhain_server.py"]
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()
                print("✓ MCP server initialized successfully")
                
                # List available tools
                tools = await session.list_tools()
                print(f"✓ Available tools: {[tool.name for tool in tools.tools]}")
                
                # List available resources
                resources = await session.list_resources()
                print(f"✓ Available resources: {[resource.uri for resource in resources.resources]}")
                
                # Test generate_mcqs tool
                print("\n--- Testing generate_mcqs tool ---")
                mcq_result = await session.call_tool(
                    "generate_mcqs", 
                    {"topic": "Python loops", "num_questions": 3}
                )
                print("✓ MCQ generation successful")
                print(f"MCQ Result: {mcq_result.content[0].text[:200]}...")
                
                # Test generate_lesson_plan tool
                print("\n--- Testing generate_lesson_plan tool ---")
                lesson_result = await session.call_tool(
                    "generate_lesson_plan",
                    {"topic": "Basic Algebra", "duration": "45 minutes"}
                )
                print("✓ Lesson plan generation successful")
                print(f"Lesson Plan Result: {lesson_result.content[0].text[:200]}...")
                
                # Test generate_flashcards tool
                print("\n--- Testing generate_flashcards tool ---")
                flashcard_result = await session.call_tool(
                    "generate_flashcards",
                    {"topic": "Python data types", "num_cards": 5}
                )
                print("✓ Flashcard generation successful")
                print(f"Flashcard Result: {flashcard_result.content[0].text[:200]}...")
                
                # Test resources
                print("\n--- Testing resources ---")
                status_resource = await session.read_resource("educhain://status")
                print(f"✓ Status resource: {status_resource.contents[0].text}")
                
                capabilities_resource = await session.read_resource("educhain://capabilities")
                print(f"✓ Capabilities resource: {capabilities_resource.contents[0].text[:200]}...")
                
                print("\n🎉 All tests passed! MCP server is working correctly.")
                
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_mcp_server())
    if success:
        print("\n✅ MCP server test completed successfully!")
    else:
        print("\n❌ MCP server test failed!")


#!/usr/bin/env python3
"""
MCP Server for EduChain Integration

This server exposes EduChain functionality through the Model Context Protocol,
allowing Claude Desktop to generate educational content using EduChain.
"""

import asyncio
import json
import os
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP
from educhain import Educhain, LLMConfig
from langchain_openai import ChatOpenAI

# Set the OPENAI_API_KEY to the OpenRouter key for EduChain
os.environ["OPENAI_API_KEY"] = ""

# Initialize EduChain with OpenRouter DeepSeek model
deepseek_model = ChatOpenAI(
    model="deepseek/deepseek-chat-v3-0324:free",
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.1
)

deepseek_config = LLMConfig(custom_model=deepseek_model)
educhain_client = Educhain(deepseek_config)

# Create MCP server
mcp = FastMCP("EduChain MCP Server")

@mcp.tool()
def generate_mcqs(topic: str, num_questions: int = 5, difficulty_level: str = "Medium") -> str:
    """
    Generate multiple choice questions on a given topic using EduChain.
    
    Args:
        topic: The topic for which to generate questions
        num_questions: Number of questions to generate (default: 5)
        difficulty_level: Difficulty level (Easy, Medium, Hard)
    
    Returns:
        JSON string containing the generated MCQs
    """
    try:
        questions = educhain_client.qna_engine.generate_questions(
            topic=topic,
            num=num_questions,
            question_type="Multiple Choice",
            difficulty_level=difficulty_level
        )
        return questions.model_dump_json(indent=2)
    except Exception as e:
        return f"Error generating MCQs: {str(e)}"

@mcp.tool()
def generate_lesson_plan(topic: str, duration: str = "60 minutes", grade_level: str = "Intermediate") -> str:
    """
    Generate a lesson plan for a given topic using EduChain.
    
    Args:
        topic: The topic for the lesson plan
        duration: Duration of the lesson (default: "60 minutes")
        grade_level: Target grade level (Beginner, Intermediate, Advanced)
    
    Returns:
        JSON string containing the generated lesson plan
    """
    try:
        lesson_plan = educhain_client.content_engine.generate_lesson_plan(
            topic=topic,
            duration=duration,
            grade_level=grade_level
        )
        return lesson_plan.model_dump_json(indent=2)
    except Exception as e:
        return f"Error generating lesson plan: {str(e)}"

@mcp.tool()
def generate_flashcards(topic: str, num_cards: int = 10) -> str:
    """
    Generate flashcards for a given topic using EduChain.
    
    Args:
        topic: The topic for which to generate flashcards
        num_cards: Number of flashcards to generate (default: 10)
    
    Returns:
        JSON string containing the generated flashcards
    """
    try:
        # Use the QnA engine to generate short answer questions that can serve as flashcards
        questions = educhain_client.qna_engine.generate_questions(
            topic=topic,
            num=num_cards,
            question_type="Short Answer",
            custom_instructions="Generate questions suitable for flashcards with concise answers"
        )
        return questions.model_dump_json(indent=2)
    except Exception as e:
        return f"Error generating flashcards: {str(e)}"

@mcp.resource("educhain://status")
def get_server_status() -> str:
    """Get the current status of the EduChain MCP server."""
    return "EduChain MCP Server is running and ready to generate educational content."

@mcp.resource("educhain://capabilities")
def get_capabilities() -> str:
    """Get the capabilities of the EduChain MCP server."""
    capabilities = {
        "tools": [
            "generate_mcqs - Generate multiple choice questions",
            "generate_lesson_plan - Generate lesson plans",
            "generate_flashcards - Generate flashcards"
        ],
        "supported_question_types": [
            "Multiple Choice",
            "Short Answer",
            "True/False",
            "Fill in the Blank"
        ],
        "supported_difficulty_levels": [
            "Easy",
            "Medium", 
            "Hard"
        ]
    }
    return json.dumps(capabilities, indent=2)

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()


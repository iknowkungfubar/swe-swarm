"""
Agent module for Gastown Swarm.

Provides various agent types including:
- BaseAgent: Abstract base class for all agents
- MockAgent: Mock agent for testing
- LLMAgent: LLM-backed intelligent agent
- ContentWriterAgent: Specialized agent for content writing
"""

from .base_agent import AgentMessage, AgentResponse, BaseAgent
from .mock_agent import MockAgent
from .llm_agent import LLMAgent
from .content_writer_agent import ContentWriterAgent

__all__ = [
    # Base classes
    "AgentMessage",
    "AgentResponse",
    "BaseAgent",
    # Implementations
    "MockAgent",
    "LLMAgent",
    "ContentWriterAgent",
]

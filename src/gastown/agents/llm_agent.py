"""
LLM-backed agent for Gastown Swarm.

This agent uses LLM providers to generate intelligent responses.
"""

import json
from typing import Any, AsyncGenerator, Dict, List, Optional

from loguru import logger

from ..llm import LLMProvider, LLMRequest, LLMResponse, LLMRouter
from .base_agent import AgentMessage, AgentResponse, BaseAgent


class LLMAgent(BaseAgent):
    """
    Base class for LLM-backed agents.
    
    Uses LLM providers to generate responses based on the agent's role and system prompt.
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        system_prompt: str,
        llm_router: Optional[LLMRouter] = None,
        llm_provider: Optional[LLMProvider] = None,
        task_type: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ):
        """
        Initialize an LLM-backed agent.
        
        Args:
            name: Agent name
            role: Agent role (e.g., "developer", "reviewer", "analyst")
            system_prompt: System prompt defining agent behavior
            llm_router: Optional LLM router for intelligent provider selection
            llm_provider: Optional direct LLM provider (if no router)
            task_type: Task type for routing decisions
            temperature: LLM temperature setting
            max_tokens: Maximum tokens to generate
        """
        super().__init__(name, role, system_prompt)
        self.llm_router = llm_router
        self.llm_provider = llm_provider
        self.task_type = task_type
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.conversation_history: List[Dict[str, str]] = []
        
        if not llm_router and not llm_provider:
            logger.warning(
                f"LLMAgent '{name}' initialized without LLM provider. "
                "Set llm_router or llm_provider before use."
            )
    
    def set_llm_provider(self, provider: LLMProvider) -> None:
        """Set the LLM provider directly."""
        self.llm_provider = provider
    
    def set_llm_router(self, router: LLMRouter) -> None:
        """Set the LLM router for intelligent routing."""
        self.llm_router = router
    
    def _build_messages(self, prompt: str) -> List[Dict[str, str]]:
        """Build messages array for LLM including conversation history."""
        messages = []
        
        # Add system prompt
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        
        # Add conversation history (last N messages to stay within context)
        history_limit = 10  # Keep last 10 messages for context
        for msg in self.conversation_history[-history_limit:]:
            messages.append(msg)
        
        # Add current user message
        messages.append({"role": "user", "content": prompt})
        
        return messages
    
    def _update_history(self, user_message: str, assistant_response: str) -> None:
        """Update conversation history with new exchange."""
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_response})
        
        # Keep history bounded
        max_history = 50  # Max 50 messages (25 exchanges)
        if len(self.conversation_history) > max_history:
            self.conversation_history = self.conversation_history[-max_history:]
    
    async def _get_llm_response(self, prompt: str) -> LLMResponse:
        """Get response from LLM using router or direct provider."""
        request = LLMRequest(
            prompt=prompt,
            system_prompt=self.system_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        
        if self.llm_router:
            return await self.llm_router.complete(request, task_type=self.task_type)
        elif self.llm_provider:
            return await self.llm_provider.complete(request)
        else:
            raise RuntimeError(
                f"Agent '{self.name}' has no LLM provider configured. "
                "Call set_llm_provider() or set_llm_router() first."
            )
    
    async def _stream_llm_response(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream response from LLM."""
        request = LLMRequest(
            prompt=prompt,
            system_prompt=self.system_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        
        if self.llm_router:
            async for chunk in self.llm_router.stream_complete(request, task_type=self.task_type):
                yield chunk.content
        elif self.llm_provider:
            async for chunk in self.llm_provider.stream_complete(request):
                yield chunk.content
        else:
            raise RuntimeError(
                f"Agent '{self.name}' has no LLM provider configured."
            )
    
    async def process_message(self, message: AgentMessage) -> AgentResponse:
        """
        Process an incoming message using LLM.
        
        The message content is sent to the LLM along with the agent's system prompt
        and conversation history.
        """
        logger.debug(f"{self.name} processing message: {message.id}")
        
        try:
            # Get LLM response
            llm_response = await self._get_llm_response(message.content)
            
            # Update conversation history
            self._update_history(message.content, llm_response.content)
            
            # Parse response for structured data if JSON
            response_data = {"response": llm_response.content}
            try:
                # Try to parse as JSON for structured responses
                parsed = json.loads(llm_response.content)
                response_data["parsed"] = parsed
            except json.JSONDecodeError:
                pass  # Not JSON, use raw text
            
            return AgentResponse(
                success=True,
                data={
                    **response_data,
                    "model": llm_response.model,
                    "provider": llm_response.provider,
                    "usage": llm_response.usage,
                },
                next_action="continue",
            )
            
        except Exception as e:
            logger.error(f"{self.name} error processing message: {e}")
            return AgentResponse(
                success=False,
                error=str(e),
                next_action="retry",
            )
    
    async def perform_task(self, task: Dict[str, Any]) -> AgentResponse:
        """
        Perform a specific task using LLM.
        
        The task dict is formatted as a prompt and sent to the LLM.
        """
        task_id = task.get("id", "unknown")
        task_description = task.get("description", "")
        task_context = task.get("context", {})
        
        logger.debug(f"{self.name} performing task: {task_id}")
        
        # Build task prompt
        prompt_parts = []
        if task_description:
            prompt_parts.append(f"Task: {task_description}")
        if task_context:
            prompt_parts.append(f"Context: {json.dumps(task_context, indent=2)}")
        
        task_prompt = "\n\n".join(prompt_parts) if prompt_parts else json.dumps(task)
        
        try:
            # Get LLM response
            llm_response = await self._get_llm_response(task_prompt)
            
            return AgentResponse(
                success=True,
                data={
                    "task_completed": True,
                    "response": llm_response.content,
                    "model": llm_response.model,
                    "provider": llm_response.provider,
                    "task_id": task_id,
                },
                next_action="complete",
            )
            
        except Exception as e:
            logger.error(f"{self.name} error performing task {task_id}: {e}")
            return AgentResponse(
                success=False,
                error=str(e),
                next_action="retry",
            )
    
    async def think(self, problem: str) -> str:
        """
        Use LLM to think through a problem.
        
        This is a simpler interface for when you just need the LLM's thoughts.
        """
        thinking_prompt = f"Think through this step by step:\n\n{problem}"
        response = await self._get_llm_response(thinking_prompt)
        return response.content
    
    async def review(self, content: str, instructions: Optional[str] = None) -> str:
        """
        Use LLM to review content.
        
        Args:
            content: The content to review
            instructions: Optional specific review instructions
        """
        review_prompt = f"Please review the following:\n\n{content}"
        if instructions:
            review_prompt += f"\n\nReview criteria: {instructions}"
        
        response = await self._get_llm_response(review_prompt)
        return response.content
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history.clear()
        logger.debug(f"{self.name} cleared conversation history")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status including LLM info."""
        status = super().get_status()
        status.update({
            "has_llm_provider": self.llm_provider is not None,
            "has_llm_router": self.llm_router is not None,
            "task_type": self.task_type,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "conversation_length": len(self.conversation_history),
        })
        return status

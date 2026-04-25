"""
Content Writer Agent for Gastown Swarm.

Specialized agent for writing content (articles, blogs, etc.)
"""

from typing import Any, Optional

from loguru import logger

from ..llm import LLMProvider, LLMRouter
from .llm_agent import LLMAgent


class ContentWriterAgent(LLMAgent):
    """Agent specialized in content writing."""
    
    def __init__(
        self,
        name: str = "content_writer",
        role: str = "content_writer",
        system_prompt: Optional[str] = None,
        llm_router: Optional[LLMRouter] = None,
        llm_provider: Optional[LLMProvider] = None,
        task_type: str = "writing",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        writing_style: str = "professional",
        target_audience: str = "general",
    ):
        """
        Initialize a content writer agent.
        
        Args:
            writing_style: Style of writing (professional, casual, technical, etc.)
            target_audience: Target audience for the content
        """
        if system_prompt is None:
            system_prompt = self._generate_system_prompt(writing_style, target_audience)
        
        super().__init__(
            name=name,
            role=role,
            system_prompt=system_prompt,
            llm_router=llm_router,
            llm_provider=llm_provider,
            task_type=task_type,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        self.writing_style = writing_style
        self.target_audience = target_audience
        logger.info(f"ContentWriterAgent initialized with style={writing_style}, audience={target_audience}")
    
    def _generate_system_prompt(self, writing_style: str, target_audience: str) -> str:
        """Generate system prompt based on writing style and target audience."""
        return f"""You are an expert content writer with a {writing_style} writing style.
Your target audience is {target_audience}.
You specialize in creating engaging, well-structured content that is:
- Clear and concise
- Well-organized with logical flow
- Factually accurate (or clearly fictional when appropriate)
- Tailored to the specified audience
- Free of plagiarism
- SEO-friendly when required

When given a writing task, you will:
1. Analyze the requirements and topic
2. Create an outline if needed
3. Write the content following best practices
4. Ensure the content meets the specified style and audience

You can write articles, blog posts, marketing copy, technical documentation, and other types of content.
Always ask clarifying questions if the task is ambiguous."""
    
    async def write_article(
        self,
        topic: str,
        outline: Optional[str] = None,
        word_count: Optional[int] = None,
    ) -> str:
        """Write an article on the given topic."""
        task = {
            "type": "write_article",
            "topic": topic,
            "outline": outline,
            "word_count": word_count,
            "description": f"Write an article about {topic}",
        }
        
        response = await self.perform_task(task)
        if response.success and response.data:
            # LLMAgent returns "response" key
            return response.data.get("response", "")
        else:
            raise Exception(f"Failed to write article: {response.error}")
    
    async def edit_content(self, content: str, feedback: str) -> str:
        """Edit content based on feedback."""
        task = {
            "type": "edit_content",
            "content": content,
            "feedback": feedback,
            "description": "Edit content based on feedback",
        }
        
        response = await self.perform_task(task)
        if response.success and response.data:
            # LLMAgent returns "response" key
            return response.data.get("response", "")
        else:
            raise Exception(f"Failed to edit content: {response.error}")
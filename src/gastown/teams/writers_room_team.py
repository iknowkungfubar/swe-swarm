"""
Writers Room Team for Gastown Swarm.

Specialized team for collaborative content creation with multiple roles:
- Lead Writer: Oversees writing process, creates main content
- Researcher: Gathers information and facts
- Editor: Reviews and improves content
"""

from typing import Any, Dict, List, Optional

from loguru import logger

from ..agents import ContentWriterAgent
from ..llm import LLMProvider, LLMRouter
from .base_team import BaseTeam


class WritersRoomTeam(BaseTeam):
    """Team for collaborative writing projects."""
    
    def __init__(
        self,
        name: str = "writers_room",
        description: str = "Collaborative writing team",
        llm_router: Optional[LLMRouter] = None,
        llm_provider: Optional[LLMProvider] = None,
        writing_style: str = "professional",
        target_audience: str = "general",
    ):
        super().__init__(name=name, description=description)
        
        self.llm_router = llm_router
        self.llm_provider = llm_provider
        self.writing_style = writing_style
        self.target_audience = target_audience
        
        # Create specialized agents
        self.lead_writer = self._create_lead_writer()
        self.researcher = self._create_researcher()
        self.editor = self._create_editor()
        
        # Add agents to team
        self.add_member(self.lead_writer)
        self.add_member(self.researcher)
        self.add_member(self.editor)
        
        logger.info(f"WritersRoomTeam initialized with {len(self.members)} specialized agents")
    
    def _create_lead_writer(self) -> ContentWriterAgent:
        """Create the lead writer agent."""
        return ContentWriterAgent(
            name="lead_writer",
            role="lead_writer",
            system_prompt=self._get_lead_writer_prompt(),
            llm_router=self.llm_router,
            llm_provider=self.llm_provider,
            task_type="writing",
            writing_style=self.writing_style,
            target_audience=self.target_audience,
        )
    
    def _create_researcher(self) -> ContentWriterAgent:
        """Create the researcher agent."""
        return ContentWriterAgent(
            name="researcher",
            role="researcher",
            system_prompt=self._get_researcher_prompt(),
            llm_router=self.llm_router,
            llm_provider=self.llm_provider,
            task_type="research",
            writing_style=self.writing_style,
            target_audience=self.target_audience,
        )
    
    def _create_editor(self) -> ContentWriterAgent:
        """Create the editor agent."""
        return ContentWriterAgent(
            name="editor",
            role="editor",
            system_prompt=self._get_editor_prompt(),
            llm_router=self.llm_router,
            llm_provider=self.llm_provider,
            task_type="editing",
            writing_style=self.writing_style,
            target_audience=self.target_audience,
        )
    
    def _get_lead_writer_prompt(self) -> str:
        """Get system prompt for lead writer."""
        return f"""You are the Lead Writer in a Writers Room team.
Your role is to:
1. Oversee the writing process from concept to final draft
2. Create the main content based on research and outlines
3. Ensure consistency in tone, style, and messaging
4. Coordinate with the Researcher and Editor
5. Make final decisions on content structure and flow

You have a {self.writing_style} writing style and your target audience is {self.target_audience}.
You work collaboratively with other team members to produce high-quality content."""
    
    def _get_researcher_prompt(self) -> str:
        """Get system prompt for researcher."""
        return f"""You are a Researcher in a Writers Room team.
Your role is to:
1. Gather factual information, statistics, and examples
2. Verify claims and ensure accuracy
3. Provide supporting evidence for arguments
4. Identify credible sources
5. Create research summaries for the Lead Writer

You work with a {self.writing_style} writing style and your target audience is {self.target_audience}.
You ensure all content is well-researched and factually accurate."""
    
    def _get_editor_prompt(self) -> str:
        """Get system prompt for editor."""
        return f"""You are an Editor in a Writers Room team.
Your role is to:
1. Review content for grammar, spelling, and punctuation
2. Improve clarity, conciseness, and flow
3. Ensure consistency in style and tone
4. Check for logical structure and organization
5. Provide constructive feedback for improvement

You work with a {self.writing_style} writing style and your target audience is {self.target_audience}.
You ensure all content meets high editorial standards."""
    
    async def write_article_collaboratively(
        self,
        topic: str,
        outline: Optional[str] = None,
        word_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Collaboratively write an article using all team members.
        
        Returns a dictionary with:
        - research: Research findings
        - draft: Initial draft by lead writer
        - edited: Final edited version
        - metadata: Team performance metrics
        """
        if not self.is_active:
            raise ValueError("Team must be active to write collaboratively")
        
        logger.info(f"Starting collaborative writing for topic: {topic}")
        
        # Step 1: Research
        research_task = {
            "type": "research",
            "topic": topic,
            "description": f"Research topic: {topic}",
        }
        research_response = await self.researcher.perform_task(research_task)
        
        if not research_response.success:
            raise Exception(f"Research failed: {research_response.error}")
        
        # Extract research text
        research_text = research_response.data.get("response", "") if research_response.data else ""
        
        # Step 2: Write draft
        draft_task = {
            "type": "write_article",
            "topic": topic,
            "outline": outline,
            "word_count": word_count,
            "research": research_text,
            "description": f"Write article about {topic}",
        }
        draft_response = await self.lead_writer.perform_task(draft_task)
        
        if not draft_response.success:
            raise Exception(f"Draft writing failed: {draft_response.error}")
        
        # Extract draft text
        draft_text = draft_response.data.get("response", "") if draft_response.data else ""
        
        # Step 3: Edit
        edit_task = {
            "type": "edit_content",
            "content": draft_text,
            "description": "Edit article for quality",
        }
        edit_response = await self.editor.perform_task(edit_task)
        
        if not edit_response.success:
            raise Exception(f"Editing failed: {edit_response.error}")
        
        # Extract edited text
        edited_text = edit_response.data.get("response", "") if edit_response.data else ""
        
        return {
            "research": research_text,
            "draft": draft_text,
            "edited": edited_text,
            "metadata": {
                "topic": topic,
                "word_count": word_count,
                "style": self.writing_style,
                "audience": self.target_audience,
            },
        }
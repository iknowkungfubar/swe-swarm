"""
YouTube Team for Gastown Swarm.

Specialized team for YouTube content creation with roles:
- Content Strategist: Plans video topics and channel strategy
- Script Writer: Creates engaging video scripts
- Video Editor: Handles post-production and editing
- SEO Optimizer: Optimizes videos for YouTube search
"""

from typing import Any, Dict, Optional

from loguru import logger

from ..agents import ContentWriterAgent
from ..llm import LLMProvider, LLMRouter
from .base_team import BaseTeam


class YouTubeTeam(BaseTeam):
    """Team for YouTube content creation."""
    
    def __init__(
        self,
        name: str = "youtube_team",
        description: str = "YouTube content creation team",
        llm_router: Optional[LLMRouter] = None,
        llm_provider: Optional[LLMProvider] = None,
    ):
        super().__init__(name=name, description=description)
        
        self.llm_router = llm_router
        self.llm_provider = llm_provider
        
        # Create specialized agents
        self.content_strategist = self._create_content_strategist()
        self.script_writer = self._create_script_writer()
        self.video_editor = self._create_video_editor()
        self.seo_optimizer = self._create_seo_optimizer()
        
        # Add agents to team
        self.add_member(self.content_strategist)
        self.add_member(self.script_writer)
        self.add_member(self.video_editor)
        self.add_member(self.seo_optimizer)
        
        logger.info(f"YouTubeTeam initialized with {len(self.members)} specialized agents")
    
    def _create_content_strategist(self) -> ContentWriterAgent:
        """Create the content strategist agent."""
        return ContentWriterAgent(
            name="content_strategist",
            role="content_strategist",
            system_prompt=self._get_content_strategy_prompt(),
            llm_router=self.llm_router,
            llm_provider=self.llm_provider,
            task_type="content_strategy",
            writing_style="strategic",
            target_audience="youtube_viewers",
        )
    
    def _create_script_writer(self) -> ContentWriterAgent:
        """Create the script writer agent."""
        return ContentWriterAgent(
            name="script_writer",
            role="script_writer",
            system_prompt=self._get_script_writer_prompt(),
            llm_router=self.llm_router,
            llm_provider=self.llm_provider,
            task_type="script_writing",
            writing_style="conversational",
            target_audience="youtube_audience",
        )
    
    def _create_video_editor(self) -> ContentWriterAgent:
        """Create the video editor agent."""
        return ContentWriterAgent(
            name="video_editor",
            role="video_editor",
            system_prompt=self._get_video_editor_prompt(),
            llm_router=self.llm_router,
            llm_provider=self.llm_provider,
            task_type="video_editing",
            writing_style="technical",
            target_audience="production_team",
        )
    
    def _create_seo_optimizer(self) -> ContentWriterAgent:
        """Create the SEO optimizer agent."""
        return ContentWriterAgent(
            name="seo_optimizer",
            role="seo_optimizer",
            system_prompt=self._get_seo_optimizer_prompt(),
            llm_router=self.llm_router,
            llm_provider=self.llm_provider,
            task_type="seo_optimization",
            writing_style="keyword_focused",
            target_audience="youtube_algorithm",
        )
    
    def _get_content_strategy_prompt(self) -> str:
        """Get system prompt for content strategist."""
        return """You are a Content Strategist in a YouTube team.
Your role is to:
1. Research trending topics and content gaps
2. Plan video series and content calendar
3. Analyze channel analytics and audience insights
4. Define target audience and content pillars
5. Collaborate with script writers on video concepts

You create strategic plans that grow channels and engage audiences."""
    
    def _get_script_writer_prompt(self) -> str:
        """Get system prompt for script writer."""
        return """You are a Script Writer in a YouTube team.
Your role is to:
1. Write engaging video scripts with hooks and calls-to-action
2. Create storyboards and visual cues
3. Develop conversational tone for on-camera delivery
4. Include timestamps and chapter markers
5. Optimize script length for target video duration

You write scripts that keep viewers engaged and drive watch time."""
    
    def _get_video_editor_prompt(self) -> str:
        """Get system prompt for video editor."""
        return """You are a Video Editor in a YouTube team.
Your role is to:
1. Create editing plans with cuts, transitions, and effects
2. Suggest B-roll, graphics, and overlay placements
3. Plan sound design, music, and audio mixing
4. Define color grading and visual style
5. Optimize export settings for YouTube upload

You create polished videos that look professional and engaging."""
    
    def _get_seo_optimizer_prompt(self) -> str:
        """Get system prompt for SEO optimizer."""
        return """You are an SEO Optimizer in a YouTube team.
Your role is to:
1. Research keywords and tags for video discovery
2. Write SEO-friendly titles, descriptions, and chapters
3. Create thumbnail concepts and A/B testing strategies
4. Analyze YouTube algorithm trends
5. Optimize playlists and channel structure

You ensure videos are discoverable and rank well in YouTube search."""
    
    async def create_video_plan(
        self,
        channel_theme: str,
        video_topic: str,
        target_length_minutes: int = 10,
    ) -> Dict[str, Any]:
        """
        Create a comprehensive video plan.
        
        Returns a dictionary with:
        - content_strategy: Content plan and topic analysis
        - script: Video script outline
        - editing_plan: Editing and production plan
        - seo_optimization: SEO keywords and metadata
        - metadata: Video plan details
        """
        if not self.is_active:
            raise ValueError("Team must be active to create video plan")
        
        logger.info(f"Creating video plan for topic: {video_topic}")
        
        # Step 1: Content Strategy
        strategy_task = {
            "type": "content_strategy",
            "channel_theme": channel_theme,
            "video_topic": video_topic,
            "description": f"Create content strategy for video about {video_topic}",
        }
        strategy_response = await self.content_strategist.perform_task(strategy_task)
        
        if not strategy_response.success:
            raise Exception(f"Content strategy failed: {strategy_response.error}")
        
        # Step 2: Script Writing
        script_task = {
            "type": "script_writing",
            "video_topic": video_topic,
            "target_length_minutes": target_length_minutes,
            "content_strategy": strategy_response.data.get("response", "") if strategy_response.data else "",
            "description": f"Write script for video about {video_topic}",
        }
        script_response = await self.script_writer.perform_task(script_task)
        
        if not script_response.success:
            raise Exception(f"Script writing failed: {script_response.error}")
        
        # Step 3: Video Editing Plan
        editing_task = {
            "type": "video_editing",
            "video_topic": video_topic,
            "target_length_minutes": target_length_minutes,
            "script": script_response.data.get("response", "") if script_response.data else "",
            "description": f"Create editing plan for video about {video_topic}",
        }
        editing_response = await self.video_editor.perform_task(editing_task)
        
        if not editing_response.success:
            raise Exception(f"Video editing plan failed: {editing_response.error}")
        
        # Step 4: SEO Optimization
        seo_task = {
            "type": "seo_optimization",
            "video_topic": video_topic,
            "channel_theme": channel_theme,
            "description": f"Optimize SEO for video about {video_topic}",
        }
        seo_response = await self.seo_optimizer.perform_task(seo_task)
        
        if not seo_response.success:
            raise Exception(f"SEO optimization failed: {seo_response.error}")
        
        # Extract responses
        strategy_text = strategy_response.data.get("response", "") if strategy_response.data else ""
        script_text = script_response.data.get("response", "") if script_response.data else ""
        editing_text = editing_response.data.get("response", "") if editing_response.data else ""
        seo_text = seo_response.data.get("response", "") if seo_response.data else ""
        
        return {
            "content_strategy": strategy_text,
            "script": script_text,
            "editing_plan": editing_text,
            "seo_optimization": seo_text,
            "metadata": {
                "channel_theme": channel_theme,
                "video_topic": video_topic,
                "target_length_minutes": target_length_minutes,
            },
        }
"""
Marketing Team for Gastown Swarm.

Specialized team for marketing tasks with roles:
- Social Media Manager: Creates and manages social media content
- Content Strategist: Plans content calendar and strategy
- SEO Specialist: Optimizes content for search engines
"""

from typing import Any, Dict, Optional

from loguru import logger

from ..agents import ContentWriterAgent
from ..llm import LLMProvider, LLMRouter
from .base_team import BaseTeam


class MarketingTeam(BaseTeam):
    """Team for marketing campaigns."""
    
    def __init__(
        self,
        name: str = "marketing_team",
        description: str = "Marketing team for campaigns",
        llm_router: Optional[LLMRouter] = None,
        llm_provider: Optional[LLMProvider] = None,
    ):
        super().__init__(name=name, description=description)
        
        self.llm_router = llm_router
        self.llm_provider = llm_provider
        
        # Create specialized agents
        self.social_media_manager = self._create_social_media_manager()
        self.content_strategist = self._create_content_strategist()
        self.seo_specialist = self._create_seo_specialist()
        
        # Add agents to team
        self.add_member(self.social_media_manager)
        self.add_member(self.content_strategist)
        self.add_member(self.seo_specialist)
        
        logger.info(f"MarketingTeam initialized with {len(self.members)} specialized agents")
    
    def _create_social_media_manager(self) -> ContentWriterAgent:
        """Create the social media manager agent."""
        return ContentWriterAgent(
            name="social_media_manager",
            role="social_media_manager",
            system_prompt=self._get_social_media_prompt(),
            llm_router=self.llm_router,
            llm_provider=self.llm_provider,
            task_type="social_media",
            writing_style="engaging",
            target_audience="social_media_users",
        )
    
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
            target_audience="marketing",
        )
    
    def _create_seo_specialist(self) -> ContentWriterAgent:
        """Create the SEO specialist agent."""
        return ContentWriterAgent(
            name="seo_specialist",
            role="seo_specialist",
            system_prompt=self._get_seo_prompt(),
            llm_router=self.llm_router,
            llm_provider=self.llm_provider,
            task_type="seo",
            writing_style="technical",
            target_audience="search_engines",
        )
    
    def _get_social_media_prompt(self) -> str:
        """Get system prompt for social media manager."""
        return """You are a Social Media Manager in a marketing team.
Your role is to:
1. Create engaging social media posts for various platforms (Twitter, LinkedIn, Instagram, Facebook)
2. Develop social media content calendars
3. Monitor engagement and suggest improvements
4. Create hashtags and trending content strategies
5. Collaborate with the content strategist for consistent messaging

You create content that is shareable, engaging, and drives audience interaction."""
    
    def _get_content_strategy_prompt(self) -> str:
        """Get system prompt for content strategist."""
        return """You are a Content Strategist in a marketing team.
Your role is to:
1. Develop content strategies aligned with business goals
2. Plan content calendars and publishing schedules
3. Analyze target audiences and create buyer personas
4. Research content gaps and opportunities
5. Ensure content consistency across all channels

You create strategic plans that support marketing objectives and brand messaging."""
    
    def _get_seo_prompt(self) -> str:
        """Get system prompt for SEO specialist."""
        return """You are an SEO Specialist in a marketing team.
Your role is to:
1. Conduct keyword research and analysis
2. Optimize content for search engines (on-page SEO)
3. Create meta descriptions, title tags, and alt texts
4. Analyze competitor SEO strategies
5. Provide recommendations for improving search rankings

You ensure all content is discoverable and ranks well in search results."""
    
    async def create_campaign(
        self,
        product: str,
        target_audience: str,
        budget: float,
        duration_days: int = 30,
    ) -> Dict[str, Any]:
        """
        Create a comprehensive marketing campaign.
        
        Returns a dictionary with:
        - social_media: Social media strategy and posts
        - content_strategy: Content calendar and plan
        - seo_optimization: SEO keywords and recommendations
        - metadata: Campaign details
        """
        if not self.is_active:
            raise ValueError("Team must be active to create campaign")
        
        logger.info(f"Creating marketing campaign for product: {product}")
        
        # Step 1: Social Media Strategy
        social_task = {
            "type": "social_media_strategy",
            "product": product,
            "target_audience": target_audience,
            "budget": budget,
            "description": f"Create social media strategy for {product}",
        }
        social_response = await self.social_media_manager.perform_task(social_task)
        
        if not social_response.success:
            raise Exception(f"Social media strategy failed: {social_response.error}")
        
        # Step 2: Content Strategy
        content_task = {
            "type": "content_strategy",
            "product": product,
            "target_audience": target_audience,
            "duration_days": duration_days,
            "description": f"Create content strategy for {product}",
        }
        content_response = await self.content_strategist.perform_task(content_task)
        
        if not content_response.success:
            raise Exception(f"Content strategy failed: {content_response.error}")
        
        # Step 3: SEO Optimization
        seo_task = {
            "type": "seo_optimization",
            "product": product,
            "target_audience": target_audience,
            "description": f"Create SEO optimization for {product}",
        }
        seo_response = await self.seo_specialist.perform_task(seo_task)
        
        if not seo_response.success:
            raise Exception(f"SEO optimization failed: {seo_response.error}")
        
        # Extract responses
        social_text = social_response.data.get("response", "") if social_response.data else ""
        content_text = content_response.data.get("response", "") if content_response.data else ""
        seo_text = seo_response.data.get("response", "") if seo_response.data else ""
        
        return {
            "social_media": social_text,
            "content_strategy": content_text,
            "seo_optimization": seo_text,
            "metadata": {
                "product": product,
                "target_audience": target_audience,
                "budget": budget,
                "duration_days": duration_days,
            },
        }
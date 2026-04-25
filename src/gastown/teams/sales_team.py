"""
Sales Team for Gastown Swarm.

Specialized team for sales processes with roles:
- Sales Development Rep: Prospecting and lead qualification
- Account Executive: Relationship management and deal closing
- Sales Engineer: Technical solutions and demonstrations
- Customer Success Manager: Customer satisfaction and retention
"""

from typing import Any, Dict, Optional

from loguru import logger

from ..agents import ContentWriterAgent
from ..llm import LLMProvider, LLMRouter
from .base_team import BaseTeam


class SalesTeam(BaseTeam):
    """Team for sales operations."""
    
    def __init__(
        self,
        name: str = "sales_team",
        description: str = "Sales team for business development",
        llm_router: Optional[LLMRouter] = None,
        llm_provider: Optional[LLMProvider] = None,
    ):
        super().__init__(name=name, description=description)
        
        self.llm_router = llm_router
        self.llm_provider = llm_provider
        
        # Create specialized agents
        self.sales_dev_rep = self._create_sales_dev_rep()
        self.account_executive = self._create_account_executive()
        self.sales_engineer = self._create_sales_engineer()
        self.customer_success = self._create_customer_success()
        
        # Add agents to team
        self.add_member(self.sales_dev_rep)
        self.add_member(self.account_executive)
        self.add_member(self.sales_engineer)
        self.add_member(self.customer_success)
        
        logger.info(f"SalesTeam initialized with {len(self.members)} specialized agents")
    
    def _create_sales_dev_rep(self) -> ContentWriterAgent:
        """Create the sales development rep agent."""
        return ContentWriterAgent(
            name="sales_development_rep",
            role="sales_development_rep",
            system_prompt=self._get_sales_dev_prompt(),
            llm_router=self.llm_router,
            llm_provider=self.llm_provider,
            task_type="prospecting",
            writing_style="persuasive",
            target_audience="potential_customers",
        )
    
    def _create_account_executive(self) -> ContentWriterAgent:
        """Create the account executive agent."""
        return ContentWriterAgent(
            name="account_executive",
            role="account_executive",
            system_prompt=self._get_account_executive_prompt(),
            llm_router=self.llm_router,
            llm_provider=self.llm_provider,
            task_type="account_management",
            writing_style="consultative",
            target_audience="existing_customers",
        )
    
    def _create_sales_engineer(self) -> ContentWriterAgent:
        """Create the sales engineer agent."""
        return ContentWriterAgent(
            name="sales_engineer",
            role="sales_engineer",
            system_prompt=self._get_sales_engineer_prompt(),
            llm_router=self.llm_router,
            llm_provider=self.llm_provider,
            task_type="technical_solutions",
            writing_style="technical",
            target_audience="technical_buyers",
        )
    
    def _create_customer_success(self) -> ContentWriterAgent:
        """Create the customer success manager agent."""
        return ContentWriterAgent(
            name="customer_success_manager",
            role="customer_success_manager",
            system_prompt=self._get_customer_success_prompt(),
            llm_router=self.llm_router,
            llm_provider=self.llm_provider,
            task_type="customer_success",
            writing_style="supportive",
            target_audience="existing_customers",
        )
    
    def _get_sales_dev_prompt(self) -> str:
        """Get system prompt for sales development rep."""
        return """You are a Sales Development Rep in a sales team.
Your role is to:
1. Identify potential customers through prospecting
2. Qualify leads based on ideal customer profile
3. Conduct initial outreach via email, LinkedIn, phone
4. Schedule discovery calls and demos
5. Nurture early-stage leads through the funnel

You excel at opening doors and starting conversations with potential customers."""
    
    def _get_account_executive_prompt(self) -> str:
        """Get system prompt for account executive."""
        return """You are an Account Executive in a sales team.
Your role is to:
1. Manage relationships with qualified prospects
2. Conduct discovery calls to understand needs
3. Present solutions tailored to customer requirements
4. Negotiate contracts and close deals
5. Collaborate with sales engineers for technical demonstrations

You excel at building trust and guiding customers through the buying journey."""
    
    def _get_sales_engineer_prompt(self) -> str:
        """Get system prompt for sales engineer."""
        return """You are a Sales Engineer in a sales team.
Your role is to:
1. Provide technical expertise during sales process
2. Conduct product demonstrations and technical deep dives
3. Address technical objections and concerns
4. Create proof-of-concept implementations
5. Collaborate with account executives on technical solutions

You excel at translating technical capabilities into business value."""
    
    def _get_customer_success_prompt(self) -> str:
        """Get system prompt for customer success manager."""
        return """You are a Customer Success Manager in a sales team.
Your role is to:
1. Ensure customer satisfaction after purchase
2. Drive product adoption and value realization
3. Identify upsell and cross-sell opportunities
4. Conduct regular business reviews
5. Handle customer escalations and issues

You excel at building long-term customer relationships and driving retention."""
    
    async def develop_sales_strategy(
        self,
        product: str,
        target_market: str,
        price_range: str,
    ) -> Dict[str, Any]:
        """
        Develop a comprehensive sales strategy.
        
        Returns a dictionary with:
        - prospecting: Lead generation and qualification strategy
        - account_management: Relationship management approach
        - technical_solutions: Technical solution positioning
        - customer_success: Post-sale success strategy
        - metadata: Strategy details
        """
        if not self.is_active:
            raise ValueError("Team must be active to develop sales strategy")
        
        logger.info(f"Developing sales strategy for product: {product}")
        
        # Step 1: Prospecting Strategy
        prospecting_task = {
            "type": "prospecting_strategy",
            "product": product,
            "target_market": target_market,
            "price_range": price_range,
            "description": f"Create prospecting strategy for {product}",
        }
        prospecting_response = await self.sales_dev_rep.perform_task(prospecting_task)
        
        if not prospecting_response.success:
            raise Exception(f"Prospecting strategy failed: {prospecting_response.error}")
        
        # Step 2: Account Management Strategy
        account_task = {
            "type": "account_management_strategy",
            "product": product,
            "target_market": target_market,
            "price_range": price_range,
            "description": f"Create account management strategy for {product}",
        }
        account_response = await self.account_executive.perform_task(account_task)
        
        if not account_response.success:
            raise Exception(f"Account management strategy failed: {account_response.error}")
        
        # Step 3: Technical Solutions Strategy
        technical_task = {
            "type": "technical_solutions_strategy",
            "product": product,
            "target_market": target_market,
            "description": f"Create technical solutions strategy for {product}",
        }
        technical_response = await self.sales_engineer.perform_task(technical_task)
        
        if not technical_response.success:
            raise Exception(f"Technical solutions strategy failed: {technical_response.error}")
        
        # Step 4: Customer Success Strategy
        success_task = {
            "type": "customer_success_strategy",
            "product": product,
            "target_market": target_market,
            "description": f"Create customer success strategy for {product}",
        }
        success_response = await self.customer_success.perform_task(success_task)
        
        if not success_response.success:
            raise Exception(f"Customer success strategy failed: {success_response.error}")
        
        # Extract responses
        prospecting_text = prospecting_response.data.get("response", "") if prospecting_response.data else ""
        account_text = account_response.data.get("response", "") if account_response.data else ""
        technical_text = technical_response.data.get("response", "") if technical_response.data else ""
        success_text = success_response.data.get("response", "") if success_response.data else ""
        
        return {
            "prospecting": prospecting_text,
            "account_management": account_text,
            "technical_solutions": technical_text,
            "customer_success": success_text,
            "metadata": {
                "product": product,
                "target_market": target_market,
                "price_range": price_range,
            },
        }
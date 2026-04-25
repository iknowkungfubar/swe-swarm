"""
Agent registry for managing agent instances.
"""

from loguru import logger

from ..agents.base_agent import BaseAgent


class AgentRegistry:
    """Registry for agent instances."""

    def __init__(self):
        self.agents: dict[str, BaseAgent] = {}
        self.agents_by_role: dict[str, list[BaseAgent]] = {}

    def register(self, agent: BaseAgent):
        """Register an agent."""
        self.agents[agent.name] = agent

        # Add to role mapping
        if agent.role not in self.agents_by_role:
            self.agents_by_role[agent.role] = []
        self.agents_by_role[agent.role].append(agent)

        logger.info(f"Registered agent: {agent.name} ({agent.role})")

    def unregister(self, agent_name: str):
        """Unregister an agent by name."""
        if agent_name in self.agents:
            agent = self.agents[agent_name]
            # Remove from role mapping
            if agent.role in self.agents_by_role:
                self.agents_by_role[agent.role] = [
                    a for a in self.agents_by_role[agent.role] if a.name != agent_name
                ]
            del self.agents[agent_name]
            logger.info(f"Unregistered agent: {agent_name}")

    def get_agent(self, name: str) -> BaseAgent | None:
        """Get an agent by name."""
        return self.agents.get(name)

    def get_agents_by_role(self, role: str) -> list[BaseAgent]:
        """Get all agents with a specific role."""
        return self.agents_by_role.get(role, [])

    def list_agents(self) -> list[dict[str, any]]:
        """List all registered agents."""
        return [agent.get_status() for agent in self.agents.values()]

    def get_active_agents(self) -> list[BaseAgent]:
        """Get all active agents."""
        return [agent for agent in self.agents.values() if agent.is_active]

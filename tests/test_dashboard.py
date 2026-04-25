"""
Tests for dashboard API.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient

from gastown.dashboard.app import create_app
from gastown.runtime.agent_registry import AgentRegistry
from gastown.agents.base_agent import BaseAgent, AgentMessage, AgentResponse


class MockAgent(BaseAgent):
    """Mock agent for testing."""
    
    def __init__(self, name="mock_agent", role="mock"):
        super().__init__(name=name, role=role, system_prompt="Mock agent")
    
    async def process_message(self, message: AgentMessage) -> AgentResponse:
        return AgentResponse(success=True, data={"processed": True})
    
    async def perform_task(self, task):
        return AgentResponse(success=True, data={"result": "mock"})


class TestDashboard:
    """Test dashboard API."""
    
    @pytest.fixture
    def mock_registry(self):
        """Create a mock agent registry."""
        registry = AgentRegistry()
        # Add a mock agent
        agent = MockAgent(name="test_agent", role="tester")
        registry.register(agent)
        return registry
    
    @pytest.fixture
    def mock_router(self):
        """Create a mock task router."""
        router = MagicMock()
        router.get_all_tasks = MagicMock(return_value=[])
        return router
    
    @pytest.fixture
    def client(self, mock_registry, mock_router):
        """Create test client."""
        app = create_app(agent_registry=mock_registry, task_router=mock_router)
        return TestClient(app)
    
    def test_health_check(self, client):
        """Test health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "gastown-dashboard"
    
    def test_list_agents(self, client):
        """Test list agents endpoint."""
        response = client.get("/api/agents")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
        assert data["agents"][0]["name"] == "test_agent"
        assert data["agents"][0]["role"] == "tester"
    
    def test_list_tasks(self, client):
        """Test list tasks endpoint."""
        response = client.get("/api/tasks")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["tasks"] == []
    
    def test_activate_agent(self, client):
        """Test activate agent endpoint."""
        response = client.post("/api/agents/test_agent/activate")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["agent"] == "test_agent"
        assert data["active"] == True
    
    def test_activate_agent_not_found(self, client):
        """Test activate non-existent agent."""
        response = client.post("/api/agents/nonexistent/activate")
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
    
    def test_deactivate_agent(self, client):
        """Test deactivate agent endpoint."""
        # First activate
        client.post("/api/agents/test_agent/activate")
        # Then deactivate
        response = client.post("/api/agents/test_agent/deactivate")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["agent"] == "test_agent"
        assert data["active"] == False
    
    def test_websocket(self, client):
        """Test WebSocket connection."""
        with client.websocket_connect("/ws") as websocket:
            websocket.send_text("Hello")
            data = websocket.receive_text()
            assert data == "Message received: Hello"
"""
FastAPI application for Gastown Swarm dashboard.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any, Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from loguru import logger

from ..runtime.agent_registry import AgentRegistry
from ..orchestrator.task_router import TaskRouter


class ConnectionManager:
    """WebSocket connection manager."""
    
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        for connection in self.active_connections:
            await connection.send_json(message)


# Global connection manager
manager = ConnectionManager()


def create_app(
    agent_registry: AgentRegistry | None = None,
    task_router: TaskRouter | None = None,
) -> FastAPI:
    """
    Create FastAPI application for dashboard.
    
    Args:
        agent_registry: Optional agent registry instance
        task_router: Optional task router instance
    """
    
    app = FastAPI(
        title="Gastown Swarm Dashboard",
        description="Web interface for monitoring and controlling Gastown Swarm agents",
        version="0.1.0",
    )
    
    # Set state immediately
    app.state.agent_registry = agent_registry or AgentRegistry()
    app.state.task_router = task_router or TaskRouter()
    
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        # Startup
        logger.info("Dashboard starting up")
        yield
        # Shutdown
        logger.info("Dashboard shutting down")
    
    app.router.lifespan_context = lifespan
    
    @app.get("/health")
    async def health_check() -> Dict[str, str]:
        """Health check endpoint."""
        return {"status": "healthy", "service": "gastown-dashboard"}
    
    @app.get("/api/agents")
    async def list_agents() -> Dict[str, Any]:
        """List all registered agents."""
        registry: AgentRegistry = app.state.agent_registry
        agents = registry.list_agents()
        return {
            "count": len(agents),
            "agents": agents,
        }
    
    @app.get("/api/tasks")
    async def list_tasks() -> Dict[str, Any]:
        """List all tasks."""
        router: TaskRouter = app.state.task_router
        tasks = router.get_all_tasks()
        return {
            "count": len(tasks),
            "tasks": [
                {
                    "id": task.id,
                    "description": task.description,
                    "status": task.status,
                    "assigned_to": task.assigned_to,
                }
                for task in tasks
            ],
        }
    
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """WebSocket endpoint for real-time updates."""
        await manager.connect(websocket)
        try:
            while True:
                # Keep connection alive, receive messages (optional)
                data = await websocket.receive_text()
                # Echo for now
                await websocket.send_text(f"Message received: {data}")
        except WebSocketDisconnect:
            manager.disconnect(websocket)
    
    @app.post("/api/agents/{agent_name}/activate")
    async def activate_agent(agent_name: str) -> Dict[str, Any]:
        """Activate an agent."""
        registry: AgentRegistry = app.state.agent_registry
        agent = registry.get_agent(agent_name)
        if not agent:
            return JSONResponse(
                status_code=404,
                content={"error": f"Agent '{agent_name}' not found"},
            )
        agent.activate()
        return {"success": True, "agent": agent_name, "active": True}
    
    @app.post("/api/agents/{agent_name}/deactivate")
    async def deactivate_agent(agent_name: str) -> Dict[str, Any]:
        """Deactivate an agent."""
        registry: AgentRegistry = app.state.agent_registry
        agent = registry.get_agent(agent_name)
        if not agent:
            return JSONResponse(
                status_code=404,
                content={"error": f"Agent '{agent_name}' not found"},
            )
        agent.deactivate()
        return {"success": True, "agent": agent_name, "active": False}
    
    return app
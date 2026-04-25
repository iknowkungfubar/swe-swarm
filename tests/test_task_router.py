"""Unit tests for TaskRouter."""
import pytest
from src.gastown.orchestrator.task_router import TaskRouter, Task, TaskStatus


class TestTaskRouter:
    """Test TaskRouter functionality."""

    def test_initialization(self):
        """Test router initialization."""
        router = TaskRouter()
        assert router.tasks == {}
        assert router.agent_capabilities == {}
        
        router2 = TaskRouter(agent_capabilities={"agent1": ["skill1"]})
        assert router2.agent_capabilities == {"agent1": ["skill1"]}

    def test_decompose_goal_calculator(self):
        """Test decomposing a calculator goal."""
        router = TaskRouter()
        tasks = router.decompose_goal("Build a calculator")
        assert len(tasks) == 3  # plan, implement, test
        
        # Check task dependencies
        plan_task = tasks[0]
        assert "plan" in plan_task.id
        assert plan_task.priority == 10
        assert plan_task.status == TaskStatus.PENDING
        
        impl_task = tasks[1]
        assert "implement" in impl_task.id
        assert plan_task.id in impl_task.dependencies
        assert impl_task.priority == 5
        
        test_task = tasks[2]
        assert "test" in test_task.id or "verify" in test_task.id
        assert impl_task.id in test_task.dependencies

    def test_decompose_goal_generic(self):
        """Test decomposing a generic goal."""
        router = TaskRouter()
        tasks = router.decompose_goal("Create a web app")
        assert len(tasks) == 3  # plan, implement, verify
        
        # Should still have planning task
        plan_task = tasks[0]
        assert plan_task.priority == 10

    def test_assign_task(self):
        """Test assigning a task."""
        router = TaskRouter()
        tasks = router.decompose_goal("Test goal")
        task_id = tasks[0].id
        
        # Assign
        success = router.assign_task(task_id, "agent1")
        assert success is True
        assert router.tasks[task_id].status == TaskStatus.ASSIGNED
        assert router.tasks[task_id].assignee == "agent1"
        
        # Cannot assign again (already assigned)
        success = router.assign_task(task_id, "agent2")
        assert success is False

    def test_start_task(self):
        """Test starting a task."""
        router = TaskRouter()
        tasks = router.decompose_goal("Test goal")
        task_id = tasks[0].id
        
        # Cannot start before assignment
        success = router.start_task(task_id)
        assert success is False
        
        router.assign_task(task_id, "agent1")
        success = router.start_task(task_id)
        assert success is True
        assert router.tasks[task_id].status == TaskStatus.IN_PROGRESS

    def test_complete_task(self):
        """Test completing a task."""
        router = TaskRouter()
        tasks = router.decompose_goal("Test goal")
        task_id = tasks[0].id
        
        router.assign_task(task_id, "agent1")
        router.start_task(task_id)
        
        result = {"output": "done"}
        success = router.complete_task(task_id, result)
        assert success is True
        assert router.tasks[task_id].status == TaskStatus.COMPLETED
        assert router.tasks[task_id].result == result
        
        # Dependent tasks should now be ready (pending)
        # The second task depends on first
        dep_task = tasks[1]
        assert dep_task.status == TaskStatus.PENDING

    def test_fail_task(self):
        """Test failing a task."""
        router = TaskRouter()
        tasks = router.decompose_goal("Test goal")
        task_id = tasks[0].id
        
        success = router.fail_task(task_id, "Something went wrong")
        assert success is True
        assert router.tasks[task_id].status == TaskStatus.FAILED
        assert router.tasks[task_id].result == {"error": "Something went wrong"}

    def test_get_pending_tasks(self):
        """Test retrieving pending tasks."""
        router = TaskRouter()
        tasks = router.decompose_goal("Test goal")
        
        pending = router.get_pending_tasks()
        assert len(pending) == 3
        
        # All should be pending
        for task in pending:
            assert task.status == TaskStatus.PENDING
        
        # Assign one
        router.assign_task(tasks[0].id, "agent1")
        pending = router.get_pending_tasks()
        assert len(pending) == 2  # one assigned

    def test_get_ready_tasks(self):
        """Test retrieving ready tasks (dependencies satisfied)."""
        router = TaskRouter()
        tasks = router.decompose_goal("Test goal")
        
        # Initially, only first task is ready (no dependencies)
        ready = router.get_ready_tasks()
        assert len(ready) == 1
        assert ready[0].id == tasks[0].id
        
        # Complete first task
        router.assign_task(tasks[0].id, "agent1")
        router.start_task(tasks[0].id)
        router.complete_task(tasks[0].id, {})
        
        ready = router.get_ready_tasks()
        assert len(ready) == 1
        assert ready[0].id == tasks[1].id

    def test_update_agent_capabilities(self):
        """Test updating agent capabilities."""
        router = TaskRouter()
        router.update_agent_capabilities("agent1", ["python", "testing"])
        assert router.agent_capabilities["agent1"] == ["python", "testing"]
        
        router.update_agent_capabilities("agent2", ["javascript"])
        assert len(router.agent_capabilities) == 2

    def test_suggest_agent_for_task(self):
        """Test agent suggestion based on task description."""
        router = TaskRouter(agent_capabilities={
            "engineer-0": ["python"],
            "qa-0": ["testing"],
            "pm-0": ["planning"],
        })
        
        # Implementation task
        task = Task(id="1", description="Implement feature")
        agent = router.suggest_agent_for_task(task)
        assert agent == "engineer-0"
        
        # Test task
        task2 = Task(id="2", description="Write tests")
        agent2 = router.suggest_agent_for_task(task2)
        assert agent2 == "qa-0"
        
        # Plan task
        task3 = Task(id="3", description="Plan project")
        agent3 = router.suggest_agent_for_task(task3)
        assert agent3 == "pm-0"
        
        # Unknown task
        task4 = Task(id="4", description="Do something")
        agent4 = router.suggest_agent_for_task(task4)
        assert agent4 == "engineer-0"  # fallback first agent

    def test_get_task_status(self):
        """Test getting task status."""
        router = TaskRouter()
        tasks = router.decompose_goal("Test goal")
        task_id = tasks[0].id
        
        status = router.get_task_status(task_id)
        assert status is not None
        assert status["id"] == task_id
        assert status["status"] == TaskStatus.PENDING
        
        # Non-existent task
        status2 = router.get_task_status("nonexistent")
        assert status2 is None

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        router = TaskRouter()
        tasks = router.decompose_goal("Test goal")
        
        all_tasks = router.get_all_tasks()
        assert len(all_tasks) == 3
        for task_dict in all_tasks:
            assert "id" in task_dict
            assert "status" in task_dict
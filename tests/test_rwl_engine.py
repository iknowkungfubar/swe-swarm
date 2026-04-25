"""Unit tests for RWL Engine."""
import asyncio
import pytest
from src.gastown.orchestrator.rwl_engine import RWLEngine, LoopPhase, LoopState


class TestRWLEngine:
    """Test RWL engine functionality."""

    def test_initial_state(self):
        """Test engine initialization."""
        engine = RWLEngine(goal="Test goal", max_iterations=5)
        assert engine.state.goal == "Test goal"
        assert engine.state.current_phase == LoopPhase.INTERPRET
        assert engine.state.iteration == 0
        assert engine.state.completed is False
        assert engine.max_iterations == 5

    @pytest.mark.asyncio
    async def test_run_simple_goal(self):
        """Test running a simple goal to completion."""
        engine = RWLEngine(goal="Simple goal", max_iterations=10)
        # Mock phase handlers to avoid actual work
        original_handlers = engine.phase_handlers.copy()
        
        async def mock_handler():
            # Return next phase or None for completion
            if engine.state.current_phase == LoopPhase.OBSERVE:
                return None  # completion
            # Move to next phase
            phases = list(LoopPhase)
            idx = phases.index(engine.state.current_phase)
            return phases[(idx + 1) % len(phases)]
        
        for phase in LoopPhase:
            engine.phase_handlers[phase] = mock_handler
        
        success = await engine.run()
        assert success is True
        assert engine.state.completed is True
        # Each phase call increments iteration, so 6 phases = 6 iterations
        assert engine.state.iteration == 6
        
        # Restore original handlers
        engine.phase_handlers = original_handlers

    @pytest.mark.asyncio
    async def test_max_iterations(self):
        """Test that engine stops at max iterations."""
        engine = RWLEngine(goal="Long goal", max_iterations=2)
        
        # Mock handlers that never complete
        async def never_complete():
            return LoopPhase.INTERPRET  # always loop back
        
        for phase in LoopPhase:
            engine.phase_handlers[phase] = never_complete
        
        success = await engine.run()
        assert success is False
        assert engine.state.iteration == 2

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test that engine handles errors and retries."""
        engine = RWLEngine(goal="Goal with errors", max_iterations=20)
        
        call_count = {}
        
        async def flaky_handler():
            phase = engine.state.current_phase
            call_count[phase] = call_count.get(phase, 0) + 1
            # Fail on first attempt per phase, succeed on second
            if call_count[phase] == 1:
                raise ValueError("Simulated error")
            # After second attempt, succeed and move to next phase
            if phase == LoopPhase.OBSERVE:
                return None
            phases = list(LoopPhase)
            idx = phases.index(phase)
            return phases[(idx + 1) % len(phases)]
        
        for phase in LoopPhase:
            engine.phase_handlers[phase] = flaky_handler
        
        success = await engine.run()
        # Should succeed after retries (6 phases * 2 attempts = 12 iterations)
        assert success is True
        assert engine.state.completed is True
        # Error count should be reset after each phase success
        assert engine.state.error_count == 0

    def test_loop_state_model(self):
        """Test LoopState model."""
        state = LoopState(goal="Test", current_phase=LoopPhase.BUILD)
        assert state.goal == "Test"
        assert state.current_phase == LoopPhase.BUILD
        assert state.iteration == 0
        assert state.phase_history == []
        assert state.artifacts == {}
        assert state.error_count == 0
        assert state.max_errors == 3
        assert state.completed is False
        
        # Test serialization
        data = state.model_dump()
        assert data["goal"] == "Test"
        assert data["current_phase"] == "build"
        
        # Test deserialization
        state2 = LoopState(**data)
        assert state2.goal == "Test"
        assert state2.current_phase == LoopPhase.BUILD
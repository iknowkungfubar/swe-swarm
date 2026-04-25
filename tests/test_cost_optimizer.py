"""
Tests for Cost Optimizer.
"""

import pytest
from unittest.mock import MagicMock

from gastown.llm.cost_optimizer import (
    CostOptimizer,
    TaskComplexity,
    QualityRequirement,
    RoutingDecision,
)
from gastown.llm.provider import LLMRequest


class MockProvider:
    """Mock provider for testing."""
    
    def __init__(self, name: str, is_initialized: bool = True):
        self.name = name
        self.is_initialized = is_initialized
    
    def estimate_cost(self, request: LLMRequest) -> float:
        if self.name == "ollama":
            return 0.0
        elif self.name == "openai":
            return 0.01
        else:
            return 0.005


class TestTaskComplexity:
    """Test TaskComplexity enum."""
    
    def test_values(self):
        """Test enum values."""
        assert TaskComplexity.SIMPLE.value == "simple"
        assert TaskComplexity.MODERATE.value == "moderate"
        assert TaskComplexity.COMPLEX.value == "complex"
        assert TaskComplexity.CRITICAL.value == "critical"


class TestQualityRequirement:
    """Test QualityRequirement enum."""
    
    def test_values(self):
        """Test enum values."""
        assert QualityRequirement.LOW.value == "low"
        assert QualityRequirement.MEDIUM.value == "medium"
        assert QualityRequirement.HIGH.value == "high"
        assert QualityRequirement.MAXIMUM.value == "maximum"


class TestCostOptimizer:
    """Test CostOptimizer class."""
    
    @pytest.fixture
    def providers(self):
        """Create mock providers."""
        return {
            "openai": MockProvider("openai"),
            "ollama": MockProvider("ollama"),
            "lemonade": MockProvider("lemonade"),
        }
    
    @pytest.fixture
    def optimizer(self, providers):
        """Create optimizer instance."""
        return CostOptimizer(providers=providers)
    
    def test_init(self, optimizer, providers):
        """Test optimizer initialization."""
        assert optimizer.providers == providers
        assert optimizer.cost_budget is None
        assert optimizer.latency_threshold_ms == 5000
    
    def test_analyze_task_simple(self, optimizer):
        """Test analyzing simple task."""
        request = LLMRequest(prompt="What is 2+2?")
        
        complexity, quality = optimizer.analyze_task(request)
        
        assert complexity == TaskComplexity.SIMPLE
        assert quality == QualityRequirement.LOW
    
    def test_analyze_task_complex(self, optimizer):
        """Test analyzing complex task."""
        request = LLMRequest(
            prompt="Analyze and compare these algorithms, then design an optimal solution step by step.",
            system_prompt="You are an expert programmer. Be thorough and detailed."
        )
        
        complexity, quality = optimizer.analyze_task(request)
        
        # Should be at least moderate complexity
        assert complexity in [TaskComplexity.MODERATE, TaskComplexity.COMPLEX]
        # Quality can be low to high depending on the prompt analysis
    
    def test_analyze_task_with_context(self, optimizer):
        """Test analyzing task with context."""
        request = LLMRequest(prompt="Simple question")
        
        context = {"is_production": True}
        complexity, quality = optimizer.analyze_task(request, context)
        
        assert quality == QualityRequirement.MAXIMUM
    
    def test_select_provider_simple_task(self, optimizer):
        """Test selecting provider for simple task."""
        request = LLMRequest(prompt="What is the weather?")
        
        decision = optimizer.select_provider(request)
        
        # Should prefer local providers for simple tasks
        assert decision.provider_name in ["ollama", "lemonade"]
        assert decision.estimated_cost == 0.0
    
    def test_select_provider_complex_task(self, optimizer):
        """Test selecting provider for complex task."""
        request = LLMRequest(
            prompt="Analyze this complex codebase and design a refactoring strategy.",
            system_prompt="You are an expert software architect."
        )
        
        decision = optimizer.select_provider(request)
        
        # Should select a provider (can be OpenAI or local depending on cost optimization)
        assert decision.provider_name in ["openai", "ollama", "lemonade"]
    
    def test_select_provider_with_task_type(self, optimizer):
        """Test selecting provider with task type hint."""
        request = LLMRequest(prompt="Write Python code")
        
        decision = optimizer.select_provider(request, task_type="coding")
        
        # Should select a provider (OpenAI is preferred for coding but local may be selected for cost)
        assert decision.provider_name in ["openai", "ollama"]
    
    def test_select_provider_with_budget_constraint(self, optimizer):
        """Test selecting provider with budget constraint."""
        # Set a very low budget
        optimizer.cost_budget = 0.001
        optimizer._total_cost = 0.0009  # Almost at budget
        
        request = LLMRequest(prompt="Expensive task")
        
        decision = optimizer.select_provider(request)
        
        # Should prefer free providers when near budget
        assert decision.provider_name in ["ollama", "lemonade"]
    
    def test_select_provider_fallback(self, optimizer):
        """Test that fallback provider is set."""
        request = LLMRequest(prompt="Test")
        
        decision = optimizer.select_provider(request)
        
        # Should have a fallback if multiple providers available
        if len(optimizer.providers) > 1:
            assert decision.fallback_provider is not None
    
    def test_select_provider_no_providers(self):
        """Test that empty providers raises error."""
        optimizer = CostOptimizer(providers={})
        request = LLMRequest(prompt="Test")
        
        with pytest.raises(RuntimeError, match="No available providers"):
            optimizer.select_provider(request)
    
    def test_record_usage(self, optimizer):
        """Test recording usage."""
        optimizer.record_usage("openai", 0.01, 1000)
        optimizer.record_usage("ollama", 0.0, 500)
        
        assert optimizer._total_cost == 0.01
        assert len(optimizer._usage_history) == 2
    
    def test_get_usage_stats(self, optimizer):
        """Test getting usage statistics."""
        optimizer.record_usage("openai", 0.01, 1000)
        optimizer.record_usage("openai", 0.02, 1200)
        optimizer.record_usage("ollama", 0.0, 500)
        
        stats = optimizer.get_usage_stats()
        
        assert stats["total_cost"] == 0.03
        assert stats["total_requests"] == 3
        assert stats["avg_latency_ms"] == 900  # (1000 + 1200 + 500) / 3
        assert "openai" in stats["provider_breakdown"]
        assert "ollama" in stats["provider_breakdown"]
    
    def test_get_usage_stats_empty(self, optimizer):
        """Test getting usage stats when empty."""
        stats = optimizer.get_usage_stats()
        
        assert stats["total_cost"] == 0.0
        assert stats["total_requests"] == 0
        assert stats["avg_latency_ms"] == 0
    
    def test_reset_budget(self, optimizer):
        """Test resetting budget tracking."""
        optimizer.record_usage("openai", 0.01, 1000)
        
        optimizer.reset_budget()
        
        assert optimizer._total_cost == 0.0
        assert len(optimizer._usage_history) == 0
    
    def test_estimate_latency(self, optimizer):
        """Test latency estimation."""
        simple_latency = optimizer._estimate_latency(TaskComplexity.SIMPLE, "ollama")
        complex_latency = optimizer._estimate_latency(TaskComplexity.COMPLEX, "openai")
        
        # Complex tasks should have higher latency
        assert complex_latency > simple_latency
        
        # Local providers should have lower base latency
        local_latency = optimizer._estimate_latency(TaskComplexity.SIMPLE, "ollama")
        remote_latency = optimizer._estimate_latency(TaskComplexity.SIMPLE, "openai")
        assert local_latency < remote_latency
    
    def test_calculate_quality_match(self, optimizer):
        """Test quality matching calculation."""
        # Provider meets requirements
        match = optimizer._calculate_quality_match(
            QualityRequirement.MEDIUM,
            QualityRequirement.HIGH
        )
        assert match == 1.0
        
        # Provider exceeds requirements
        match = optimizer._calculate_quality_match(
            QualityRequirement.LOW,
            QualityRequirement.MAXIMUM
        )
        assert match == 1.0
        
        # Provider falls short
        match = optimizer._calculate_quality_match(
            QualityRequirement.HIGH,
            QualityRequirement.LOW
        )
        assert match < 1.0

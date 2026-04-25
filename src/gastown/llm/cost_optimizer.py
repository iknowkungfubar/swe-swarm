"""
Cost optimizer for intelligent LLM provider routing.

Routes requests to the most cost-effective provider based on:
- Task complexity and quality requirements
- Latency constraints
- Cost budgets
- Provider capabilities and availability
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger

from .provider import LLMProvider, LLMRequest


class TaskComplexity(Enum):
    """Task complexity levels for routing decisions."""
    SIMPLE = "simple"      # Simple queries, translations, basic completions
    MODERATE = "moderate"  # Summarization, code generation, analysis
    COMPLEX = "complex"    # Multi-step reasoning, complex code, research
    CRITICAL = "critical"  # Production code, important decisions, high-stakes


class QualityRequirement(Enum):
    """Quality requirements for task execution."""
    LOW = "low"          # Speed over quality
    MEDIUM = "medium"    # Balanced quality/speed
    HIGH = "high"        # Quality over speed
    MAXIMUM = "maximum"  # Best possible quality


@dataclass
class RoutingDecision:
    """Result of routing decision."""
    provider_name: str
    reason: str
    estimated_cost: float
    estimated_latency_ms: int
    fallback_provider: Optional[str] = None


class CostOptimizer:
    """
    Intelligently routes LLM requests to optimal providers.
    
    Considers:
    1. Task complexity and quality requirements
    2. Provider capabilities and strengths
    3. Cost constraints and budgets
    4. Latency requirements
    5. Provider health and availability
    """
    
    # Provider capabilities mapping
    PROVIDER_CAPABILITIES = {
        "openai": {
            "strengths": ["complex_reasoning", "coding", "analysis", "creativity"],
            "max_quality": QualityRequirement.MAXIMUM,
            "supports_streaming": True,
            "supports_functions": True,
            "reliability": 0.99,
        },
        "ollama": {
            "strengths": ["local_inference", "privacy", "low_latency"],
            "max_quality": QualityRequirement.HIGH,
            "supports_streaming": True,
            "supports_functions": False,
            "reliability": 0.95,
        },
        "lemonade": {
            "strengths": ["amd_optimization", "local_inference", "efficiency"],
            "max_quality": QualityRequirement.HIGH,
            "supports_streaming": True,
            "supports_functions": False,
            "reliability": 0.95,
        },
    }
    
    def __init__(
        self,
        providers: Dict[str, LLMProvider],
        cost_budget: Optional[float] = None,
        latency_threshold_ms: int = 5000,
    ):
        self.providers = providers
        self.cost_budget = cost_budget
        self.latency_threshold_ms = latency_threshold_ms
        self._usage_history: List[Dict[str, Any]] = []
        self._total_cost: float = 0.0
    
    def analyze_task(
        self,
        request: LLMRequest,
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[TaskComplexity, QualityRequirement]:
        """
        Analyze task to determine complexity and quality requirements.
        
        This is a heuristic analysis based on prompt characteristics.
        """
        prompt_length = len(request.prompt)
        system_prompt_length = len(request.system_prompt) if request.system_prompt else 0
        
        # Analyze prompt content for complexity indicators
        complexity_indicators = [
            "analyze", "compare", "evaluate", "design", "architect",
            "implement", "optimize", "debug", "explain", "reason",
            "step by step", "think", "consider", "evaluate", "assess",
        ]
        
        quality_indicators = [
            "important", "critical", "production", "careful", "thorough",
            "detailed", "comprehensive", "accurate", "precise", "exact",
        ]
        
        prompt_lower = request.prompt.lower()
        
        # Count complexity indicators
        complexity_score = sum(1 for indicator in complexity_indicators 
                             if indicator in prompt_lower)
        
        # Count quality indicators
        quality_score = sum(1 for indicator in quality_indicators 
                          if indicator in prompt_lower)
        
        # Determine complexity
        if complexity_score >= 3 or prompt_length > 2000:
            complexity = TaskComplexity.COMPLEX
        elif complexity_score >= 1 or prompt_length > 500:
            complexity = TaskComplexity.MODERATE
        else:
            complexity = TaskComplexity.SIMPLE
        
        # Determine quality requirement
        if quality_score >= 2 or system_prompt_length > 500:
            quality = QualityRequirement.HIGH
        elif quality_score >= 1:
            quality = QualityRequirement.MEDIUM
        else:
            quality = QualityRequirement.LOW
        
        # Adjust based on context
        if context:
            if context.get("is_production"):
                quality = QualityRequirement.MAXIMUM
            if context.get("latency_critical"):
                quality = QualityRequirement.LOW
        
        return complexity, quality
    
    def select_provider(
        self,
        request: LLMRequest,
        task_type: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> RoutingDecision:
        """
        Select the optimal provider for a request.
        
        Args:
            request: The LLM request
            task_type: Optional task type hint
            context: Additional context (production flag, latency requirements, etc.)
            
        Returns:
            RoutingDecision with selected provider and reasoning
        """
        complexity, quality = self.analyze_task(request, context)
        
        # Score each available provider
        provider_scores: Dict[str, float] = {}
        provider_reasons: Dict[str, str] = {}
        
        for name, provider in self.providers.items():
            if not provider.is_initialized:
                continue
            
            score = 0.0
            reasons = []
            
            # Get provider capabilities
            caps = self.PROVIDER_CAPABILITIES.get(name, {})
            
            # Quality matching (40% weight)
            max_quality = caps.get("max_quality", QualityRequirement.MEDIUM)
            quality_score = self._calculate_quality_match(quality, max_quality)
            score += quality_score * 0.4
            
            # Cost efficiency (30% weight)
            estimated_cost = provider.estimate_cost(request)
            if estimated_cost == 0:
                cost_score = 1.0
                reasons.append("local/free")
            else:
                cost_score = max(0, 1 - (estimated_cost / 0.1))  # Normalize
            score += cost_score * 0.3
            
            # Latency suitability (20% weight)
            if complexity in [TaskComplexity.SIMPLE, TaskComplexity.MODERATE]:
                # Prefer local providers for simple tasks
                if name in ["ollama", "lemonade"]:
                    score += 0.2
                    reasons.append("low_latency")
                else:
                    score += 0.1
            else:
                # Prefer frontier models for complex tasks
                if name == "openai":
                    score += 0.2
                    reasons.append("high_capability")
                else:
                    score += 0.1
            
            # Reliability (10% weight)
            reliability = caps.get("reliability", 0.5)
            score += reliability * 0.1
            
            # Task type matching
            if task_type:
                task_mapping = {
                    "coding": ["openai"],
                    "analysis": ["openai"],
                    "creative": ["openai"],
                    "simple_qa": ["ollama", "lemonade"],
                    "translation": ["ollama", "lemonade", "openai"],
                }
                preferred = task_mapping.get(task_type, [])
                if name in preferred:
                    score += 0.1
                    reasons.append(f"task_match:{task_type}")
            
            # Budget constraint
            if self.cost_budget and (self._total_cost + estimated_cost) > self.cost_budget:
                score *= 0.5  # Penalize over-budget providers
                reasons.append("budget_constrained")
            
            provider_scores[name] = score
            provider_reasons[name] = ", ".join(reasons) if reasons else "default"
        
        # Select best provider
        if not provider_scores:
            raise RuntimeError("No available providers")
        
        best_provider = max(provider_scores.items(), key=lambda x: x[1])
        
        # Select fallback (second best)
        fallback = None
        if len(provider_scores) > 1:
            remaining = [(k, v) for k, v in provider_scores.items() if k != best_provider[0]]
            fallback = max(remaining, key=lambda x: x[0])[0]
        
        return RoutingDecision(
            provider_name=best_provider[0],
            reason=provider_reasons[best_provider[0]],
            estimated_cost=self.providers[best_provider[0]].estimate_cost(request),
            estimated_latency_ms=self._estimate_latency(complexity, best_provider[0]),
            fallback_provider=fallback,
        )
    
    def _calculate_quality_match(
        self,
        required: QualityRequirement,
        max_available: QualityRequirement,
    ) -> float:
        """Calculate how well provider quality matches requirements."""
        quality_levels = [
            QualityRequirement.LOW,
            QualityRequirement.MEDIUM,
            QualityRequirement.HIGH,
            QualityRequirement.MAXIMUM,
        ]
        
        req_idx = quality_levels.index(required)
        avail_idx = quality_levels.index(max_available)
        
        if avail_idx >= req_idx:
            return 1.0  # Provider meets or exceeds requirements
        else:
            # Provider falls short
            diff = req_idx - avail_idx
            return max(0.3, 1.0 - (diff * 0.3))
    
    def _estimate_latency(self, complexity: TaskComplexity, provider: str) -> int:
        """Estimate latency based on complexity and provider."""
        base_latencies = {
            "openai": 1000,
            "ollama": 500,
            "lemonade": 400,
        }
        
        complexity_multipliers = {
            TaskComplexity.SIMPLE: 0.5,
            TaskComplexity.MODERATE: 1.0,
            TaskComplexity.COMPLEX: 2.0,
            TaskComplexity.CRITICAL: 3.0,
        }
        
        base = base_latencies.get(provider, 1000)
        multiplier = complexity_multipliers.get(complexity, 1.0)
        
        return int(base * multiplier)
    
    def record_usage(self, provider: str, cost: float, latency_ms: int) -> None:
        """Record usage for budget tracking and optimization."""
        self._usage_history.append({
            "provider": provider,
            "cost": cost,
            "latency_ms": latency_ms,
        })
        self._total_cost += cost
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        if not self._usage_history:
            return {
                "total_cost": 0.0,
                "total_requests": 0,
                "avg_latency_ms": 0,
                "provider_breakdown": {},
            }
        
        provider_costs: Dict[str, float] = {}
        total_latency = 0
        
        for entry in self._usage_history:
            provider = entry["provider"]
            provider_costs[provider] = provider_costs.get(provider, 0) + entry["cost"]
            total_latency += entry["latency_ms"]
        
        return {
            "total_cost": self._total_cost,
            "total_requests": len(self._usage_history),
            "avg_latency_ms": total_latency // len(self._usage_history),
            "provider_breakdown": provider_costs,
            "budget_remaining": (
                self.cost_budget - self._total_cost if self.cost_budget else None
            ),
        }
    
    def reset_budget(self) -> None:
        """Reset budget tracking."""
        self._total_cost = 0.0
        self._usage_history.clear()

"""
Configuration loader for LLM providers.

Loads and validates LLM provider configurations from YAML files.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from loguru import logger

from ..llm import (
    LLMProvider,
    OpenAIProvider,
    OllamaProvider,
    LemonadeProvider,
    LLMRouter,
    CostOptimizer,
)


class LLMConfigError(Exception):
    """Exception raised for LLM configuration errors."""
    pass


class LLMConfigLoader:
    """Loads and manages LLM provider configurations."""
    
    PROVIDER_CLASSES = {
        "openai": OpenAIProvider,
        "ollama": OllamaProvider,
        "lemonade": LemonadeProvider,
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Path to LLM config YAML file. If None, uses default.
        """
        if config_path:
            self.config_path = Path(config_path)
        else:
            # Default config path relative to this file
            default_path = Path(__file__).parent.parent / "configs" / "llm_providers.yaml"
            self.config_path = default_path
        
        self._config: Dict[str, Any] = {}
        self._providers: Dict[str, LLMProvider] = {}
        self._router: Optional[LLMRouter] = None
        self._cost_optimizer: Optional[CostOptimizer] = None
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise LLMConfigError(f"Config file not found: {self.config_path}")
        
        try:
            with open(self.config_path, "r") as f:
                self._config = yaml.safe_load(f)
            logger.info(f"Loaded LLM config from: {self.config_path}")
            return self._config
        except yaml.YAMLError as e:
            raise LLMConfigError(f"Failed to parse YAML config: {e}")
        except Exception as e:
            raise LLMConfigError(f"Failed to load config: {e}")
    
    def validate_config(self) -> List[str]:
        """
        Validate the loaded configuration.
        
        Returns:
            List of validation warnings (empty if valid)
        """
        warnings = []
        
        if not self._config:
            self.load_config()
        
        # Check required sections
        if "providers" not in self._config:
            raise LLMConfigError("Missing 'providers' section in config")
        
        # Check at least one provider is enabled
        providers = self._config.get("providers", {})
        enabled_providers = [
            name for name, config in providers.items()
            if config.get("enabled", False)
        ]
        
        if not enabled_providers:
            warnings.append("No LLM providers are enabled")
        
        # Check routing config
        routing = self._config.get("routing", {})
        default_provider = routing.get("default_provider")
        if default_provider and default_provider not in providers:
            warnings.append(f"Default provider '{default_provider}' not in providers list")
        elif default_provider and not providers.get(default_provider, {}).get("enabled"):
            warnings.append(f"Default provider '{default_provider}' is disabled")
        
        return warnings
    
    def create_provider(self, name: str, provider_config: Dict[str, Any]) -> LLMProvider:
        """
        Create a provider instance from configuration.
        
        Args:
            name: Provider name
            provider_config: Provider configuration dict
            
        Returns:
            Configured provider instance
        """
        provider_type = provider_config.get("type")
        if not provider_type:
            raise LLMConfigError(f"Provider '{name}' missing 'type' field")
        
        provider_class = self.PROVIDER_CLASSES.get(provider_type)
        if not provider_class:
            raise LLMConfigError(
                f"Unknown provider type '{provider_type}'. "
                f"Available: {list(self.PROVIDER_CLASSES.keys())}"
            )
        
        config = provider_config.get("config", {})
        return provider_class(name=name, config=config)
    
    async def initialize_providers(
        self,
        provider_names: Optional[List[str]] = None,
    ) -> Dict[str, bool]:
        """
        Initialize specified or all enabled providers.
        
        Args:
            provider_names: List of provider names to initialize. If None, initializes all enabled.
            
        Returns:
            Dict mapping provider names to initialization success
        """
        if not self._config:
            self.load_config()
        
        providers_config = self._config.get("providers", {})
        results = {}
        
        for name, config in providers_config.items():
            # Skip if not enabled or not in requested list
            if not config.get("enabled", False):
                continue
            if provider_names and name not in provider_names:
                continue
            
            try:
                provider = self.create_provider(name, config)
                success = await provider.initialize()
                results[name] = success
                
                if success:
                    self._providers[name] = provider
                    logger.success(f"Initialized provider: {name}")
                else:
                    logger.warning(f"Failed to initialize provider: {name}")
                    
            except Exception as e:
                logger.error(f"Error creating provider '{name}': {e}")
                results[name] = False
        
        return results
    
    def create_router(self) -> LLMRouter:
        """
        Create and configure an LLMRouter with all initialized providers.
        
        Returns:
            Configured LLMRouter instance
        """
        router = LLMRouter()
        
        # Register all initialized providers
        for name, provider in self._providers.items():
            is_default = (
                name == self._config.get("routing", {}).get("default_provider")
            )
            router.register_provider(provider, is_default=is_default)
        
        # Set up task routing rules from task_profiles
        task_profiles = self._config.get("task_profiles", {})
        for task_type, profile in task_profiles.items():
            priorities = profile.get("priority", [])
            for i, provider_name in enumerate(priorities):
                if provider_name in self._providers:
                    router.set_routing_rule(task_type, provider_name)
                    break  # Use highest priority available provider
        
        self._router = router
        return router
    
    def create_cost_optimizer(self) -> CostOptimizer:
        """
        Create and configure a CostOptimizer.
        
        Returns:
            Configured CostOptimizer instance
        """
        routing_config = self._config.get("routing", {})
        cost_config = routing_config.get("cost_optimization", {})
        latency_config = routing_config.get("latency", {})
        
        cost_budget = cost_config.get("monthly_budget")
        latency_threshold = latency_config.get("max_latency_ms", 5000)
        
        optimizer = CostOptimizer(
            providers=self._providers,
            cost_budget=cost_budget,
            latency_threshold_ms=latency_threshold,
        )
        
        self._cost_optimizer = optimizer
        return optimizer
    
    async def setup(
        self,
        provider_names: Optional[List[str]] = None,
    ) -> tuple[LLMRouter, CostOptimizer]:
        """
        Complete setup: load config, initialize providers, create router and optimizer.
        
        Args:
            provider_names: Optional list of specific providers to initialize
            
        Returns:
            Tuple of (LLMRouter, CostOptimizer)
        """
        self.load_config()
        warnings = self.validate_config()
        for warning in warnings:
            logger.warning(warning)
        
        await self.initialize_providers(provider_names)
        router = self.create_router()
        optimizer = self.create_cost_optimizer()
        
        return router, optimizer
    
    @property
    def providers(self) -> Dict[str, LLMProvider]:
        """Get initialized providers."""
        return self._providers.copy()
    
    @property
    def router(self) -> Optional[LLMRouter]:
        """Get configured router (if setup() was called)."""
        return self._router
    
    @property
    def cost_optimizer(self) -> Optional[CostOptimizer]:
        """Get configured cost optimizer (if setup() was called)."""
        return self._cost_optimizer
    
    @property
    def config(self) -> Dict[str, Any]:
        """Get loaded configuration."""
        return self._config.copy()

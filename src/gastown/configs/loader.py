"""
Configuration loader for Gastown Swarm.
"""

from pathlib import Path
from typing import Any

import yaml
from loguru import logger


class ConfigLoader:
    """Loads and manages configuration from YAML files."""

    def __init__(self, config_dir: str | None = None):
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent
        self._configs: dict[str, dict[str, Any]] = {}

    def load_config(self, name: str) -> dict[str, Any]:
        """
        Load a configuration by name (without .yaml extension).

        Args:
            name: Configuration name (e.g., 'model_frontier', 'model_local')

        Returns:
            Configuration dictionary
        """
        if name in self._configs:
            return self._configs[name]

        config_path = self.config_dir / f"{name}.yaml"
        if not config_path.exists():
            logger.warning(f"Configuration file not found: {config_path}")
            return {}

        try:
            with open(config_path) as f:
                config = yaml.safe_load(f)
            self._configs[name] = config
            logger.debug(f"Loaded configuration: {name}")
            return config
        except Exception as e:
            logger.error(f"Failed to load configuration {name}: {e}")
            return {}

    def get_model_config(self, agent_role: str | None = None) -> dict[str, Any]:
        """
        Get model configuration, optionally for a specific agent role.

        Args:
            agent_role: If provided, returns model config for that role.
                       If None, returns global model config.

        Returns:
            Model configuration dictionary
        """
        # Default to frontier config
        config = self.load_config("model_frontier")

        if not config:
            return {}

        if agent_role and "agents" in config:
            agent_config = config["agents"].get(agent_role, {})
            # Merge with global model config
            global_model = config.get("model", {})
            return {**global_model, **agent_config}

        return config.get("model", {})

    def get_execution_config(self) -> dict[str, Any]:
        """Get execution configuration."""
        config = self.load_config("model_frontier")
        return config.get("execution", {})

    def get_logging_config(self) -> dict[str, Any]:
        """Get logging configuration."""
        config = self.load_config("model_frontier")
        return config.get("logging", {})

    def list_configs(self) -> list[str]:
        """List available configuration files."""
        configs = []
        for path in self.config_dir.glob("*.yaml"):
            configs.append(path.stem)
        return configs


# Global loader instance
_loader = ConfigLoader()


def load_config(name: str) -> dict[str, Any]:
    """Convenience function to load a configuration."""
    return _loader.load_config(name)


def get_model_config(agent_role: str | None = None) -> dict[str, Any]:
    """Convenience function to get model configuration."""
    return _loader.get_model_config(agent_role)


def get_execution_config() -> dict[str, Any]:
    """Convenience function to get execution configuration."""
    return _loader.get_execution_config()


def get_logging_config() -> dict[str, Any]:
    """Convenience function to get logging configuration."""
    return _loader.get_logging_config()

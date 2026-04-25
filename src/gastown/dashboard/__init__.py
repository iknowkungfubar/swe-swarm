"""
Dashboard module for Gastown Swarm.

Provides web interface for monitoring and controlling agents and tasks.
"""

from .app import create_app

__all__ = ["create_app"]
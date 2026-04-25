"""
Teams module for Gastown Swarm.

Provides specialized team modules for collaborative agent work.
"""

from .base_team import BaseTeam
from .writers_room_team import WritersRoomTeam
from .marketing_team import MarketingTeam

__all__ = ["BaseTeam", "WritersRoomTeam", "MarketingTeam"]

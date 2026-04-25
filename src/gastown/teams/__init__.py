"""
Teams module for Gastown Swarm.

Provides specialized team modules for collaborative agent work.
"""

from .base_team import BaseTeam
from .writers_room_team import WritersRoomTeam
from .marketing_team import MarketingTeam
from .sales_team import SalesTeam

__all__ = ["BaseTeam", "WritersRoomTeam", "MarketingTeam", "SalesTeam"]

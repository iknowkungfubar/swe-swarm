"""
Teams module for Gastown Swarm.

Provides specialized team modules for collaborative agent work.
"""

from .base_team import BaseTeam
from .writers_room_team import WritersRoomTeam
from .marketing_team import MarketingTeam
from .sales_team import SalesTeam
from .youtube_team import YouTubeTeam

__all__ = ["BaseTeam", "WritersRoomTeam", "MarketingTeam", "SalesTeam", "YouTubeTeam"]

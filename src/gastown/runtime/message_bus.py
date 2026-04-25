"""
Simple message bus for inter-agent communication.
"""

import asyncio
from collections.abc import Awaitable, Callable

from loguru import logger

from ..agents.base_agent import AgentMessage


class MessageBus:
    """Async message bus with pub/sub support."""

    def __init__(self):
        self.subscribers: dict[
            str, list[Callable[[AgentMessage], Awaitable[None]]]
        ] = {}
        self.queue = asyncio.Queue()
        self._running = False
        self._task = None

    async def start(self):
        """Start the message bus processing loop."""
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._process_loop())
        logger.info("Message bus started")

    async def stop(self):
        """Stop the message bus."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Message bus stopped")

    async def publish(self, message: AgentMessage):
        """Publish a message to the bus."""
        await self.queue.put(message)
        logger.debug(f"Message published: {message.id} ({message.message_type})")

    async def subscribe(
        self, recipient: str, callback: Callable[[AgentMessage], Awaitable[None]]
    ):
        """Subscribe a callback for messages addressed to a specific recipient."""
        if recipient not in self.subscribers:
            self.subscribers[recipient] = []
        self.subscribers[recipient].append(callback)
        logger.debug(f"Subscribed {recipient} to message bus")

    async def _process_loop(self):
        """Process messages from the queue."""
        while self._running:
            try:
                message = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                await self._dispatch(message)
            except TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error in message bus loop: {e}")

    async def _dispatch(self, message: AgentMessage):
        """Dispatch a message to appropriate subscribers."""
        recipients = []

        # Direct message
        if message.recipient in self.subscribers:
            recipients.extend(self.subscribers[message.recipient])

        # Broadcast (recipient="*")
        if "*" in self.subscribers:
            recipients.extend(self.subscribers["*"])

        if not recipients:
            logger.warning(f"No subscribers for message to {message.recipient}")
            return

        # Call all subscribers
        for callback in recipients:
            try:
                await callback(message)
            except Exception as e:
                logger.error(f"Error in subscriber callback: {e}")

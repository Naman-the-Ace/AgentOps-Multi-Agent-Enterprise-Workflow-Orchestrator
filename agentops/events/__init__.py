"""Event-driven workflow triggers — Redis Streams + Kafka adapters."""

from agentops.events.dispatcher import EventDispatcher, WorkflowTrigger
from agentops.events.redis_consumer import RedisStreamsConsumer

__all__ = ["EventDispatcher", "RedisStreamsConsumer", "WorkflowTrigger"]

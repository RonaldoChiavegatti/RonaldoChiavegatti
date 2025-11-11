import redis
import json
from typing import Dict, Any

from services.document_service.application.ports.output.message_queue import (
    MessageQueue,
)


class RedisMessageQueue(MessageQueue):
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url, decode_responses=True)

    def publish_message(self, queue_name: str, message: Dict[str, Any]):
        self.redis_client.rpush(queue_name, json.dumps(message))

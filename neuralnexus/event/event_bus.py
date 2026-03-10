from datetime import datetime
import pytz
from typing import List, Dict
from neuralnexus.utils.logger import setup_logger

logger = setup_logger(__name__)

class EventBus:
    def __init__(self):
        self.events: List[Dict] = []
        self.timezone = pytz.timezone("Asia/Kolkata")
    
    def publish_event(self, event_type: str, data: dict):
        """Publish an event to the event bus"""
        timestamp = datetime.now(self.timezone)
        event = {
            "timestamp": timestamp.isoformat(),
            "event_type": event_type,
            "data": data
        }
        self.events.append(event)
        logger.info(f"Event published: {event_type}")
    
    def get_events(self, limit: int = 100) -> List[Dict]:
        """Get recent events from the timeline"""
        return self.events[-limit:]
    
    def clear_events(self):
        """Clear all events"""
        self.events.clear()
        logger.info("Event timeline cleared")

event_bus = EventBus()

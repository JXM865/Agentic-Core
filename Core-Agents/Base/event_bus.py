"""
MTP 2.0 - Event Bus System
Core messaging system for agent communication
Linear Issue: MYT-5
"""

import asyncio
from typing import Dict, List, Callable, Any
from datetime import datetime
import json

class EventBus:
    """Central message hub for all MTP agents"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_history: List[Dict] = []
        print("🚀 MTP EventBus initialized!")
    
    async def publish(self, topic: str, message: Any, source: str = "system"):
        """Publish message to all subscribers of a topic"""
        msg_data = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "source": source,
            "message": message
        }
        
        # Store in history
        self.message_history.append(msg_data)
        
        # Notify subscribers
        if topic in self.subscribers:
            print(f"📤 Publishing to {topic}: {message}")
            for callback in self.subscribers[topic]:
                await callback(msg_data)
        
        return msg_data
    
    def subscribe(self, topic: str, callback: Callable):
        """Subscribe to receive messages on a topic"""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        
        self.subscribers[topic].append(callback)
        print(f"📥 New subscription to '{topic}'")
        return True
    
    def get_history(self, topic: str = None, limit: int = 10):
        """Get message history"""
        history = self.message_history
        if topic:
            history = [m for m in history if m["topic"] == topic]
        return history[-limit:]


# Test the EventBus
async def test_eventbus():
    """Test our messaging system"""
    print("\n" + "="*50)
    print("🧪 TESTING MTP EVENT BUS")
    print("="*50)
    
    # Create bus
    bus = EventBus()
    
    # Create a test subscriber
    async def price_handler(msg):
        print(f"💰 Price Handler received: {msg['message']}")
    
    async def sentiment_handler(msg):
        print(f"😊 Sentiment Handler received: {msg['message']}")
    
    # Subscribe to topics
    bus.subscribe("price_update", price_handler)
    bus.subscribe("sentiment", sentiment_handler)
    
    # Publish some messages
    await bus.publish("price_update", {"BTC": 45000}, "price_agent")
    await bus.publish("sentiment", {"score": 0.75, "trend": "bullish"}, "sentiment_agent")
    await bus.publish("unknown_topic", "This won't be received", "test")
    
    # Show history
    print("\n📜 Message History:")
    for msg in bus.get_history():
        print(f"  - [{msg['timestamp']}] {msg['topic']}: {msg['message']}")
    
    print("\n✅ EventBus test complete!")

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_eventbus())
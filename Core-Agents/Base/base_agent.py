"""
MTP 2.0 - Base Agent Class
Abstract base class for all MTP agents with EventBus integration
Linear Issue: MYT-5
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from .event_bus import EventBus


class BaseAgent(ABC):
    """Abstract base class for all MTP agents with EventBus communication"""
    
    def __init__(self, agent_id: str, event_bus: EventBus):
        """
        Initialize the base agent
        
        Args:
            agent_id: Unique identifier for this agent
            event_bus: Shared EventBus instance for communication
        """
        self.agent_id = agent_id
        self.event_bus = event_bus
        self.is_running = False
        self.subscriptions = []
        self.start_time = None
        
        print(f"🤖 Agent '{agent_id}' initialized")
    
    async def start(self):
        """Start the agent and set up subscriptions"""
        if self.is_running:
            print(f"⚠️  Agent '{self.agent_id}' is already running")
            return
        
        self.is_running = True
        self.start_time = datetime.now()
        
        # Set up subscriptions
        await self.setup_subscriptions()
        
        # Run agent-specific startup logic
        await self.on_start()
        
        print(f"✅ Agent '{self.agent_id}' started successfully")
    
    async def stop(self):
        """Stop the agent and clean up resources"""
        if not self.is_running:
            print(f"⚠️  Agent '{self.agent_id}' is not running")
            return
        
        self.is_running = False
        
        # Run agent-specific cleanup
        await self.on_stop()
        
        # Clear subscriptions (EventBus doesn't have unsubscribe, so we just track them)
        self.subscriptions.clear()
        
        print(f"🛑 Agent '{self.agent_id}' stopped")
    
    async def publish_message(self, topic: str, message: Any):
        """
        Publish a message to the EventBus
        
        Args:
            topic: The topic to publish to
            message: The message data to publish
        """
        await self.event_bus.publish(topic, message, source=self.agent_id)
    
    async def handle_message(self, msg_data: Dict[str, Any]):
        """
        Handle incoming messages from EventBus subscriptions
        
        Args:
            msg_data: Message data from EventBus
        """
        try:
            # Don't process our own messages
            if msg_data.get("source") == self.agent_id:
                return
            
            # Call agent-specific message processing
            await self.process_message(msg_data)
            
        except Exception as e:
            print(f"❌ Error in {self.agent_id} handling message: {e}")
            await self.on_error(e, msg_data)
    
    def subscribe_to_topic(self, topic: str):
        """
        Subscribe to a topic on the EventBus
        
        Args:
            topic: The topic to subscribe to
        """
        self.event_bus.subscribe(topic, self.handle_message)
        self.subscriptions.append(topic)
        print(f"📥 Agent '{self.agent_id}' subscribed to '{topic}'")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        uptime = None
        if self.start_time:
            uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "agent_id": self.agent_id,
            "is_running": self.is_running,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "uptime_seconds": uptime,
            "subscriptions": self.subscriptions.copy()
        }
    
    # Abstract methods that must be implemented by subclasses
    
    @abstractmethod
    async def setup_subscriptions(self):
        """Set up EventBus subscriptions for this agent"""
        pass
    
    @abstractmethod
    async def process_message(self, msg_data: Dict[str, Any]):
        """Process incoming messages from subscribed topics"""
        pass
    
    @abstractmethod
    async def on_start(self):
        """Called when agent starts - implement agent-specific startup logic"""
        pass
    
    @abstractmethod
    async def on_stop(self):
        """Called when agent stops - implement agent-specific cleanup logic"""
        pass
    
    async def on_error(self, error: Exception, msg_data: Optional[Dict[str, Any]] = None):
        """
        Handle errors - can be overridden by subclasses
        
        Args:
            error: The exception that occurred
            msg_data: Message data that caused the error (if applicable)
        """
        print(f"❌ Error in agent '{self.agent_id}': {error}")
        if msg_data:
            print(f"   Message: {msg_data}")

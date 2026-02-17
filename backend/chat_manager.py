"""
Chat Manager - Handles conversation memory and context.
"""

from typing import Dict, List
from datetime import datetime
import uuid

class ChatManager:
    """Manages chat conversations with memory."""
    
    def __init__(self):
        self.conversations: Dict[str, List[Dict]] = {}
    
    def create_conversation(self) -> str:
        """Create new conversation and return ID."""
        conv_id = str(uuid.uuid4())
        self.conversations[conv_id] = []
        return conv_id
    
    def add_message(self, conv_id: str, role: str, content: str, metadata: Dict = None):
        """Add message to conversation."""
        if conv_id not in self.conversations:
            self.conversations[conv_id] = []
        
        self.conversations[conv_id].append({
            "role": role,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        })
    
    def get_conversation(self, conv_id: str) -> List[Dict]:
        """Get full conversation history."""
        return self.conversations.get(conv_id, [])
    
    def get_context(self, conv_id: str, max_messages: int = 5) -> str:
        """Get recent context as string for LLM."""
        conv = self.get_conversation(conv_id)
        recent = conv[-max_messages:] if len(conv) > max_messages else conv
        
        context = ""
        for msg in recent:
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content']}\n"
        
        return context.strip()

chat_manager = ChatManager()

# 🤖 Agentic-Core

Open-source multi-agent orchestration framework for building AI-powered systems.

## ✨ Features

- **Event-Driven Architecture** - Agents communicate via EventBus pub/sub system
- **Modular Design** - Plug-and-play agent architecture
- **Async Operations** - Built on Python asyncio for high performance
- **100% Python** - No complex dependencies
- **Production Ready** - Comprehensive error handling and logging

## 🚀 Quick Start

```python
from Base.event_bus import EventBus
from Architecture.architect_agent import ArchitectAgent

# Create event bus
bus = EventBus()

# Initialize agents
architect = ArchitectAgent("architect-01", bus)

# Agents now communicate autonomously!
## 📦 Included Agents

### L1 Core Agents

- **Architect Agent** - System design and architecture planning
- **Code Generator Agent** - Automated code generation from specifications
- **QA Agent** - Automated testing and quality assurance
- **Documentation Agent** - Auto-generates comprehensive documentation

## 🏗️ Architecture

```
Core-Agents/
├── Base/           # Core framework components
│   ├── event_bus.py      # Event-driven communication
│   ├── base_agent.py     # Base agent class
│   └── agent_factory.py  # Agent instantiation
├── Architecture/   # System design agents
├── CodeGen/       # Code generation agents
├── Documentation/ # Documentation agents
└── QA/           # Quality assurance agents
```

## 💡 Use Cases

- **Automated software development** - Streamline the entire development lifecycle
- **AI-powered code generation** - Generate production-ready code from specifications
- **Self-documenting systems** - Maintain up-to-date documentation automatically
- **Autonomous testing pipelines** - Continuous quality assurance without manual intervention

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-core.git
cd agentic-core

# Install in development mode
pip install -e .
```

## 🔧 Usage

### Basic Agent Setup

```python
from Base.event_bus import EventBus
from Base.base_agent import BaseAgent

class MyAgent(BaseAgent):
    async def handle_event(self, event):
        # Process incoming events
        print(f"Processing: {event}")
        
# Initialize
bus = EventBus()
agent = MyAgent("my-agent", bus)
```

### Event Communication

```python
# Publish events
await bus.publish("user.request", {"data": "hello"})

# Subscribe to events
@bus.subscribe("user.request")
async def handle_user_request(event):
    return {"response": "world"}
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/agentic-core&type=Date)](https://star-history.com/#yourusername/agentic-core&Date)

---

**Built with ❤️ by [Jen Mensah](https://github.com/JXM865)**

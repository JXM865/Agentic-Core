"""
Core-Agents Package

This package contains all the core agents for the MTP-2.0 system:
- Base: Base classes and utilities
- Architecture: Architect agent for system design
- CodeGen: Code generation agent
- QA: Quality assurance agent
- Documentation: Documentation generation agent
"""

# Import base classes
from .Base.base_agent import BaseAgent
from .Base.event_bus import EventBus
from .Base.agent_factory import AgentFactory

# Import agents
from .Architecture.architect_agent import ArchitectAgent
from .CodeGen.code_generator_agent import CodeGeneratorAgent
from .QA.qa_agent import QAAgent
from .Documentation.docs_agent import DocumentationAgent

__all__ = [
    'BaseAgent',
    'EventBus', 
    'AgentFactory',
    'ArchitectAgent',
    'CodeGeneratorAgent',
    'QAAgent',
    'DocumentationAgent'
]

__version__ = "2.0.0"

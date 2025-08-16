import os
import json
from typing import Dict, Any, List, Optional, Type
from pathlib import Path

from Base.base_agent import BaseAgent
from Base.event_bus import EventBus
from Architecture.architect_agent import ArchitectAgent
from CodeGen.code_generator_agent import CodeGeneratorAgent
from QA.qa_agent import QAAgent
from Documentation.docs_agent import DocumentationAgent


class AgentFactory:
    """Factory class for creating and managing agent teams for different projects."""
    
    def __init__(self, event_bus: EventBus, config_base_path: str = "projects"):
        """
        Initialize the AgentFactory.
        
        Args:
            event_bus: EventBus instance for agent communication
            config_base_path: Base path where project configurations are stored
        """
        self.event_bus = event_bus
        self.config_base_path = Path(config_base_path)
        self.registered_agents: Dict[str, Type[BaseAgent]] = {}
        self._register_core_agents()
    
    def _register_core_agents(self) -> None:
        """Register the core agent types."""
        self.registered_agents.update({
            "architect": ArchitectAgent,
            "codegen": CodeGeneratorAgent,
            "qa": QAAgent,
            "docs": DocumentationAgent
        })
    
    def register_agent(self, agent_name: str, agent_class: Type[BaseAgent]) -> None:
        """
        Register a custom agent type.
        
        Args:
            agent_name: Name to register the agent under
            agent_class: Agent class that inherits from BaseAgent
        """
        if not issubclass(agent_class, BaseAgent):
            raise ValueError(f"Agent class {agent_class} must inherit from BaseAgent")
        
        self.registered_agents[agent_name] = agent_class
    
    def load_project_config(self, project_name: str) -> Dict[str, Any]:
        """
        Load configuration for a specific project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Project configuration dictionary
            
        Raises:
            FileNotFoundError: If project config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        config_path = self.config_base_path / project_name / "config.json"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Project config not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def create_agent(self, agent_type: str, config: Dict[str, Any]) -> BaseAgent:
        """
        Create a single agent instance.
        
        Args:
            agent_type: Type of agent to create
            config: Configuration for the agent
            
        Returns:
            Configured agent instance
            
        Raises:
            ValueError: If agent type is not registered
        """
        if agent_type not in self.registered_agents:
            raise ValueError(f"Unknown agent type: {agent_type}. "
                           f"Available types: {list(self.registered_agents.keys())}")
        
        agent_class = self.registered_agents[agent_type]
        agent_id = config.get("agent_id", f"{agent_type}_agent")
        
        # Special handling for agents that accept config parameter
        if agent_type in ["qa", "docs"]:
            return agent_class(agent_id, self.event_bus, config)
        else:
            return agent_class(agent_id, self.event_bus)
    
    def create_core_agents(self, project_config: Dict[str, Any]) -> Dict[str, BaseAgent]:
        """
        Create the core agent team (architect, codegen, qa, docs).
        
        Args:
            project_config: Project configuration dictionary
            
        Returns:
            Dictionary mapping agent names to agent instances
        """
        core_agent_types = ["architect", "codegen", "qa", "docs"]
        agents = {}
        
        for agent_type in core_agent_types:
            agent_config = project_config.get("agents", {}).get(agent_type, {})
            # Merge project-level config with agent-specific config
            merged_config = {**project_config.get("common", {}), **agent_config}
            agents[agent_type] = self.create_agent(agent_type, merged_config)
        
        return agents
    
    def create_project_agents(self, project_name: str) -> Dict[str, BaseAgent]:
        """
        Create all agents for a specific project based on its configuration.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Dictionary mapping agent names to agent instances
        """
        project_config = self.load_project_config(project_name)
        
        # Start with core agents
        agents = self.create_core_agents(project_config)
        
        # Add any custom agents defined in the project config
        custom_agents = project_config.get("custom_agents", {})
        for agent_name, agent_config in custom_agents.items():
            agent_type = agent_config.get("type")
            if not agent_type:
                raise ValueError(f"Custom agent '{agent_name}' missing 'type' field")
            
            # Merge project-level config with agent-specific config
            merged_config = {**project_config.get("common", {}), **agent_config}
            agents[agent_name] = self.create_agent(agent_type, merged_config)
        
        return agents
    
    def list_available_agents(self) -> List[str]:
        """
        Get list of all registered agent types.
        
        Returns:
            List of available agent type names
        """
        return list(self.registered_agents.keys())
    
    def create_agent_team(self, team_config: Dict[str, Dict[str, Any]]) -> Dict[str, BaseAgent]:
        """
        Create a custom team of agents from a team configuration.
        
        Args:
            team_config: Dictionary mapping agent names to their configurations
                        Each config should include a 'type' field
            
        Returns:
            Dictionary mapping agent names to agent instances
        """
        agents = {}
        
        for agent_name, config in team_config.items():
            agent_type = config.get("type")
            if not agent_type:
                raise ValueError(f"Agent '{agent_name}' missing 'type' field")
            
            agents[agent_name] = self.create_agent(agent_type, config)
        
        return agents

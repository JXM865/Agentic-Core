#!/usr/bin/env python3
"""
Documentation Agent for automated documentation generation.

This agent handles code documentation, API docs, README generation,
and user guides across multiple formats and programming languages.
"""

import asyncio
import logging
import json
import re
import ast
import inspect
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

from Base.base_agent import BaseAgent


class DocumentationAgent(BaseAgent):
    """
    Documentation Agent that automatically generates comprehensive documentation
    from code, architecture designs, and test results.
    """
    
    def __init__(self, agent_id: str, event_bus, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Documentation Agent.
        
        Args:
            agent_id: Unique identifier for this agent
            event_bus: Event bus for inter-agent communication
            config: Optional configuration dictionary
        """
        super().__init__(agent_id, event_bus)
        
        # Set up logging
        self.logger = logging.getLogger(f"MTP.{self.agent_id}")
        self.logger.setLevel(logging.INFO)
        
        # Documentation-specific configuration
        self.supported_formats = config.get('supported_formats', ['markdown', 'rst', 'html']) if config else ['markdown', 'rst', 'html']
        self.default_format = config.get('default_format', 'markdown') if config else 'markdown'
        self.include_examples = config.get('include_examples', True) if config else True
        self.generate_diagrams = config.get('generate_diagrams', True) if config else True
        
        # Documentation templates
        self.templates = {
            'function_doc': self._get_function_doc_template(),
            'class_doc': self._get_class_doc_template(),
            'api_doc': self._get_api_doc_template(),
            'readme': self._get_readme_template()
        }
        
        # Note: Event subscriptions are handled in setup_subscriptions() method
        
        print(f"📚 Documentation Agent {agent_id} initialized")
    
    async def start(self):
        """Start the Documentation Agent"""
        print("📚 Starting Documentation Agent...")
        await super().start()
        
        await self._setup_docs_environment()
        print("📚 Documentation Agent started successfully")
    
    async def stop(self):
        """Stop the Documentation Agent"""
        print("📚 Stopping Documentation Agent...")
        await self._cleanup_docs_environment()
        await super().stop()
        print("📚 Documentation Agent stopped")
    
    # Note: handle_message is inherited from BaseAgent and calls process_message
    
    async def generate_code_docs(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Generate comprehensive code documentation including docstrings and inline docs.
        
        Args:
            code: Source code to document
            language: Programming language of the code
            
        Returns:
            Dictionary containing generated documentation
        """
        print("📝 Generating code documentation...")
        
        try:
            if language.lower() == "python":
                return await self._generate_python_docs(code)
            elif language.lower() == "javascript":
                return await self._generate_javascript_docs(code)
            else:
                return await self._generate_generic_docs(code, language)
        
        except Exception as e:
            self.logger.error(f"Error generating code docs: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "documentation": ""
            }
    
    async def generate_api_docs(self, code: str, format: str = "openapi") -> Dict[str, Any]:
        """
        Generate API documentation in OpenAPI/Swagger format.
        
        Args:
            code: Source code containing API definitions
            format: Documentation format (openapi, swagger, etc.)
            
        Returns:
            Dictionary containing API documentation
        """
        print("🔌 Generating API documentation...")
        
        # Mock API documentation generation
        api_docs = {
            "openapi": "3.0.0",
            "info": {
                "title": "Generated API Documentation",
                "version": "1.0.0",
                "description": "Auto-generated API documentation from code analysis"
            },
            "paths": {
                "/api/example": {
                    "get": {
                        "summary": "Example endpoint",
                        "description": "An example API endpoint extracted from code",
                        "responses": {
                            "200": {
                                "description": "Successful response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "message": {"type": "string"},
                                                "data": {"type": "object"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "components": {
                "schemas": {
                    "ApiResponse": {
                        "type": "object",
                        "properties": {
                            "success": {"type": "boolean"},
                            "message": {"type": "string"},
                            "data": {"type": "object"}
                        }
                    }
                }
            }
        }
        
        return {
            "success": True,
            "format": format,
            "documentation": api_docs,
            "generated_at": datetime.now().isoformat()
        }
    
    async def generate_readme(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate or update README files for the project.
        
        Args:
            project_info: Information about the project
            
        Returns:
            Dictionary containing README content
        """
        print("📄 Generating README documentation...")
        
        project_name = project_info.get("name", "Project")
        description = project_info.get("description", "A software project")
        features = project_info.get("features", [])
        
        readme_content = f"""# {project_name}

{description}

## Features

{self._format_feature_list(features)}

## Installation

```bash
# Installation instructions here
```

## Usage

```python
# Usage examples here
```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
"""
        return readme_content
    
    def _format_feature_list(self, features: List[str]) -> str:
        """Format a list of features for markdown."""
        if not features:
            return "- No features specified"
        
        return "\n".join(f"- {feature}" for feature in features)
    
    # Required abstract methods from BaseAgent
    
    async def setup_subscriptions(self):
        """Set up EventBus subscriptions for documentation-related topics"""
        self.subscribe_to_topic("code.generated")
        self.subscribe_to_topic("architecture.spec_generated")
        self.subscribe_to_topic("test.results")
        self.subscribe_to_topic("docs.generate_request")
        self.subscribe_to_topic("docs.update_request")
        
        print("📋 Documentation Agent subscriptions configured")
    
    async def process_message(self, msg_data: Dict[str, Any]):
        """
        Process incoming messages and route to appropriate handlers
        
        Args:
            msg_data: Message data from EventBus
        """
        topic = msg_data.get("topic")
        message = msg_data.get("message")
        source = msg_data.get("source")
        
        print(f"📚 Docs processing: {topic} from {source}")
        
        try:
            if topic == "code.generated":
                await self._handle_code_generated(message)
            elif topic == "architecture.spec_generated":
                await self._handle_architecture_spec(message)
            elif topic == "test.results":
                await self._handle_test_results(message)
            elif topic == "docs.generate_request":
                await self._handle_docs_request(message)
            elif topic == "docs.update_request":
                await self._handle_docs_update(message)
            else:
                print(f"⚠️  Unknown topic received: {topic}")
                
        except Exception as e:
            print(f"❌ Error processing {topic}: {e}")
            await self.on_error(e, msg_data)
    
    async def on_start(self):
        """Initialize Documentation agent on startup"""
        print("🚀 Documentation Agent starting up...")
        
        # Initialize documentation templates and output directories
        await self._setup_docs_environment()
        
        print("✅ Documentation Agent startup complete")
    
    async def on_stop(self):
        """Cleanup on agent shutdown"""
        print("🛑 Documentation Agent shutting down...")
        
        # Save any pending documentation and cleanup
        await self._cleanup_docs_environment()
        
        print("✅ Documentation Agent shutdown complete")
    
    # Helper methods for message handling
    
    async def _handle_code_generated(self, message: Dict[str, Any]):
        """Handle newly generated code for documentation"""
        print("📝 Processing generated code for documentation...")
        
        code_path = message.get("code_path", "")
        language = message.get("language", "python")
        
        if code_path:
            # Generate documentation for the code
            docs = await self.generate_code_documentation(code_path, language)
            
            # Publish documentation results
            await self.publish_message("docs.code_documented", {
                "code_path": code_path,
                "language": language,
                "documentation": docs,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_architecture_spec(self, message: Dict[str, Any]):
        """Handle architecture specifications for documentation"""
        print("🏗️ Processing architecture spec for documentation...")
        
        spec_name = message.get("specification", "")
        document = message.get("document", {})
        
        if spec_name and document:
            # Generate architecture documentation
            arch_docs = await self.generate_architecture_docs(spec_name, document)
            
            # Publish architecture documentation
            await self.publish_message("docs.architecture_documented", {
                "specification": spec_name,
                "documentation": arch_docs,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_test_results(self, message: Dict[str, Any]):
        """Handle test results for documentation"""
        print("🧪 Processing test results for documentation...")
        
        test_path = message.get("test_path", "")
        results = message.get("results", {})
        
        if test_path and results:
            # Generate test documentation
            test_docs = await self.generate_test_docs(test_path, results)
            
            # Publish test documentation
            await self.publish_message("docs.test_documented", {
                "test_path": test_path,
                "documentation": test_docs,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_docs_request(self, message: Dict[str, Any]):
        """Handle documentation generation requests"""
        print("📋 Processing documentation generation request...")
        
        doc_type = message.get("type", "general")
        target = message.get("target", "")
        
        if target:
            # Generate requested documentation
            if doc_type == "api":
                docs = await self.generate_api_documentation(target)
            elif doc_type == "readme":
                docs = await self.generate_readme(target, 
                    message.get("description", ""), 
                    message.get("features", []))
            else:
                docs = await self.generate_user_guide(target, message.get("content", {}))
            
            # Publish documentation
            await self.publish_message("docs.generated", {
                "type": doc_type,
                "target": target,
                "documentation": docs,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_docs_update(self, message: Dict[str, Any]):
        """Handle documentation update requests"""
        print("🔄 Processing documentation update request...")
        
        doc_path = message.get("path", "")
        updates = message.get("updates", {})
        
        if doc_path and updates:
            # Update existing documentation
            updated_docs = await self._update_documentation(doc_path, updates)
            
            # Publish update results
            await self.publish_message("docs.updated", {
                "path": doc_path,
                "documentation": updated_docs,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _setup_docs_environment(self):
        """Setup documentation environment"""
        print("🔧 Setting up Documentation environment...")
        # Initialize documentation directories, templates, etc.
    
    async def _cleanup_docs_environment(self):
        """Cleanup documentation environment"""
        print("🧹 Cleaning up Documentation environment...")
        # Save pending docs, cleanup temp files, etc.
    
    async def _update_documentation(self, doc_path: str, updates: Dict[str, Any]) -> str:
        """Update existing documentation with new information"""
        # Implementation for updating documentation
        return f"Updated documentation at {doc_path}"
    
    # Template methods
    
    def _get_function_doc_template(self) -> str:
        """Get template for function documentation"""
        return """
        Args:
            {args}
        
        Returns:
            {returns}
        
        Raises:
            {raises}
        
        Example:
            {example}
        """
    
    def _get_class_doc_template(self) -> str:
        """Get template for class documentation"""
        return """
        {description}
        
        Attributes:
            {attributes}
        
        Methods:
            {methods}
        
        Example:
            {example}
        """
    
    def _get_api_doc_template(self) -> str:
        """Get template for API documentation"""
        return """
        # API Documentation
        
        ## Endpoints
        
        {endpoints}
        
        ## Authentication
        
        {auth}
        
        ## Examples
        
        {examples}
        """
    
    def _get_readme_template(self) -> str:
        """Get template for README documentation"""
        return """
        # {title}
        
        {description}
        
        ## Installation
        
        {installation}
        
        ## Usage
        
        {usage}
        
        ## Contributing
        
        {contributing}
        """
"""
MTP 2.0 - Code Generator Agent
L1-C: Generates code from specifications
Fixed version with proper imports and EventBus integration
"""

import asyncio
from datetime import datetime
import logging
from typing import Dict, Any, List

# Fixed imports using absolute imports (works with sys.path manipulation)
from Base.base_agent import BaseAgent
from Base.event_bus import EventBus


class CodeGeneratorAgent(BaseAgent):
    """
    Code Generator Agent - L1-C
    Generates high-quality code from specifications
    """
    
    def __init__(self, agent_id: str, event_bus: EventBus):
        """Initialize the Code Generator Agent."""
        super().__init__(agent_id, event_bus)
        
        # Set up logging
        self.logger = logging.getLogger(f"MTP.{self.agent_id}")
        self.logger.setLevel(logging.INFO)
        
        # Initialize code templates
        self.templates = self._initialize_templates()
        
        # Quality standards
        self.quality_standards = {
            'line_length': 88,
            'test_coverage': 85,
            'documentation_required': True,
            'type_hints': True
        }
        
        self.logger.info("Code Generator Agent initialized with templates and quality standards")

    async def setup_subscriptions(self):
        """Set up EventBus subscriptions for code generation requests"""
        self.subscribe_to_topic("architecture.spec_generated")
        self.subscribe_to_topic("development.generation_request")
        self.subscribe_to_topic("code.template_request")
        self.subscribe_to_topic("quality.standards_updated")
        
        self.logger.info("Code Generator subscriptions established")

    async def process_message(self, msg_data: Dict[str, Any]):
        """Process incoming messages and route to appropriate handlers"""
        topic = msg_data.get("topic")
        message = msg_data.get("message")
        source = msg_data.get("source")
        
        self.logger.info(f"Processing message from {source} on topic: {topic}")
        
        try:
            if topic == "architecture.spec_generated":
                await self._handle_spec_generated(message)
            elif topic == "development.generation_request":
                await self._handle_generation_request(message)
            elif topic == "code.template_request":
                await self._handle_template_request(message)
            elif topic == "quality.standards_updated":
                await self._handle_standards_update(message)
            else:
                self.logger.warning(f"Unhandled topic: {topic}")
                
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            await self.on_error(e, msg_data)

    async def generate_code(self, specification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate code from technical specifications
        
        Args:
            specification: Technical specification from architect
            
        Returns:
            Generated code with metadata
        """
        try:
            self.logger.info(f"Generating code for: {specification.get('name', 'unnamed')}")
            
            # Extract specification details
            name = specification.get('name', 'GeneratedClass')
            code_type = specification.get('type', 'class')
            methods = specification.get('methods', [])
            description = specification.get('description', f'Generated {code_type}')
            
            # Generate code based on type
            if code_type == 'class':
                generated_code = self._generate_class(name, methods, description)
            elif code_type == 'agent':
                generated_code = self._generate_agent(name, specification)
            elif code_type == 'function':
                generated_code = self._generate_function(name, specification)
            else:
                generated_code = self._generate_default(name, code_type)
            
            # Create result with metadata
            result = {
                'code': generated_code,
                'type': code_type,
                'name': name,
                'timestamp': datetime.now().isoformat(),
                'specification': specification,
                'quality_metrics': {
                    'lines': len(generated_code.split('\n')),
                    'has_docstrings': '"""' in generated_code
                },
                'file_path': f"Generated/{name.lower()}.py"
            }
            
            # Publish the generated code to EventBus
            await self.publish_message('code.generated', result)
            
            self.logger.info(f"Code generation complete for {name}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating code: {e}")
            # Still publish error result
            error_result = {
                'code': f"# Error generating code: {str(e)}",
                'type': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'specification': specification
            }
            await self.publish_message('code.generated', error_result)
            return error_result

    def _initialize_templates(self) -> Dict[str, str]:
        """Initialize code generation templates."""
        return {
            'class': '''"""
{description}
"""

class {name}:
    """Auto-generated class: {name}"""
    
    def __init__(self):
        """Initialize {name}"""
        {init_body}
    
    {methods}
''',
            'agent': '''"""
{description} - MTP Agent
"""

from Base.base_agent import BaseAgent
from Base.event_bus import EventBus

class {name}(BaseAgent):
    """Auto-generated MTP Agent: {name}"""
    
    def __init__(self, event_bus: EventBus):
        super().__init__("{agent_id}", event_bus)
    
    async def setup_subscriptions(self):
        """Set up EventBus subscriptions"""
        pass
    
    async def process_message(self, msg_data: Dict[str, Any]):
        """Process incoming messages"""
        pass
    
    async def on_start(self):
        """Agent startup logic"""
        pass
    
    async def on_stop(self):
        """Agent cleanup logic"""
        pass
''',
            'function': '''def {name}({params}) -> {return_type}:
    """
    {description}
    """
    {body}
'''
        }

    def _generate_class(self, name: str, methods: List[str], description: str) -> str:
        """Generate a Python class."""
        method_strs = []
        for method in methods:
            method_strs.append(f'''    def {method}(self):
        """Implement {method}."""
        # TODO: Implement {method}
        pass''')
        
        return self.templates['class'].format(
            name=name,
            description=description,
            init_body="pass",
            methods='\n\n'.join(method_strs) if method_strs else '    pass'
        )

    def _generate_agent(self, name: str, specification: Dict[str, Any]) -> str:
        """Generate an agent class."""
        return self.templates['agent'].format(
            name=name,
            description=specification.get('description', f'{name} Agent'),
            agent_id=name.lower().replace(' ', '_')
        )

    def _generate_function(self, name: str, specification: Dict[str, Any]) -> str:
        """Generate a function."""
        return self.templates['function'].format(
            name=name,
            params=specification.get('params', ''),
            return_type=specification.get('return_type', 'None'),
            description=specification.get('description', f'{name} function'),
            body=specification.get('body', '    pass')
        )

    def _generate_default(self, name: str, code_type: str) -> str:
        """Generate default code when type is not recognized."""
        return f'''# Generated {code_type}: {name}
# Type '{code_type}' not recognized, using default template

def {name.lower()}_placeholder():
    """Placeholder for {name}."""
    # TODO: Implement {name}
    pass
'''

    def apply_template(self, template_name: str, params: Dict[str, Any] = None) -> str:
        """
        Apply a code template with parameters
        
        Args:
            template_name: Name of the template to apply ('class', 'agent', 'function')
            params: Parameters to fill in the template
            
        Returns:
            Generated code string
        """
        if params is None:
            params = {}
        
        # Get the template
        if template_name not in self.templates:
            self.logger.error(f"Template '{template_name}' not found")
            return f"# Error: Template '{template_name}' not found"
        
        template = self.templates[template_name]
        
        # Set up safe default parameters
        safe_params = {
            'name': 'GeneratedCode',
            'description': 'Auto-generated code',
            'init_body': 'pass',
            'methods': 'pass',
            'params': '',
            'return_type': 'None',
            'body': '    pass',
            'agent_id': 'generated_agent'
        }
        
        # Update with provided params
        safe_params.update(params)
        
        try:
            # Apply template with parameters
            result = template.format(**safe_params)
            self.logger.info(f"Template '{template_name}' applied successfully")
            return result
        except KeyError as e:
            self.logger.error(f"Missing template parameter: {e}")
            return f"# Error: Missing template parameter: {e}"
        except Exception as e:
            self.logger.error(f"Template formatting error: {e}")
            return f"# Error formatting template: {str(e)}"

    async def _handle_spec_generated(self, message: Dict[str, Any]):
        """Handle architecture specification messages"""
        self.logger.info("Processing architecture specification")
        
        # Extract the specification document
        specification_doc = message.get('document', message)
        
        # Convert architecture spec to code generation specs
        if isinstance(specification_doc, dict):
            # Extract components from the architecture
            components = specification_doc.get('components', [])
            project_name = specification_doc.get('project_name', 'GeneratedProject')
            
            if components:
                # Generate code for each component
                for component in components:
                    await self.generate_code({
                        'name': component.get('name', 'Component'),
                        'type': component.get('type', 'class'),
                        'methods': component.get('methods', []),
                        'description': component.get('description', f"Generated component from {project_name}")
                    })
            else:
                # Generate a main class based on the project
                await self.generate_code({
                    'name': project_name.replace(' ', ''),
                    'type': 'class',
                    'methods': ['initialize', 'process', 'cleanup'],
                    'description': f"Main class for {project_name}"
                })
        else:
            self.logger.warning("Received specification is not a dictionary, generating default code")
            await self.generate_code({
                'name': 'GeneratedFromSpec',
                'type': 'class',
                'methods': ['process'],
                'description': 'Generated from architecture specification'
            })

    async def _handle_generation_request(self, message: Dict[str, Any]):
        """Handle direct code generation requests"""
        self.logger.info("Processing code generation request")
        await self.generate_code(message)

    async def _handle_template_request(self, message: Dict[str, Any]):
        """Handle template creation/update requests"""
        self.logger.info("Processing template request")
        template_name = message.get("name")
        template_content = message.get("content")
        
        if template_name and template_content:
            self.templates[template_name] = template_content
            
            result = {
                "template_name": template_name,
                "status": "updated",
                "timestamp": datetime.now().isoformat()
            }
            
            await self.publish_message("code.templates_updated", result)
            self.logger.info(f"Template updated: {template_name}")

    async def _handle_standards_update(self, message: Dict[str, Any]):
        """Handle quality standards updates"""
        self.logger.info("Updating quality standards")
        if isinstance(message, dict):
            self.quality_standards.update(message)
            self.logger.info(f"Quality standards updated: {list(message.keys())}")

    async def on_start(self):
        """Agent startup logic"""
        self.logger.info("Code Generator Agent starting up")
        self.logger.info(f"Loaded {len(self.templates)} code templates")

    async def on_stop(self):
        """Agent cleanup logic"""
        self.logger.info("Code Generator Agent shutting down")


# Test function
async def test_code_generator_agent():
    """Test the Code Generator Agent"""
    print("\n" + "="*60)
    print("🧪 TESTING CODE GENERATOR AGENT")
    print("="*60)
    
    # Create EventBus and Agent
    from Base.event_bus import EventBus
    event_bus = EventBus()
    code_gen = CodeGeneratorAgent("test_codegen", event_bus)
    
    # Start the agent
    await code_gen.start()
    
    # Test code generation
    spec = {
        "name": "UserService",
        "type": "class",
        "methods": ["create_user", "get_user", "update_user"],
        "description": "Service for user management"
    }
    
    code_result = await code_gen.generate_code(spec)
    print(f"📝 Generated code preview:\n{code_result['code'][:300]}...")
    
    # Show agent status
    status = code_gen.get_status()
    print(f"\n📊 Agent Status: {status}")
    
    # Stop the agent
    await code_gen.stop()
    
    print("\n✅ Code Generator Agent test complete!")


if __name__ == "__main__":
    # Run the test
    asyncio.run(test_code_generator_agent())
    
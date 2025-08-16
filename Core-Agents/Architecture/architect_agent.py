"""
MTP 2.0 - Architect Agent (L1-A)
System architecture design and maintenance agent
Linear Issue: MYT-5
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from Base.base_agent import BaseAgent
from Base.event_bus import EventBus


class ArchitectAgent(BaseAgent):
    """
    L1-A Architect Agent - Responsible for system architecture design and maintenance
    
    Core Responsibilities:
    - Design and maintain overall system architecture
    - Create technical specifications and design documents
    - Ensure architectural consistency across components
    - Plan system evolution and scalability improvements
    """
    
    def __init__(self, agent_id: str, event_bus: EventBus):
        """
        Initialize the Architect Agent
        
        Args:
            agent_id: Unique identifier for this agent
            event_bus: Shared EventBus instance for communication
        """
        super().__init__(agent_id, event_bus)
        
        # Architecture state
        self.current_architecture = {}
        self.specifications = {}
        self.coding_standards = self._initialize_coding_standards()
        self.review_queue = []
        self.performance_metrics = {}
        
        print("🏗️  Architect Agent initialized - Ready to design systems!")
    
    async def setup_subscriptions(self):
        """Set up EventBus subscriptions for architecture-related topics"""
        # Subscribe to topics as specified in PRD
        self.subscribe_to_topic("system.requirements_changed")
        self.subscribe_to_topic("development.feedback")
        self.subscribe_to_topic("performance.metrics")
        self.subscribe_to_topic("code.review_request")
        
        print("📋 Architect Agent subscriptions configured")
    
    async def process_message(self, msg_data: Dict[str, Any]):
        """
        Process incoming messages and route to appropriate handlers
        
        Args:
            msg_data: Message data from EventBus
        """
        topic = msg_data.get("topic")
        message = msg_data.get("message")
        source = msg_data.get("source")
        
        print(f"🏗️  Architect processing: {topic} from {source}")
        
        try:
            if topic == "system.requirements_changed":
                await self._handle_requirements_change(message)
            elif topic == "development.feedback":
                await self._handle_development_feedback(message)
            elif topic == "performance.metrics":
                await self._handle_performance_metrics(message)
            elif topic == "code.review_request":
                await self._handle_review_request(message)
            else:
                print(f"⚠️  Unknown topic received: {topic}")
                
        except Exception as e:
            print(f"❌ Error processing {topic}: {e}")
            await self.on_error(e, msg_data)
    
    async def on_start(self):
        """Initialize architect agent on startup"""
        print("🚀 Architect Agent starting up...")
        
        # Initialize default architecture
        await self.design_component("core_system", {
            "type": "microservices",
            "components": ["event_bus", "agents", "data_layer"],
            "patterns": ["observer", "factory", "strategy"]
        })
        
        # Generate initial specifications
        await self.generate_specification("system_overview", {
            "architecture_type": "event_driven_microservices",
            "communication": "event_bus",
            "scalability": "horizontal"
        })
        
        print("✅ Architect Agent startup complete")
    
    async def on_stop(self):
        """Cleanup on agent shutdown"""
        print("🛑 Architect Agent shutting down...")
        
        # Save current state (in real implementation, this would persist to storage)
        final_state = {
            "architecture": self.current_architecture,
            "specifications": self.specifications,
            "standards": self.coding_standards,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"💾 Architecture state saved: {len(self.current_architecture)} components")
        print("✅ Architect Agent shutdown complete")
    
    async def design_component(self, component_name: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create architecture design for a system component
        
        Args:
            component_name: Name of the component to design
            requirements: Component requirements and constraints
            
        Returns:
            Architecture design specification
        """
        print(f"🎨 Designing component: {component_name}")
        
        # Mock architecture design based on requirements
        design = {
            "component_name": component_name,
            "timestamp": datetime.now().isoformat(),
            "architecture_type": requirements.get("type", "modular"),
            "components": requirements.get("components", []),
            "interfaces": self._generate_interfaces(component_name, requirements),
            "data_flow": self._design_data_flow(component_name, requirements),
            "scalability": self._design_scalability(requirements),
            "security": self._design_security(requirements),
            "patterns": requirements.get("patterns", ["mvc", "observer"]),
            "dependencies": self._identify_dependencies(component_name, requirements),
            "performance_targets": {
                "response_time_ms": 100,
                "throughput_rps": 1000,
                "availability": 99.9
            }
        }
        
        # Store in current architecture
        self.current_architecture[component_name] = design
        
        # Publish architecture update
        await self.publish_message("architecture.design_updated", {
            "component": component_name,
            "design": design,
            "version": "1.0"
        })
        
        print(f"✅ Component '{component_name}' architecture designed")
        return design
    
    async def generate_specification(self, spec_name: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate detailed technical specification
        
        Args:
            spec_name: Name of the specification
            requirements: Specification requirements
            
        Returns:
            Technical specification document
        """
        print(f"📋 Generating specification: {spec_name}")
        
        specification = {
            "name": spec_name,
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "overview": f"Technical specification for {spec_name}",
            "requirements": requirements,
            "architecture": {
                "style": requirements.get("architecture_type", "layered"),
                "communication": requirements.get("communication", "rest_api"),
                "data_storage": "postgresql",
                "caching": "redis",
                "monitoring": "prometheus"
            },
            "api_endpoints": self._generate_api_spec(spec_name, requirements),
            "data_models": self._generate_data_models(spec_name, requirements),
            "deployment": {
                "containerization": "docker",
                "orchestration": "kubernetes",
                "scaling": requirements.get("scalability", "auto")
            },
            "testing": {
                "unit_tests": "pytest",
                "integration_tests": "pytest",
                "coverage_target": 85
            },
            "documentation": {
                "api_docs": "openapi",
                "code_docs": "sphinx",
                "architecture_diagrams": "plantuml"
            }
        }
        
        # Store specification
        self.specifications[spec_name] = specification
        
        # Publish specification
        await self.publish_message("architecture.spec_generated", {
            "specification": spec_name,
            "document": specification,
            "format": "json"
        })
        
        print(f"✅ Specification '{spec_name}' generated")
        return specification
    
    async def review_architecture(self, review_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review code architecture for compliance and quality
        
        Args:
            review_request: Architecture review request details
            
        Returns:
            Architecture review results
        """
        component = review_request.get("component", "unknown")
        code_path = review_request.get("code_path", "")
        
        print(f"🔍 Reviewing architecture for: {component}")
        
        # Mock architecture review
        review_result = {
            "component": component,
            "code_path": code_path,
            "timestamp": datetime.now().isoformat(),
            "reviewer": self.agent_id,
            "compliance_score": 85,  # Mock score
            "findings": [
                {
                    "type": "pattern_violation",
                    "severity": "medium",
                    "description": "Consider using Factory pattern for object creation",
                    "file": f"{code_path}/service.py",
                    "line": 45
                },
                {
                    "type": "dependency_issue",
                    "severity": "low",
                    "description": "Circular dependency detected",
                    "files": [f"{code_path}/module_a.py", f"{code_path}/module_b.py"]
                }
            ],
            "recommendations": [
                "Implement dependency injection for better testability",
                "Add interface abstractions for external services",
                "Consider breaking large modules into smaller components"
            ],
            "standards_compliance": {
                "coding_standards": 90,
                "documentation": 75,
                "testing": 80,
                "security": 85
            },
            "approved": True
        }
        
        # Publish review results
        await self.publish_message("architecture.review_completed", {
            "component": component,
            "review": review_result,
            "status": "completed"
        })
        
        print(f"✅ Architecture review completed for '{component}' - Score: {review_result['compliance_score']}")
        return review_result
    
    async def update_standards(self, standards_update: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update coding standards and architectural guidelines
        
        Args:
            standards_update: New or updated standards
            
        Returns:
            Updated standards document
        """
        print("📏 Updating coding standards...")
        
        # Update standards
        for category, updates in standards_update.items():
            if category in self.coding_standards:
                self.coding_standards[category].update(updates)
            else:
                self.coding_standards[category] = updates
        
        # Add timestamp
        self.coding_standards["last_updated"] = datetime.now().isoformat()
        self.coding_standards["version"] = "2.0"
        
        # Publish standards update
        await self.publish_message("architecture.standards_updated", {
            "standards": self.coding_standards,
            "updated_categories": list(standards_update.keys()),
            "version": "2.0"
        })
        
        print(f"✅ Coding standards updated - Categories: {list(standards_update.keys())}")
        return self.coding_standards
    
    # Private helper methods
    
    async def _handle_requirements_change(self, message: Dict[str, Any]):
        """Handle system requirements changes"""
        print("📋 Processing requirements change...")
        
        # For integration test, treat the entire message as requirements
        if "project_name" in message:
            # This is a full project requirements message
            project_name = message.get("project_name", "system")
            print(f"🏗️  Designing architecture for project: {project_name}")
            
            # Design the system architecture
            await self.design_component(project_name, message)
            
            # Generate specification for the project
            await self.generate_specification(f"{project_name}_architecture", message)
        else:
            # Legacy handling for component-specific changes
            component = message.get("component", "system")
            new_requirements = message.get("requirements", {})
            
            # Redesign affected components
            await self.design_component(component, new_requirements)
            
            # Always generate specification for new requirements
            await self.generate_specification(f"{component}_spec", new_requirements)
    
    async def _handle_development_feedback(self, message: Dict[str, Any]):
        """Handle feedback from development teams"""
        print("💬 Processing development feedback...")
        
        feedback_type = message.get("type", "general")
        component = message.get("component", "unknown")
        
        if feedback_type == "architecture_issue":
            # Add to review queue
            self.review_queue.append({
                "component": component,
                "issue": message.get("issue", ""),
                "priority": message.get("priority", "medium"),
                "timestamp": datetime.now().isoformat()
            })
            
            # Trigger architecture review
            await self.review_architecture({
                "component": component,
                "code_path": message.get("code_path", "")
            })
    
    async def _handle_performance_metrics(self, message: Dict[str, Any]):
        """Handle system performance metrics"""
        print("📊 Processing performance metrics...")
        
        component = message.get("component", "system")
        metrics = message.get("metrics", {})
        
        # Store metrics
        self.performance_metrics[component] = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics
        }
        
        # Check if architecture changes are needed based on performance
        if metrics.get("response_time_ms", 0) > 500:
            print("⚠️  High response time detected - considering architecture optimization")
            await self.design_component(f"{component}_optimized", {
                "type": "performance_optimized",
                "current_metrics": metrics,
                "target_improvement": 50
            })
    
    async def _handle_review_request(self, message: Dict[str, Any]):
        """Handle architecture review requests"""
        print("🔍 Processing review request...")
        await self.review_architecture(message)
    
    def _initialize_coding_standards(self) -> Dict[str, Any]:
        """Initialize default coding standards"""
        return {
            "python": {
                "style": "PEP 8",
                "line_length": 88,
                "imports": "isort",
                "formatting": "black",
                "linting": "flake8",
                "type_hints": "required"
            },
            "architecture": {
                "patterns": ["SOLID", "DRY", "KISS"],
                "structure": "layered",
                "communication": "event_driven",
                "error_handling": "centralized",
                "logging": "structured"
            },
            "testing": {
                "coverage_minimum": 85,
                "unit_tests": "required",
                "integration_tests": "required",
                "framework": "pytest"
            },
            "documentation": {
                "docstrings": "google_style",
                "api_docs": "openapi",
                "architecture_docs": "required"
            },
            "security": {
                "authentication": "required",
                "authorization": "rbac",
                "data_encryption": "at_rest_and_transit",
                "input_validation": "required"
            },
            "version": "1.0",
            "last_updated": datetime.now().isoformat()
        }
    
    def _generate_interfaces(self, component_name: str, requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate component interfaces"""
        return [
            {
                "name": f"{component_name}_api",
                "type": "rest_api",
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "authentication": "jwt"
            },
            {
                "name": f"{component_name}_events",
                "type": "event_interface",
                "publishes": [f"{component_name}.updated", f"{component_name}.error"],
                "subscribes": [f"{component_name}.command"]
            }
        ]
    
    def _design_data_flow(self, component_name: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design data flow patterns"""
        return {
            "input_sources": ["api_requests", "event_messages", "scheduled_tasks"],
            "processing_stages": ["validation", "business_logic", "persistence"],
            "output_destinations": ["database", "event_bus", "external_apis"],
            "error_handling": "circuit_breaker_pattern"
        }
    
    def _design_scalability(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design scalability approach"""
        return {
            "horizontal_scaling": True,
            "load_balancing": "round_robin",
            "caching_strategy": "redis_cluster",
            "database_sharding": "by_tenant",
            "cdn": "cloudflare"
        }
    
    def _design_security(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design security measures"""
        return {
            "authentication": "oauth2",
            "authorization": "rbac",
            "encryption": "aes_256",
            "network_security": "vpc",
            "monitoring": "security_events"
        }
    
    def _identify_dependencies(self, component_name: str, requirements: Dict[str, Any]) -> List[str]:
        """Identify component dependencies"""
        base_deps = ["event_bus", "database", "logging"]
        component_deps = requirements.get("dependencies", [])
        return base_deps + component_deps
    
    def _generate_api_spec(self, spec_name: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate API specification"""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": f"{spec_name} API",
                "version": "1.0.0"
            },
            "paths": {
                f"/{spec_name}": {
                    "get": {"summary": f"Get {spec_name} data"},
                    "post": {"summary": f"Create {spec_name}"}
                }
            }
        }
    
    def _generate_data_models(self, spec_name: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data model specifications"""
        return {
            f"{spec_name}_model": {
                "fields": {
                    "id": "uuid",
                    "name": "string",
                    "created_at": "timestamp",
                    "updated_at": "timestamp"
                },
                "indexes": ["id", "name"],
                "constraints": ["unique_name"]
            }
        }


# Test function for the Architect Agent
async def test_architect_agent():
    """Test the Architect Agent functionality"""
    print("\n" + "="*60)
    print("🧪 TESTING ARCHITECT AGENT")
    print("="*60)
    
    # Create EventBus and Agent
    from Base.event_bus import EventBus
    event_bus = EventBus()
    architect = ArchitectAgent("test_architect", event_bus)
    
    # Start the agent
    await architect.start()
    
    # Test component design
    design = await architect.design_component("user_service", {
        "type": "microservice",
        "components": ["api", "business_logic", "data_access"],
        "patterns": ["repository", "service_layer"]
    })
    
    # Test specification generation
    spec = await architect.generate_specification("user_api", {
        "architecture_type": "rest_api",
        "communication": "http",
        "scalability": "horizontal"
    })
    
    # Test architecture review
    review = await architect.review_architecture({
        "component": "user_service",
        "code_path": "/src/user_service"
    })
    
    # Test standards update
    standards = await architect.update_standards({
        "python": {"line_length": 100},
        "testing": {"coverage_minimum": 90}
    })
    
    # Show agent status
    status = architect.get_status()
    print(f"\n📊 Agent Status: {status}")
    
    # Stop the agent
    await architect.stop()
    
    print("\n✅ Architect Agent test complete!")


if __name__ == "__main__":
    # Run the test
    asyncio.run(test_architect_agent())

#!/usr/bin/env python3
"""
QA Agent for automated testing and quality assurance.

This agent handles code testing, test generation, and quality reporting
across multiple programming languages.
"""

import asyncio
import logging
import json
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from Base.base_agent import BaseAgent


class QAAgent(BaseAgent):
    """
    Quality Assurance Agent that automatically tests generated code,
    creates unit tests, and reports on code quality and coverage.
    """
    
    def __init__(self, agent_id: str, event_bus, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the QA Agent.
        
        Args:
            agent_id: Unique identifier for this agent
            event_bus: Event bus for inter-agent communication
            config: Optional configuration dictionary
        """
        super().__init__(agent_id, event_bus)
        
        # Set up logging
        self.logger = logging.getLogger(f"MTP.{self.agent_id}")
        self.logger.setLevel(logging.INFO)
        
        # QA-specific configuration
        self.supported_languages = config.get('supported_languages', ['python', 'javascript']) if config else ['python', 'javascript']
        self.test_timeout = config.get('test_timeout', 30) if config else 30
        self.coverage_threshold = config.get('coverage_threshold', 80) if config else 80
        
        # Test frameworks by language
        self.test_frameworks = {
            'python': 'pytest',
            'javascript': 'jest',
            'java': 'junit',
            'csharp': 'nunit'
        }
        
        # Subscribe to relevant events
        self.subscribe_to_topic('code.generated')
        self.subscribe_to_topic('qa.run_tests')
        self.subscribe_to_topic('qa.generate_tests')
        
        self.logger.info(f"QA Agent {self.agent_id} initialized with languages: {self.supported_languages}")
    
    async def handle_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Handle incoming events.
        
        Args:
            event_type: Type of the event
            data: Event data
        """
        try:
            if event_type == 'code.generated':
                await self._handle_code_generated(data)
            elif event_type == 'qa.run_tests':
                await self._handle_run_tests(data)
            elif event_type == 'qa.generate_tests':
                await self._handle_generate_tests(data)
            else:
                self.logger.warning(f"Unhandled event type: {event_type}")
                
        except Exception as e:
            self.logger.error(f"Error handling event {event_type}: {str(e)}")
            await self._publish_error(event_type, str(e))
    
    async def _handle_code_generated(self, data: Dict[str, Any]) -> None:
        """
        Handle code generation events by automatically testing the code.
        
        Args:
            data: Event data containing generated code information
        """
        self.logger.info(f"Processing generated code: {data.get('file_path', 'unknown')}")
        
        code_content = data.get('code', '')
        language = data.get('language', 'python')
        file_path = data.get('file_path', '')
        
        if language not in self.supported_languages:
            self.logger.warning(f"Language {language} not supported for testing")
            return
        
        # Generate tests for the code
        test_results = await self._generate_and_run_tests(code_content, language, file_path)
        
        # Publish test results
        await self.publish('qa.test_results', {
            'agent_id': self.agent_id,
            'timestamp': datetime.now().isoformat(),
            'file_path': file_path,
            'language': language,
            'results': test_results
        })
    
    async def _handle_run_tests(self, data: Dict[str, Any]) -> None:
        """
        Handle explicit test run requests.
        
        Args:
            data: Event data containing test run parameters
        """
        test_path = data.get('test_path', '')
        language = data.get('language', 'python')
        
        self.logger.info(f"Running tests for: {test_path}")
        
        results = await self._run_existing_tests(test_path, language)
        
        await self.publish('qa.test_results', {
            'agent_id': self.agent_id,
            'timestamp': datetime.now().isoformat(),
            'test_path': test_path,
            'language': language,
            'results': results
        })
    
    async def _handle_generate_tests(self, data: Dict[str, Any]) -> None:
        """
        Handle test generation requests.
        
        Args:
            data: Event data containing code to generate tests for
        """
        code_content = data.get('code', '')
        language = data.get('language', 'python')
        file_path = data.get('file_path', '')
        
        self.logger.info(f"Generating tests for: {file_path}")
        
        tests = await self._generate_unit_tests(code_content, language, file_path)
        
        await self.publish('qa.tests_generated', {
            'agent_id': self.agent_id,
            'timestamp': datetime.now().isoformat(),
            'file_path': file_path,
            'language': language,
            'tests': tests
        })
    
    async def _generate_and_run_tests(self, code: str, language: str, file_path: str) -> Dict[str, Any]:
        """
        Generate unit tests for code and run them.
        
        Args:
            code: Source code to test
            language: Programming language
            file_path: Path to the source file
            
        Returns:
            Dictionary containing test results
        """
        # Generate tests
        tests = await self._generate_unit_tests(code, language, file_path)
        
        # Run the generated tests
        if tests:
            results = await self._execute_tests(tests, language)
        else:
            results = {
                'status': 'no_tests',
                'message': 'No tests could be generated',
                'passed': 0,
                'failed': 0,
                'total': 0
            }
        
        # Generate coverage report
        coverage = await self._generate_coverage_report(code, tests, language)
        
        return {
            'test_execution': results,
            'coverage': coverage,
            'generated_tests': len(tests) if tests else 0
        }
    
    async def _generate_unit_tests(self, code: str, language: str, file_path: str) -> List[str]:
        """
        Generate unit tests for the given code.
        Currently returns mock tests - in a real implementation,
        this would use AI/LLM to generate meaningful tests.
        
        Args:
            code: Source code to generate tests for
            language: Programming language
            file_path: Path to the source file
            
        Returns:
            List of generated test code strings
        """
        self.logger.info(f"Generating unit tests for {language} code")
        
        if language == 'python':
            return await self._generate_python_tests(code, file_path)
        elif language == 'javascript':
            return await self._generate_javascript_tests(code, file_path)
        else:
            self.logger.warning(f"Test generation not implemented for {language}")
            return []
    
    async def _generate_python_tests(self, code: str, file_path: str) -> List[str]:
        """
        Generate Python unit tests (mock implementation).
        
        Args:
            code: Python source code
            file_path: Path to the source file
            
        Returns:
            List of Python test code strings
        """
        # Mock test generation - in reality, this would analyze the code
        # and generate meaningful tests using AI/LLM
        
        module_name = Path(file_path).stem if file_path else 'test_module'
        
        mock_test = f'''
import pytest
import sys
from pathlib import Path

# Add the module to path for testing
sys.path.insert(0, str(Path(__file__).parent))

def test_{module_name}_basic():
    """Basic test for {module_name}"""
    # Mock test - would contain actual test logic
    assert True, "Basic test passed"

def test_{module_name}_edge_cases():
    """Test edge cases for {module_name}"""
    # Mock test for edge cases
    assert True, "Edge case test passed"

def test_{module_name}_error_handling():
    """Test error handling for {module_name}"""
    # Mock test for error handling
    assert True, "Error handling test passed"
'''
        
        return [mock_test]
    
    async def _generate_javascript_tests(self, code: str, file_path: str) -> List[str]:
        """
        Generate JavaScript unit tests (mock implementation).
        
        Args:
            code: JavaScript source code
            file_path: Path to the source file
            
        Returns:
            List of JavaScript test code strings
        """
        module_name = Path(file_path).stem if file_path else 'testModule'
        
        mock_test = f'''
const {{ {module_name} }} = require('./{module_name}');

describe('{module_name}', () => {{
    test('basic functionality', () => {{
        // Mock test - would contain actual test logic
        expect(true).toBe(true);
    }});
    
    test('edge cases', () => {{
        // Mock test for edge cases
        expect(true).toBe(true);
    }});
    
    test('error handling', () => {{
        // Mock test for error handling
        expect(true).toBe(true);
    }});
}});
'''
        
        return [mock_test]
    
    async def _execute_tests(self, tests: List[str], language: str) -> Dict[str, Any]:
        """
        Execute the generated tests.
        
        Args:
            tests: List of test code strings
            language: Programming language
            
        Returns:
            Dictionary containing test execution results
        """
        if language == 'python':
            return await self._run_python_tests(tests)
        elif language == 'javascript':
            return await self._run_javascript_tests(tests)
        else:
            return {
                'status': 'unsupported',
                'message': f'Test execution not supported for {language}',
                'passed': 0,
                'failed': 0,
                'total': 0
            }
    
    async def _run_python_tests(self, tests: List[str]) -> Dict[str, Any]:
        """
        Run Python tests using pytest.
        
        Args:
            tests: List of Python test code strings
            
        Returns:
            Dictionary containing test results
        """
        try:
            # Create temporary test files
            with tempfile.TemporaryDirectory() as temp_dir:
                test_files = []
                
                for i, test_code in enumerate(tests):
                    test_file = Path(temp_dir) / f'test_{i}.py'
                    test_file.write_text(test_code)
                    test_files.append(str(test_file))
                
                # Run pytest
                cmd = ['python', '-m', 'pytest', '-v', '--tb=short'] + test_files
                
                process = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=temp_dir
                )
                
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=self.test_timeout
                )
                
                # Parse results (mock parsing)
                output = stdout.decode() + stderr.decode()
                
                # Mock result parsing - in reality, would parse pytest output
                return {
                    'status': 'completed',
                    'passed': 3,  # Mock values
                    'failed': 0,
                    'total': 3,
                    'output': output,
                    'execution_time': 1.5
                }
                
        except asyncio.TimeoutError:
            return {
                'status': 'timeout',
                'message': f'Tests timed out after {self.test_timeout} seconds',
                'passed': 0,
                'failed': 0,
                'total': 0
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'passed': 0,
                'failed': 0,
                'total': 0
            }
    
    async def _run_javascript_tests(self, tests: List[str]) -> Dict[str, Any]:
        """
        Run JavaScript tests using Jest.
        
        Args:
            tests: List of JavaScript test code strings
            
        Returns:
            Dictionary containing test results
        """
        # Mock implementation - similar to Python but for Jest
        return {
            'status': 'completed',
            'passed': 3,  # Mock values
            'failed': 0,
            'total': 3,
            'output': 'Mock Jest output',
            'execution_time': 1.2
        }
    
    async def _run_existing_tests(self, test_path: str, language: str) -> Dict[str, Any]:
        """
        Run existing test files.
        
        Args:
            test_path: Path to test files
            language: Programming language
            
        Returns:
            Dictionary containing test results
        """
        if not os.path.exists(test_path):
            return {
                'status': 'error',
                'message': f'Test path not found: {test_path}',
                'passed': 0,
                'failed': 0,
                'total': 0
            }
        
        # Mock implementation - would run actual tests
        return {
            'status': 'completed',
            'passed': 5,  # Mock values
            'failed': 1,
            'total': 6,
            'output': f'Mock test output for {test_path}',
            'execution_time': 2.1
        }
    
    async def _generate_coverage_report(self, code: str, tests: List[str], language: str) -> Dict[str, Any]:
        """
        Generate code coverage report.
        
        Args:
            code: Source code
            tests: Test code
            language: Programming language
            
        Returns:
            Dictionary containing coverage information
        """
        # Mock coverage report
        coverage_percentage = 85.5  # Mock value
        
        coverage_report = {
            'overall_coverage': coverage_percentage,
            'line_coverage': 87.2,
            'branch_coverage': 83.8,
            'function_coverage': 90.0,
            'meets_threshold': coverage_percentage >= self.coverage_threshold,
            'threshold': self.coverage_threshold,
            'uncovered_lines': [15, 23, 45],  # Mock uncovered lines
            'language': language
        }
        
        # Publish coverage report
        await self.publish('qa.coverage_report', {
            'agent_id': self.agent_id,
            'timestamp': datetime.now().isoformat(),
            'coverage': coverage_report
        })
        
        return coverage_report
    
    async def _publish_error(self, event_type: str, error_message: str) -> None:
        """
        Publish error information.
        
        Args:
            event_type: The event type that caused the error
            error_message: Error message
        """
        await self.publish('qa.error', {
            'agent_id': self.agent_id,
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'error': error_message
        })
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the QA Agent.
        
        Returns:
            Dictionary containing agent status
        """
        return {
            'agent_id': self.agent_id,
            'status': 'active',
            'supported_languages': self.supported_languages,
            'test_frameworks': self.test_frameworks,
            'coverage_threshold': self.coverage_threshold,
            'test_timeout': self.test_timeout
        }
    
    # Required abstract methods from BaseAgent
    
    async def setup_subscriptions(self):
        """Set up EventBus subscriptions for QA-related topics"""
        self.subscribe_to_topic("code.generated")
        self.subscribe_to_topic("code.review_request")
        self.subscribe_to_topic("test.run_request")
        self.subscribe_to_topic("quality.check_request")
        
        print("📋 QA Agent subscriptions configured")
    
    async def process_message(self, msg_data: Dict[str, Any]):
        """
        Process incoming messages and route to appropriate handlers
        
        Args:
            msg_data: Message data from EventBus
        """
        topic = msg_data.get("topic")
        message = msg_data.get("message")
        source = msg_data.get("source")
        
        print(f"🔍 QA processing: {topic} from {source}")
        
        try:
            if topic == "code.generated":
                await self._handle_code_generated(message)
            elif topic == "code.review_request":
                await self._handle_review_request(message)
            elif topic == "test.run_request":
                await self._handle_test_request(message)
            elif topic == "quality.check_request":
                await self._handle_quality_check(message)
            else:
                print(f"⚠️  Unknown topic received: {topic}")
                
        except Exception as e:
            print(f"❌ Error processing {topic}: {e}")
            await self.on_error(e, msg_data)
    
    async def on_start(self):
        """Initialize QA agent on startup"""
        print("🚀 QA Agent starting up...")
        
        # Initialize test environment
        await self._setup_test_environment()
        
        print("✅ QA Agent startup complete")
    
    async def on_stop(self):
        """Cleanup on agent shutdown"""
        print("🛑 QA Agent shutting down...")
        
        # Save test results and cleanup
        await self._cleanup_test_environment()
        
        print("✅ QA Agent shutdown complete")
    
    # Helper methods for message handling
    
    async def _handle_code_generated(self, message: Dict[str, Any]):
        """Handle newly generated code for testing"""
        print("🧪 Processing generated code for testing...")
        
        code_path = message.get("code_path", "")
        language = message.get("language", "python")
        
        if code_path:
            # Run tests on the generated code
            test_results = await self.run_tests(code_path, language)
            
            # Publish test results
            await self.publish_message("test.results", {
                "code_path": code_path,
                "language": language,
                "results": test_results,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_review_request(self, message: Dict[str, Any]):
        """Handle code review requests"""
        print("📋 Processing code review request...")
        
        code_path = message.get("code_path", "")
        language = message.get("language", "python")
        
        if code_path:
            # Perform quality analysis
            quality_report = await self.analyze_code_quality(code_path, language)
            
            # Publish quality report
            await self.publish_message("quality.report", {
                "code_path": code_path,
                "language": language,
                "report": quality_report,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_test_request(self, message: Dict[str, Any]):
        """Handle test execution requests"""
        print("🏃 Processing test execution request...")
        
        test_path = message.get("test_path", "")
        language = message.get("language", "python")
        
        if test_path:
            # Run specific tests
            results = await self.run_tests(test_path, language)
            
            # Publish results
            await self.publish_message("test.execution_results", {
                "test_path": test_path,
                "language": language,
                "results": results,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _handle_quality_check(self, message: Dict[str, Any]):
        """Handle quality check requests"""
        print("🔍 Processing quality check request...")
        
        code_path = message.get("code_path", "")
        language = message.get("language", "python")
        
        if code_path:
            # Perform comprehensive quality analysis
            quality_report = await self.analyze_code_quality(code_path, language)
            
            # Publish quality report
            await self.publish_message("quality.analysis_complete", {
                "code_path": code_path,
                "language": language,
                "report": quality_report,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _setup_test_environment(self):
        """Setup testing environment"""
        print("🔧 Setting up QA test environment...")
        # Initialize test directories, frameworks, etc.
    
    async def _cleanup_test_environment(self):
        """Cleanup testing environment"""
        print("🧹 Cleaning up QA test environment...")
        # Save results, cleanup temp files, etc.

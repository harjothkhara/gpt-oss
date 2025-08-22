"""
Interactive Code Helper - Core Analysis Engine

This module provides the core functionality for analyzing code using gpt-oss-20b
with the Metal backend optimized for Apple Silicon.
"""

import datetime
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from gpt_oss.metal import Context, Model
from gpt_oss.tools.python_docker.docker_tool import PythonTool
from openai_harmony import (
    SystemContent,
    Message,
    Conversation,
    Role,
    load_harmony_encoding,
    HarmonyEncodingName,
    ReasoningEffort,
    StreamableParser,
    StreamState
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalysisType(Enum):
    """Types of code analysis available."""
    EXPLANATION = "explanation"
    IMPROVEMENT = "improvement"
    BUG_DETECTION = "bug_detection"
    LEARNING = "learning"


@dataclass
class CodeAnalysisRequest:
    """Request structure for code analysis."""
    code: str
    language: str
    analysis_type: AnalysisType
    user_level: str = "beginner"  # beginner, intermediate, advanced
    specific_question: Optional[str] = None


@dataclass
class CodeAnalysisResponse:
    """Response structure for code analysis."""
    analysis: str
    suggestions: List[str]
    examples: List[str]
    execution_result: Optional[str] = None
    error: Optional[str] = None


class CodeAnalyzer:
    """Main code analysis engine using gpt-oss-20b with Metal backend."""

    def __init__(self, model_path: str, context_length: int = 8192):
        """
        Initialize the code analyzer.

        Args:
            model_path: Path to the gpt-oss-20b Metal model file
            context_length: Maximum context length for the model
        """
        self.model_path = model_path
        self.context_length = context_length
        self.model = None
        self.context = None
        self.encoding = None
        self.python_tool = None

        self._initialize_model()
        self._initialize_harmony()
        self._initialize_tools()

    def _initialize_model(self):
        """Initialize the Metal model and context."""
        try:
            logger.info(f"Loading gpt-oss-20b model from {self.model_path}")
            self.model = Model(self.model_path)
            self.context = Context(self.model, context_length=self.context_length)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def _initialize_harmony(self):
        """Initialize the harmony encoding for chat format."""
        try:
            self.encoding = load_harmony_encoding(HarmonyEncodingName.HARMONY_GPT_OSS)
            logger.info("Harmony encoding initialized")
        except Exception as e:
            logger.error(f"Failed to initialize harmony encoding: {e}")
            raise

    def _initialize_tools(self):
        """Initialize available tools (Python execution)."""
        try:
            self.python_tool = PythonTool()
            logger.info("Python tool initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Python tool: {e}")
            self.python_tool = None

    def _create_system_prompt(self, analysis_type: AnalysisType, user_level: str) -> SystemContent:
        """Create a system prompt tailored for the specific analysis type."""

        base_instructions = {
            AnalysisType.EXPLANATION: f"""You are an expert programming tutor helping {user_level} programmers understand code.
Your goal is to explain code clearly and thoroughly, breaking down complex concepts into digestible parts.

For each piece of code:
1. Provide a high-level overview of what the code does
2. Explain each significant line or block of code
3. Highlight important programming concepts being used
4. Use simple, clear language appropriate for {user_level} level
5. Provide examples when helpful""",

            AnalysisType.IMPROVEMENT: f"""You are a code review expert helping {user_level} programmers improve their code.
Focus on practical, actionable suggestions that will make the code better.

For each piece of code:
1. Identify areas for improvement (performance, readability, best practices)
2. Suggest specific changes with explanations
3. Provide improved code examples
4. Explain why the improvements are beneficial
5. Consider {user_level} level - suggest improvements they can understand and implement""",

            AnalysisType.BUG_DETECTION: f"""You are a debugging expert helping {user_level} programmers find and fix issues in their code.
Focus on identifying potential problems and providing clear solutions.

For each piece of code:
1. Scan for syntax errors, logic errors, and potential runtime issues
2. Identify edge cases that might cause problems
3. Suggest specific fixes with explanations
4. Provide corrected code examples
5. Explain how to prevent similar issues in the future""",

            AnalysisType.LEARNING: f"""You are an interactive programming teacher helping {user_level} programmers learn through code examples.
Make learning engaging and progressive.

For each piece of code:
1. Explain the educational value and concepts demonstrated
2. Break down the learning objectives
3. Provide related exercises or variations to try
4. Suggest next steps for learning
5. Connect concepts to broader programming principles"""
        }

        system_content = (
            SystemContent.new()
            .with_reasoning_effort(ReasoningEffort.MEDIUM)
            .with_conversation_start_date(datetime.datetime.now().strftime("%Y-%m-%d"))
        )

        # Add Python tool if available for code execution
        if self.python_tool:
            system_content = system_content.with_tools(self.python_tool.tool_config)

        return system_content

    def _create_user_message(self, request: CodeAnalysisRequest) -> str:
        """Create a user message for the analysis request."""

        message_parts = [
            f"Please analyze this {request.language} code:",
            f"```{request.language}",
            request.code,
            "```",
            "",
            f"Analysis type: {request.analysis_type.value}",
            f"User level: {request.user_level}"
        ]

        if request.specific_question:
            message_parts.extend([
                "",
                f"Specific question: {request.specific_question}"
            ])

        return "\n".join(message_parts)

    async def analyze_code(self, request: CodeAnalysisRequest) -> CodeAnalysisResponse:
        """
        Analyze code based on the request parameters.

        Args:
            request: CodeAnalysisRequest containing code and analysis parameters

        Returns:
            CodeAnalysisResponse with analysis results
        """
        try:
            # Create system prompt
            system_content = self._create_system_prompt(request.analysis_type, request.user_level)
            system_message = Message.from_role_and_content(Role.SYSTEM, system_content)

            # Create user message
            user_content = self._create_user_message(request)
            user_message = Message.from_role_and_content(Role.USER, user_content)

            # Create conversation
            messages = [system_message, user_message]
            conversation = Conversation.from_messages(messages)

            # Generate response
            response_text = await self._generate_response(conversation)

            # Parse response into structured format
            analysis_response = self._parse_response(response_text, request)

            # Execute code if it's Python and execution is requested
            if (request.language.lower() == "python" and
                request.analysis_type in [AnalysisType.IMPROVEMENT, AnalysisType.BUG_DETECTION] and
                self.python_tool):
                try:
                    execution_result = await self._execute_python_code(request.code)
                    analysis_response.execution_result = execution_result
                except Exception as e:
                    analysis_response.execution_result = f"Execution error: {str(e)}"

            return analysis_response

        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return CodeAnalysisResponse(
                analysis=f"Analysis failed: {str(e)}",
                suggestions=[],
                examples=[],
                error=str(e)
            )

    async def _generate_response(self, conversation: Conversation) -> str:
        """Generate response using the Metal backend."""
        try:
            # Reset context for new conversation
            self.context.reset()

            # Render conversation to tokens
            tokens = self.encoding.render_conversation_for_completion(conversation, Role.ASSISTANT)

            # Add tokens to context
            for token in tokens:
                self.context.append(token)

            # Process the context
            self.context.process()

            # Generate response tokens
            response_tokens = []
            max_tokens = 1000  # Limit response length

            for _ in range(max_tokens):
                token = self.context.sample(temperature=0.7)
                response_tokens.append(token)
                self.context.append(token)

                # Check for stop tokens
                if token in self.encoding.stop_tokens_for_assistant_actions():
                    break

            # Decode response
            response_text = self.encoding.decode(response_tokens)
            return response_text

        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            raise

    def _parse_response(self, response_text: str, request: CodeAnalysisRequest) -> CodeAnalysisResponse:
        """Parse the model response into structured format."""
        try:
            # Simple parsing - in a production system, you might want more sophisticated parsing
            lines = response_text.strip().split('\n')

            analysis = response_text  # Full response as analysis
            suggestions = []
            examples = []

            # Extract suggestions (lines starting with specific patterns)
            for line in lines:
                line = line.strip()
                if line.startswith('- ') or line.startswith('* '):
                    suggestions.append(line[2:])
                elif '```' in line and len(examples) < 3:  # Limit examples
                    # Try to extract code examples
                    if line.count('```') >= 2:
                        start = line.find('```') + 3
                        end = line.rfind('```')
                        if start < end:
                            examples.append(line[start:end].strip())

            return CodeAnalysisResponse(
                analysis=analysis,
                suggestions=suggestions[:5],  # Limit to 5 suggestions
                examples=examples[:3]  # Limit to 3 examples
            )

        except Exception as e:
            logger.error(f"Response parsing failed: {e}")
            return CodeAnalysisResponse(
                analysis=response_text,
                suggestions=[],
                examples=[],
                error=f"Parsing error: {str(e)}"
            )

    async def _execute_python_code(self, code: str) -> str:
        """Execute Python code using the Python tool."""
        try:
            if not self.python_tool:
                return "Python execution not available"

            # Create a message for the Python tool
            python_message = Message.from_role_and_content(Role.ASSISTANT, code).with_recipient("python")

            # Process the code
            result_messages = []
            async for msg in self.python_tool.process(python_message):
                result_messages.append(msg)

            if result_messages:
                return result_messages[0].content[0].text
            else:
                return "No output from code execution"

        except Exception as e:
            logger.error(f"Code execution failed: {e}")
            return f"Execution error: {str(e)}"

    def get_supported_languages(self) -> List[str]:
        """Get list of supported programming languages."""
        return [
            "python", "javascript", "java", "cpp", "c", "csharp",
            "go", "rust", "php", "ruby", "swift", "kotlin", "typescript"
        ]

    def get_analysis_types(self) -> List[str]:
        """Get list of available analysis types."""
        return [analysis_type.value for analysis_type in AnalysisType]

"""
Demo version of the Interactive Code Helper
This runs without the gpt-oss model for demonstration purposes.
"""

import argparse
import datetime
from typing import List

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Interactive Code Helper - Demo",
    description="Demo version of AI-powered code learning assistant",
    version="1.0.0-demo"
)

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mock data for demo
SUPPORTED_LANGUAGES = [
    "python", "javascript", "java", "cpp", "c", "csharp",
    "go", "rust", "php", "ruby", "swift", "kotlin", "typescript"
]

ANALYSIS_TYPES = [
    "explanation", "improvement", "bug_detection", "learning"
]

def generate_mock_analysis(code: str, language: str, analysis_type: str, user_level: str) -> dict:
    """Generate mock analysis results for demo purposes."""

    # Analyze the actual code content to provide more specific explanations
    code_lines = code.strip().split('\n')

    if analysis_type == "explanation":
        # Generate specific analysis based on code content
        if "fibonacci" in code.lower():
            analysis = f"""**What this code actually does:**

**The `fibonacci(n)` function:**
This function calculates the nth number in the Fibonacci sequence using recursion. When you call `fibonacci(5)`, it breaks the problem down by calling `fibonacci(4) + fibonacci(3)`, which in turn call smaller versions of themselves. The base cases (n=0 returns 0, n=1 returns 1) stop the recursion. This creates a tree of function calls that eventually resolves to the correct Fibonacci number.

**The test loop at the bottom:**
This loop calls the fibonacci function for numbers 0 through 9 and prints each result. It's demonstrating how the function works by showing the first 10 Fibonacci numbers: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34.

**How the recursion works:**
When you call `fibonacci(4)`, it doesn't calculate the answer directly. Instead, it says "I need fibonacci(3) plus fibonacci(2)". Each of those calls breaks down further until you reach the base cases. The function calls stack up and then resolve backwards to give you the final answer."""

        elif "sort" in code.lower() or "bubble" in code.lower():
            analysis = f"""**What this code actually does:**

**The `bubbleSort(arr)` function:**
This function takes an unsorted array and returns it sorted in ascending order using the bubble sort algorithm. It works by repeatedly stepping through the array, comparing adjacent elements, and swapping them if they're in the wrong order. The name "bubble sort" comes from the way smaller elements "bubble" to the beginning of the array.

**The optimization with the `swapped` flag:**
The code includes a smart optimization - if it goes through an entire pass without swapping any elements, it knows the array is already sorted and breaks out early. This makes the algorithm more efficient for arrays that are already partially sorted.

**The nested loop structure:**
The outer loop controls how many passes through the array we make, while the inner loop does the actual comparing and swapping. Each pass guarantees that the largest unsorted element moves to its correct position at the end.

**The test code at the bottom:**
This creates a test array `[64, 34, 25, 12, 22, 11, 90]`, shows the original array, then calls bubbleSort on a copy and displays the sorted result. It demonstrates the function working on real data."""

        elif "class" in code.lower() and "account" in code.lower():
            analysis = f"""**What this code actually does:**

**The `BankAccount` class:**
This class creates a digital representation of a bank account. When you create a new BankAccount object, it stores the account holder's name, keeps track of the current balance, and maintains a history of all transactions.

**The `__init__` constructor:**
This sets up a new bank account when you create one. It takes the account holder's name and an optional starting balance (defaults to $0 if not provided). It also creates an empty list to track all transactions.

**The `deposit(amount)` method:**
This method adds money to the account. It first checks that you're depositing a positive amount, then adds it to the balance and records the transaction in the history. It returns True if successful, False if you try to deposit a negative amount.

**The `withdraw(amount)` method:**
This method removes money from the account, but only if you have enough funds and the amount is positive. It prevents overdrafts by checking that the withdrawal amount doesn't exceed the current balance. Like deposit, it records the transaction and returns True/False based on success.

**The `get_balance()` method:**
This is a simple getter method that returns the current account balance.

**The usage example at the bottom:**
This demonstrates the class in action - creating an account for "John Doe" with $1000, depositing $500, withdrawing $200, and then displaying the final balance of $1300."""

        else:
            # Generic but more specific analysis for other code
            analysis = f"""**What this code actually does:**

**Code Analysis:**
Looking at your {language} code, here's what's happening step by step:

"""
            # Try to identify key patterns and explain them
            for i, line in enumerate(code_lines[:10], 1):  # Analyze first 10 lines
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('//'):
                    if 'def ' in line or 'function ' in line:
                        func_name = line.split('(')[0].split()[-1]
                        analysis += f"**Line {i}:** Defines function '{func_name}' - this will contain the main logic\n"
                    elif 'if ' in line:
                        analysis += f"**Line {i}:** Conditional check - decides what to do based on a condition\n"
                    elif 'for ' in line or 'while ' in line:
                        analysis += f"**Line {i}:** Loop structure - repeats code multiple times\n"
                    elif 'return ' in line:
                        analysis += f"**Line {i}:** Returns a value - sends result back to whoever called this function\n"
                    elif '=' in line and not '==' in line:
                        var_name = line.split('=')[0].strip()
                        analysis += f"**Line {i}:** Assigns value to variable '{var_name}'\n"
                    elif 'print(' in line or 'console.log(' in line:
                        analysis += f"**Line {i}:** Outputs information to the screen/console\n"

            analysis += f"\n**Overall Purpose:** This {language} code appears to implement specific functionality that processes data and produces results."

        if "fibonacci" in code.lower():
            suggestions = [
                "Add memoization to avoid recalculating the same values (fibonacci(5) calculates fibonacci(3) multiple times)",
                "Include input validation: check if n is negative and handle appropriately",
                "Add a docstring explaining the mathematical sequence: F(n) = F(n-1) + F(n-2)",
                "Consider iterative approach for better performance with large numbers",
                "Add type hints: def fibonacci(n: int) -> int"
            ]
        elif "sort" in code.lower():
            suggestions = [
                "The algorithm is O(n²) - consider quicksort or mergesort for better performance on large arrays",
                "Add input validation to ensure arr is actually an array",
                "The early termination with 'swapped' flag is good - keeps it!",
                "Consider adding a parameter to sort in descending order: bubbleSort(arr, reverse=False)",
                "Add JSDoc comments to explain the algorithm complexity"
            ]
        elif "account" in code.lower():
            suggestions = [
                "Add account number generation for unique identification",
                "Implement interest calculation method for savings accounts",
                "Add transaction timestamps to history entries",
                "Consider adding account type (checking, savings, etc.)",
                "Implement overdraft protection with fees"
            ]
        else:
            suggestions = [
                f"Add specific error handling for the operations in your {language} code",
                "Include input validation for user-provided data",
                "Add logging to track function execution flow",
                "Consider breaking complex functions into smaller, focused methods",
                "Add comprehensive unit tests for each function"
            ]

        examples = [
            f"# Example of improved {language} code with better structure",
            f"# Example of error handling in {language}",
            f"# Example of documentation best practices"
        ]

    elif analysis_type == "improvement":
        analysis = f"""Code Improvement Analysis for {language}:

**Performance Optimizations:**
- The current implementation can be optimized for better performance
- Consider using more efficient algorithms or data structures
- Memory usage could be reduced with better variable management

**Code Quality:**
- Add comprehensive error handling
- Improve variable naming for better readability
- Consider breaking down complex functions
- Add proper documentation and comments

**{language.title()} Best Practices:**
- Follow {language} style guidelines
- Use appropriate design patterns
- Implement proper testing strategies
- Consider maintainability and scalability"""

        suggestions = [
            "Optimize algorithm complexity from O(n²) to O(n log n)",
            "Use more descriptive variable names",
            "Add input validation and error handling",
            "Implement proper logging for debugging",
            "Consider using design patterns for better structure"
        ]

        examples = [
            f"# Optimized version with better algorithm",
            f"# Refactored code with improved structure",
            f"# Example with proper error handling"
        ]

    elif analysis_type == "bug_detection":
        analysis = f"""Bug Detection Analysis for {language}:

**Potential Issues Found:**
1. **Index Out of Bounds**: Possible array/list access beyond bounds
2. **Null/Undefined References**: Variables might be used before initialization
3. **Type Mismatches**: Potential type conversion issues
4. **Logic Errors**: Conditional statements might not cover all cases
5. **Resource Leaks**: Files or connections might not be properly closed

**Security Considerations:**
- Input validation missing
- Potential injection vulnerabilities
- Unsafe operations detected

**Runtime Errors:**
- Division by zero possibilities
- Infinite loop conditions
- Memory allocation issues"""

        suggestions = [
            "Add bounds checking for array/list access",
            "Initialize all variables before use",
            "Add try-catch blocks for error handling",
            "Validate all user inputs",
            "Use safe string operations to prevent injection"
        ]

        examples = [
            f"# Fixed version with proper bounds checking",
            f"# Example with comprehensive error handling",
            f"# Secure implementation with input validation"
        ]

    else:  # learning
        analysis = f"""Learning Guide for {language}:

**Educational Value:**
This code is excellent for learning {language} because it demonstrates:

1. **Core Concepts**: Basic syntax and structure
2. **Problem Solving**: How to break down problems into code
3. **Language Features**: Specific {language} capabilities
4. **Programming Patterns**: Common approaches in {language}

**Learning Path:**
- Start with understanding the basic syntax
- Practice with similar examples
- Experiment with modifications
- Build upon these concepts

**Next Steps:**
- Try implementing variations of this code
- Explore more advanced {language} features
- Practice with different problem types
- Join {language} communities for support"""

        suggestions = [
            f"Practice more {language} syntax with similar examples",
            "Try modifying the code to see how it behaves",
            "Read the official {language} documentation",
            "Join online {language} learning communities",
            "Work on small projects to apply these concepts"
        ]

        examples = [
            f"# Beginner-friendly {language} exercise",
            f"# Intermediate challenge building on this concept",
            f"# Advanced project idea using these principles"
        ]

    return {
        "analysis": analysis,
        "suggestions": suggestions,
        "examples": examples,
        "execution_result": f"Demo mode - Code execution simulated for {language}" if language == "python" else None,
        "error": None
    }


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "supported_languages": SUPPORTED_LANGUAGES,
        "analysis_types": ANALYSIS_TYPES
    })


@app.post("/analyze")
async def analyze_code(
    request: Request,
    code: str = Form(...),
    language: str = Form(...),
    analysis_type: str = Form(...),
    user_level: str = Form(default="beginner"),
    specific_question: str = Form(default="")
):
    """Analyze code and return mock results for demo."""
    try:
        # Validate inputs
        if not code.strip():
            raise HTTPException(status_code=400, detail="Code cannot be empty")

        if language not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")

        if analysis_type not in ANALYSIS_TYPES:
            raise HTTPException(status_code=400, detail=f"Invalid analysis type: {analysis_type}")

        # Generate mock analysis
        result = generate_mock_analysis(code, language, analysis_type, user_level)

        # Return HTML response
        return templates.TemplateResponse("index.html", {
            "request": request,
            "result": type('MockResult', (), result)(),  # Convert dict to object
            "code": code,
            "language": language,
            "analysis_type": analysis_type,
            "user_level": user_level,
            "specific_question": specific_question,
            "supported_languages": SUPPORTED_LANGUAGES,
            "analysis_types": ANALYSIS_TYPES,
            "demo_mode": True
        })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "mode": "demo",
        "analyzer_ready": True,
        "model_loaded": False,
        "note": "Running in demo mode - mock analysis results"
    }


def main():
    """Main entry point for demo."""
    parser = argparse.ArgumentParser(description="Interactive Code Helper - Demo")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind the server to"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind the server to"
    )

    args = parser.parse_args()

    print("🚀 Starting Interactive Code Helper - Demo Mode")
    print("=" * 50)
    print(f"🌐 Server: http://{args.host}:{args.port}")
    print("📝 Mode: Demo (mock AI responses)")
    print("💡 This shows the interface without requiring the full gpt-oss model")
    print("")

    # Run the server
    uvicorn.run(
        "demo_app:app",
        host=args.host,
        port=args.port,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()

# Interactive Code Helper

An AI-powered code learning assistant built with OpenAI's gpt-oss-20b model, designed to help beginners learn programming through code explanation, improvement suggestions, and interactive guidance.

## Features

- **Code Explanation**: Get detailed, line-by-line explanations of your code
- **Improvement Suggestions**: Receive specific recommendations for better coding practices
- **Bug Detection**: Identify potential issues and get suggested fixes
- **Multi-language Support**: Works with Python, JavaScript, Java, C++, and more
- **Interactive Learning**: Beginner-friendly explanations with examples
- **Code Execution**: Test and validate code suggestions in real-time

## Hardware Requirements

- **Recommended**: MacBook Pro with Apple Silicon (M1/M2/M3)
- **Memory**: At least 16GB RAM (8GB minimum, but may require closing other applications)
- **Storage**: ~10GB for model weights and dependencies

## Quick Start

### 1. Install Dependencies

```bash
# Install with Metal backend for Apple Silicon (from the gpt-oss root directory)
GPTOSS_BUILD_METAL=1 pip install -e ".[metal]"

# Install additional dependencies for the code helper
pip install fastapi uvicorn jinja2 python-multipart
```

### 2. Download the Model

```bash
# Download gpt-oss-20b model weights
hf download openai/gpt-oss-20b --include "metal/*" --local-dir gpt-oss-20b/metal/
```

### 3. Run the Application

```bash
# Start the local server
cd code_helper
python app.py --model-path ../gpt-oss-20b/metal/model.bin
```

### 4. Open in Browser

Navigate to `http://localhost:8000` to start using the Interactive Code Helper.

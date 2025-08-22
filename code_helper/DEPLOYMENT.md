# Deployment Guide

This guide covers both local deployment and Vercel deployment options for the Interactive Code Helper.

## Local Deployment (Recommended)

The Interactive Code Helper is designed to run locally with the gpt-oss-20b model using the Metal backend on Apple Silicon.

### Prerequisites

- **Hardware**: MacBook Pro/Air with Apple Silicon (M1/M2/M3)
- **Memory**: 16GB+ RAM recommended (8GB minimum)
- **Storage**: ~15GB free disk space
- **OS**: macOS 12.0+ (Monterey or later)
- **Software**: Python 3.12+, Xcode CLI tools

### Quick Setup

1. **Clone and navigate to the project**:

   ```bash
   git clone https://github.com/openai/gpt-oss.git
   cd gpt-oss
   git checkout interactive-code-helper
   cd code_helper
   ```

2. **Run the automated setup**:

   ```bash
   ./setup.sh
   ```

3. **Download the model** (if not done automatically):

   ```bash
   pip install huggingface-hub
   hf download openai/gpt-oss-20b --include "metal/*" --local-dir ../gpt-oss-20b/metal/
   ```

4. **Start the application**:

   ```bash
   ./run.sh
   ```

5. **Open your browser** to `http://localhost:8000`

### Manual Setup

If the automated setup doesn't work, follow these manual steps:

1. **Install dependencies**:

   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install gpt-oss with Metal backend
   cd ..
   GPTOSS_BUILD_METAL=1 pip install -e ".[metal]"
   cd code_helper

   # Install additional dependencies
   pip install -r requirements.txt
   ```

2. **Download the model**:

   ```bash
   hf download openai/gpt-oss-20b --include "metal/*" --local-dir ../gpt-oss-20b/metal/
   ```

3. **Run the application**:
   ```bash
   python app.py --model-path ../gpt-oss-20b/metal/model.bin
   ```

### Configuration Options

The application supports several command-line options:

```bash
python app.py --help
```

Common options:

- `--model-path`: Path to the model file (default: `../gpt-oss-20b/metal/model.bin`)
- `--host`: Host to bind to (default: `127.0.0.1`)
- `--port`: Port to bind to (default: `8000`)
- `--reload`: Enable auto-reload for development

### Performance Tuning

For optimal performance:

1. **Close unnecessary applications** to free up RAM
2. **Use Activity Monitor** to monitor memory usage
3. **Ensure good ventilation** to prevent thermal throttling
4. **Keep the application running** to avoid model reload times

## Vercel Deployment (Demo Only)

⚠️ **Important**: Vercel deployment provides only a demo version since the gpt-oss-20b model cannot run in serverless environments.

### What the Vercel deployment includes:

- **Demo landing page** with setup instructions
- **Static file serving** for CSS/JS assets
- **Health check endpoint**
- **Instructions for local deployment**

### Deploy to Vercel

1. **Install Vercel CLI**:

   ```bash
   npm install -g vercel
   ```

2. **Deploy from the code_helper directory**:

   ```bash
   cd code_helper
   vercel
   ```

3. **Follow the prompts** to configure your deployment

### Vercel Configuration

The `vercel.json` file configures:

- **Serverless functions** for API endpoints
- **Static file serving** for assets
- **Routing** for different paths
- **Environment variables** and function settings

### Limitations of Vercel Deployment

- **No AI analysis**: Cannot run the gpt-oss-20b model
- **Demo only**: Shows setup instructions and features
- **No code execution**: Python tool not available
- **Static content**: No real-time AI interactions

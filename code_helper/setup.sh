#!/bin/bash

# Interactive Code Helper - Setup Script for macOS
# This script sets up the Interactive Code Helper on macOS with Apple Silicon

set -e  # Exit on any error

echo "🚀 Interactive Code Helper Setup"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This setup script is designed for macOS. Please follow manual installation instructions."
    exit 1
fi

# Check if running on Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    print_warning "This script is optimized for Apple Silicon (M1/M2/M3). Intel Macs may work but are not officially supported."
fi

# Check Python version
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not installed. Please install Python 3.12 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.12"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 12) else 1)" 2>/dev/null; then
    print_error "Python 3.12 or later is required. Found: $PYTHON_VERSION"
    exit 1
fi

print_success "Python $PYTHON_VERSION found"

# Check available memory
print_status "Checking system memory..."
MEMORY_GB=$(sysctl -n hw.memsize | awk '{print int($1/1024/1024/1024)}')
if [ $MEMORY_GB -lt 8 ]; then
    print_error "At least 8GB of RAM is required. Found: ${MEMORY_GB}GB"
    exit 1
elif [ $MEMORY_GB -lt 16 ]; then
    print_warning "16GB+ RAM is recommended for optimal performance. Found: ${MEMORY_GB}GB"
    print_warning "You may need to close other applications when running the model."
else
    print_success "Memory check passed: ${MEMORY_GB}GB available"
fi

# Check disk space
print_status "Checking disk space..."
AVAILABLE_GB=$(df -g . | tail -1 | awk '{print $4}')
if [ $AVAILABLE_GB -lt 15 ]; then
    print_error "At least 15GB of free disk space is required. Available: ${AVAILABLE_GB}GB"
    exit 1
fi
print_success "Disk space check passed: ${AVAILABLE_GB}GB available"

# Check if we're in the right directory
if [ ! -f "app.py" ] || [ ! -f "code_analyzer.py" ]; then
    print_error "Please run this script from the code_helper directory"
    exit 1
fi

# Install Xcode CLI tools if needed
print_status "Checking Xcode CLI tools..."
if ! xcode-select -p &> /dev/null; then
    print_status "Installing Xcode CLI tools..."
    xcode-select --install
    print_warning "Please complete the Xcode CLI tools installation and run this script again."
    exit 1
fi
print_success "Xcode CLI tools are installed"

# Create virtual environment
print_status "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install gpt-oss with Metal backend
print_status "Installing gpt-oss with Metal backend..."
print_warning "This may take several minutes..."

# Go to parent directory to install gpt-oss
cd ..
GPTOSS_BUILD_METAL=1 pip install -e ".[metal]"
cd code_helper

print_success "gpt-oss with Metal backend installed"

# Install additional dependencies
print_status "Installing additional dependencies..."
pip install -r requirements.txt

print_success "All dependencies installed"

# Check if model exists
MODEL_PATH="../gpt-oss-20b/metal/model.bin"
if [ ! -f "$MODEL_PATH" ]; then
    print_warning "Model file not found at $MODEL_PATH"
    print_status "To download the model, run:"
    echo "  hf download openai/gpt-oss-20b --include \"metal/*\" --local-dir ../gpt-oss-20b/metal/"
    echo ""
    print_status "Make sure you have huggingface-hub installed:"
    echo "  pip install huggingface-hub"
    echo ""
else
    print_success "Model file found at $MODEL_PATH"
fi

# Create run script
print_status "Creating run script..."
cat > run.sh << 'EOF'
#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Set model path
MODEL_PATH="../gpt-oss-20b/metal/model.bin"

# Check if model exists
if [ ! -f "$MODEL_PATH" ]; then
    echo "❌ Model file not found at $MODEL_PATH"
    echo "Please download the model first:"
    echo "  hf download openai/gpt-oss-20b --include \"metal/*\" --local-dir ../gpt-oss-20b/metal/"
    exit 1
fi

echo "🚀 Starting Interactive Code Helper..."
echo "📍 Model: $MODEL_PATH"
echo "🌐 Server will be available at: http://localhost:8000"
echo ""

# Run the application
python app.py --model-path "$MODEL_PATH" --host 127.0.0.1 --port 8000
EOF

chmod +x run.sh
print_success "Run script created: ./run.sh"

echo ""
print_success "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Download the model (if not already done):"
echo "   hf download openai/gpt-oss-20b --include \"metal/*\" --local-dir ../gpt-oss-20b/metal/"
echo ""
echo "2. Start the application:"
echo "   ./run.sh"
echo ""
echo "3. Open your browser to:"
echo "   http://localhost:8000"
echo ""
print_warning "Note: The first run may take a few minutes to load the model into memory."

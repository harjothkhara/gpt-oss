# Troubleshooting Guide

This guide helps resolve common issues when setting up and running the Interactive Code Helper.

## Common Issues

### 1. Model Loading Issues

#### Problem: "Model file not found"

```
❌ Model file not found at ../gpt-oss-20b/metal/model.bin
```

**Solution:**

1. Download the model using Hugging Face CLI:

   ```bash
   pip install huggingface-hub
   hf download openai/gpt-oss-20b --include "metal/*" --local-dir ../gpt-oss-20b/metal/
   ```

2. Verify the model file exists:
   ```bash
   ls -la ../gpt-oss-20b/metal/model.bin
   ```

#### Problem: "Failed to load model"

```
ERROR: Failed to load model: [error details]
```

**Solutions:**

1. **Memory Issue**: Close other applications to free up RAM
2. **Corrupted Download**: Re-download the model
3. **Permissions**: Check file permissions:
   ```bash
   chmod 644 ../gpt-oss-20b/metal/model.bin
   ```

### 2. Installation Issues

#### Problem: "GPTOSS_BUILD_METAL=1 pip install failed"

```
ERROR: Failed building wheel for gpt-oss
```

**Solutions:**

1. **Install Xcode CLI tools**:

   ```bash
   xcode-select --install
   ```

2. **Update pip and setuptools**:

   ```bash
   pip install --upgrade pip setuptools wheel
   ```

3. **Check Python version**:
   ```bash
   python3 --version  # Should be 3.12+
   ```

#### Problem: "No module named 'gpt_oss'"

```
ModuleNotFoundError: No module named 'gpt_oss'
```

**Solution:**
Make sure you're in the virtual environment:

```bash
source venv/bin/activate
```

### 3. Memory Issues

#### Problem: "Out of Memory" or system freezing

```
torch.cuda.OutOfMemoryError: CUDA out of memory
```

**Solutions:**

1. **Close other applications** to free up RAM
2. **Restart your Mac** to clear memory
3. **Check available memory**:
   ```bash
   vm_stat | grep "Pages free"
   ```

#### Problem: Slow performance

**Solutions:**

1. **Ensure sufficient RAM** (16GB+ recommended)
2. **Close browser tabs** and other memory-intensive apps
3. **Use Activity Monitor** to check memory usage

### 4. Network Issues

#### Problem: "Failed to download model"

```
HTTPError: 403 Client Error: Forbidden
```

**Solutions:**

1. **Login to Hugging Face**:

   ```bash
   huggingface-cli login
   ```

2. **Check internet connection**
3. **Use alternative download method**:
   ```bash
   git lfs clone https://huggingface.co/openai/gpt-oss-20b
   ```

### 5. Port Issues

#### Problem: "Port 8000 already in use"

```
OSError: [Errno 48] Address already in use
```

**Solutions:**

1. **Find and kill the process**:

   ```bash
   lsof -ti:8000 | xargs kill -9
   ```

2. **Use a different port**:
   ```bash
   python app.py --port 8001
   ```

### 6. Browser Issues

#### Problem: "This site can't be reached"

**Solutions:**

1. **Check if server is running**:

   ```bash
   curl http://localhost:8000/health
   ```

2. **Try different browser** or **incognito mode**
3. **Clear browser cache**

#### Problem: "Analysis takes too long"

**Solutions:**

1. **Check server logs** for errors
2. **Reduce code complexity** for testing
3. **Restart the application**

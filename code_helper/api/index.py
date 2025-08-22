"""
Vercel serverless function for the main page.
Since we can't run the Metal backend on Vercel, this serves a demo version.
"""

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve the main page with a notice about local deployment
        # Serve the full Interactive Code Helper interface
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Code Helper - Learn Programming with AI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet">
    <style>
        body { background-color: #f5f5f5; }
        .hero-section {
            background: linear-gradient(135deg, #007bff, #17a2b8);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
        }
        .card { border: none; border-radius: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
        .code-input { font-family: 'Courier New', monospace; }
        .fade-in { animation: fadeIn 0.5s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .demo-notice { background: linear-gradient(45deg, #ffc107, #fd7e14); color: white; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-code"></i>
                Interactive Code Helper
            </a>
        </div>
    </nav>

    <main class="container mt-4">
        <div class="row">
            <div class="col-lg-12">
                <div class="hero-section text-center mb-5">
                    <h1 class="display-4 text-primary">Interactive Code Helper</h1>
                    <p class="lead">
                        Learn programming with AI-powered code analysis, explanations, and improvements.
                        Powered by <strong>gpt-oss-20b</strong> running locally on your machine.
                    </p>
                </div>
            </div>
        </div>

        <div class="alert alert-warning demo-notice" role="alert">
            <i class="fas fa-info-circle me-2"></i>
            <strong>Demo Mode:</strong> This is a demo version running on Vercel. Responses are simulated. For full AI-powered analysis with gpt-oss-20b, please run the application locally.
        </div>

        <div class="row">
            <!-- Input Section -->
            <div class="col-lg-6">
                <div class="card shadow-sm">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0"><i class="fas fa-edit"></i> Code Input</h5>
                    </div>
                    <div class="card-body">
                        <form id="codeForm" method="post" action="/api/analyze">
                            <div class="mb-3">
                                <label for="language" class="form-label">Programming Language</label>
                                <select class="form-select" id="language" name="language" required>
                                    <option value="">Select a language...</option>
                                    <option value="python">Python</option>
                                    <option value="javascript">JavaScript</option>
                                    <option value="java">Java</option>
                                    <option value="cpp">C++</option>
                                    <option value="c">C</option>
                                    <option value="csharp">C#</option>
                                    <option value="go">Go</option>
                                    <option value="rust">Rust</option>
                                    <option value="php">PHP</option>
                                    <option value="ruby">Ruby</option>
                                </select>
                            </div>

                            <div class="mb-3">
                                <label for="analysis_type" class="form-label">Analysis Type</label>
                                <select class="form-select" id="analysis_type" name="analysis_type" required>
                                    <option value="">Select analysis type...</option>
                                    <option value="explanation">Explanation</option>
                                    <option value="improvement">Improvement</option>
                                    <option value="bug_detection">Bug Detection</option>
                                    <option value="learning">Learning</option>
                                </select>
                            </div>

                            <div class="mb-3">
                                <label for="user_level" class="form-label">Your Programming Level</label>
                                <select class="form-select" id="user_level" name="user_level" required>
                                    <option value="">Select your level...</option>
                                    <option value="beginner">Beginner</option>
                                    <option value="intermediate">Intermediate</option>
                                    <option value="advanced">Advanced</option>
                                </select>
                            </div>

                            <div class="mb-3">
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <label for="code" class="form-label mb-0">Your Code</label>
                                    <button type="button" class="btn btn-outline-secondary btn-sm" id="clearCodeBtn">
                                        <i class="fas fa-trash-alt me-1"></i>Clear
                                    </button>
                                </div>
                                <textarea
                                    class="form-control code-input"
                                    id="code"
                                    name="code"
                                    rows="12"
                                    placeholder="Paste your code here..."
                                    required
                                ></textarea>
                            </div>

                            <div class="mb-3">
                                <label for="specific_question" class="form-label">Specific Question (Optional)</label>
                                <input
                                    type="text"
                                    class="form-control"
                                    id="specific_question"
                                    name="specific_question"
                                    placeholder="Ask a specific question about your code..."
                                >
                            </div>

                            <div class="d-grid">
                                <button type="submit" class="btn btn-success btn-lg" id="analyzeBtn">
                                    <i class="fas fa-magic"></i> Analyze Code
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Code Examples Section -->
            <div class="col-lg-6">
                <div class="card shadow-sm">
                    <div class="card-header bg-info text-white">
                        <h5 class="mb-0"><i class="fas fa-lightbulb"></i> Quick Start Examples</h5>
                    </div>
                    <div class="card-body">
                        <p class="text-muted">Click on any example to load it into the code editor:</p>

                        <div class="mb-3">
                            <button class="btn btn-outline-primary btn-sm w-100 text-start code-example"
                                    data-language="python"
                                    data-code="def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test the function
for i in range(10):
    print(f'F({i}) = {fibonacci(i)}')">
                                <i class="fab fa-python me-2"></i>Python Fibonacci
                            </button>
                        </div>

                        <div class="mb-3">
                            <button class="btn btn-outline-warning btn-sm w-100 text-start code-example"
                                    data-language="javascript"
                                    data-code="function bubbleSort(arr) {
    let n = arr.length;
    for (let i = 0; i < n - 1; i++) {
        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
            }
        }
    }
    return arr;
}

console.log(bubbleSort([64, 34, 25, 12, 22, 11, 90]));">
                                <i class="fab fa-js-square me-2"></i>JavaScript Bubble Sort
                            </button>
                        </div>

                        <div class="mb-3">
                            <button class="btn btn-outline-danger btn-sm w-100 text-start code-example"
                                    data-language="java"
                                    data-code="public class BinarySearch {
    public static int binarySearch(int[] arr, int target) {
        int left = 0, right = arr.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (arr[mid] == target) return mid;
            if (arr[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }
}">
                                <i class="fab fa-java me-2"></i>Java Binary Search
                            </button>
                        </div>

                        <div class="mb-3">
                            <button class="btn btn-outline-success btn-sm w-100 text-start code-example"
                                    data-language="cpp"
                                    data-code="#include <iostream>
#include <vector>
using namespace std;

class Stack {
private:
    vector<int> data;
public:
    void push(int x) { data.push_back(x); }
    void pop() { if (!empty()) data.pop_back(); }
    int top() { return empty() ? -1 : data.back(); }
    bool empty() { return data.empty(); }
};

int main() {
    Stack s;
    s.push(1); s.push(2); s.push(3);
    cout << s.top() << endl;
    return 0;
}">
                                <i class="fas fa-code me-2"></i>C++ Stack Implementation
                            </button>
                        </div>
                    </div>
                </div>

                <!-- How to Use Section -->
                <div class="card shadow-sm mt-4">
                    <div class="card-header bg-secondary text-white">
                        <h5 class="mb-0"><i class="fas fa-question-circle"></i> How to Use</h5>
                    </div>
                    <div class="card-body">
                        <ol>
                            <li><strong>Select a programming language</strong> from the dropdown</li>
                            <li><strong>Choose an analysis type:</strong>
                                <ul class="mt-2">
                                    <li><strong>Explanation:</strong> Get detailed explanations of how your code works</li>
                                    <li><strong>Improvement:</strong> Receive suggestions to make your code better</li>
                                    <li><strong>Bug Detection:</strong> Find and fix potential issues</li>
                                    <li><strong>Learning:</strong> Interactive tutorials and exercises</li>
                                </ul>
                            </li>
                            <li><strong>Set your programming level</strong> for appropriate explanations</li>
                            <li><strong>Paste your code</strong> in the text area</li>
                            <li><strong>Ask a specific question</strong> (optional)</li>
                            <li><strong>Click "Analyze Code"</strong> and wait for AI-powered insights!</li>
                        </ol>

                        <div class="alert alert-info mt-3">
                            <strong>💡 Tip:</strong> Try the example codes above to see how the analysis works!
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Loading Modal -->
    <div class="modal fade" id="loadingModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-body text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-3">Analyzing your code with gpt-oss-20b...</p>
                    <small class="text-muted">This may take a few moments</small>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-light mt-5 py-4">
        <div class="container text-center">
            <p class="mb-0">
                Powered by <strong>gpt-oss-20b</strong> with Metal backend
                <br>
                <small class="text-muted">An AI-powered code learning assistant</small>
            </p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
    <script src="/static/script.js"></script>
</body>
</html>"""

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
        return

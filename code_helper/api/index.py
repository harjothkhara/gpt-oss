"""
Vercel serverless function for the main page.
Since we can't run the Metal backend on Vercel, this serves a demo version.
"""

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve the main page with a notice about local deployment
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Code Helper - Demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f5f5f5; }
        .hero-section {
            background: linear-gradient(135deg, #007bff, #17a2b8);
            color: white;
            padding: 3rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
        }
        .card { border: none; border-radius: 15px; }
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
                <div class="hero-section text-center">
                    <h1 class="display-4">Interactive Code Helper</h1>
                    <p class="lead">
                        AI-powered code learning assistant using gpt-oss-20b
                    </p>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-lg-8 mx-auto">
                <div class="card shadow-sm">
                    <div class="card-header bg-warning text-dark">
                        <h5 class="mb-0">⚠️ Demo Version</h5>
                    </div>
                    <div class="card-body">
                        <p><strong>This is a demo deployment on Vercel.</strong></p>
                        <p>The full Interactive Code Helper requires local deployment with the gpt-oss-20b model running on Apple Silicon hardware.</p>

                        <h6 class="mt-4">To run the full version locally:</h6>
                        <ol>
                            <li>Clone the repository:
                                <pre class="bg-light p-2 mt-2"><code>git clone https://github.com/openai/gpt-oss.git
cd gpt-oss
git checkout interactive-code-helper</code></pre>
                            </li>
                            <li>Run the setup script:
                                <pre class="bg-light p-2 mt-2"><code>cd code_helper
./setup.sh</code></pre>
                            </li>
                            <li>Download the model:
                                <pre class="bg-light p-2 mt-2"><code>hf download openai/gpt-oss-20b --include "metal/*" --local-dir ../gpt-oss-20b/metal/</code></pre>
                            </li>
                            <li>Start the application:
                                <pre class="bg-light p-2 mt-2"><code>./run.sh</code></pre>
                            </li>
                        </ol>

                        <div class="alert alert-info mt-4">
                            <strong>Requirements:</strong>
                            <ul class="mb-0">
                                <li>macOS with Apple Silicon (M1/M2/M3)</li>
                                <li>16GB+ RAM recommended (8GB minimum)</li>
                                <li>~15GB free disk space</li>
                                <li>Python 3.12+</li>
                            </ul>
                        </div>

                        <h6 class="mt-4">Features of the full version:</h6>
                        <ul>
                            <li><strong>Code Explanation:</strong> Detailed explanations of how code works</li>
                            <li><strong>Improvement Suggestions:</strong> Recommendations for better coding practices</li>
                            <li><strong>Bug Detection:</strong> Identify and fix potential issues</li>
                            <li><strong>Interactive Learning:</strong> Beginner-friendly tutorials</li>
                            <li><strong>Multi-language Support:</strong> Python, JavaScript, Java, C++, and more</li>
                            <li><strong>Code Execution:</strong> Test Python code in real-time</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </main>

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
</body>
</html>
        """

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
        return

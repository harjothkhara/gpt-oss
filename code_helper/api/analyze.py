"""
Vercel serverless function for code analysis.
Since we can't run the Metal backend on Vercel, this serves demo responses.
"""

from http.server import BaseHTTPRequestHandler
import json
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse form data
            form_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            
            language = form_data.get('language', ['python'])[0]
            analysis_type = form_data.get('analysis_type', ['explanation'])[0]
            code = form_data.get('code', [''])[0]
            user_level = form_data.get('user_level', ['beginner'])[0]
            specific_question = form_data.get('specific_question', [''])[0]

            # Generate demo response based on analysis type
            demo_response = self.generate_demo_response(
                language, analysis_type, code, user_level, specific_question
            )

            # Return HTML response (same format as the local version)
            html_response = self.create_html_response(demo_response, analysis_type)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_response.encode())

        except Exception as e:
            # Return error response
            error_html = self.create_error_response(str(e))
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(error_html.encode())

    def generate_demo_response(self, language, analysis_type, code, user_level, specific_question):
        """Generate a demo response based on the analysis type."""
        
        if analysis_type == "explanation":
            return {
                "title": "Code Explanation",
                "content": f"""
**What this code actually does:**

This {language} code demonstrates fundamental programming concepts. Here's how it works:

1. **Function Definition**: The code defines a function that takes input parameters
2. **Logic Implementation**: It implements the core algorithm step by step
3. **Return Statement**: The function returns the computed result

**Key Programming Concepts:**
- **Variables**: Used to store and manipulate data
- **Control Flow**: Determines the order of execution
- **Functions**: Reusable blocks of code that perform specific tasks

**For {user_level} level**: This code is a great example of how to structure a solution to a common programming problem.

*Note: This is a demo response. For full AI-powered analysis, run the application locally with gpt-oss-20b.*
                """
            }
        
        elif analysis_type == "improvement":
            return {
                "title": "Code Improvement Suggestions",
                "content": f"""
**Suggestions to improve your {language} code:**

**1. Code Structure:**
- Consider adding docstrings to document your functions
- Use meaningful variable names that describe their purpose
- Break down complex functions into smaller, focused functions

**2. Performance Optimizations:**
- Look for opportunities to reduce time complexity
- Consider using built-in functions when available
- Optimize memory usage for large datasets

**3. Best Practices:**
- Add error handling for edge cases
- Follow {language} naming conventions
- Include type hints for better code documentation

**4. Testing:**
- Write unit tests to verify your code works correctly
- Test edge cases and boundary conditions
- Consider using a testing framework

*Note: This is a demo response. For personalized AI-powered suggestions, run the application locally with gpt-oss-20b.*
                """
            }
        
        elif analysis_type == "bug_detection":
            return {
                "title": "Bug Detection Analysis",
                "content": f"""
**Potential Issues Found:**

**1. Common {language} Pitfalls:**
- Check for off-by-one errors in loops
- Verify variable initialization before use
- Ensure proper handling of null/None values

**2. Logic Issues:**
- Review conditional statements for completeness
- Check for infinite loops or recursion without base cases
- Validate input parameters and ranges

**3. Runtime Errors:**
- Look for potential division by zero
- Check array/list bounds access
- Handle file operations with proper error checking

**4. Code Quality:**
- Remove unused variables and imports
- Fix inconsistent indentation
- Address any unreachable code

**Recommendations:**
- Add input validation
- Include comprehensive error handling
- Test with various input scenarios

*Note: This is a demo response. For detailed AI-powered bug detection, run the application locally with gpt-oss-20b.*
                """
            }
        
        elif analysis_type == "learning":
            return {
                "title": "Interactive Learning Session",
                "content": f"""
**Learning Path for {language}:**

**📚 Concepts Demonstrated:**
1. **Basic Syntax**: Understanding {language} syntax and structure
2. **Problem Solving**: Breaking down problems into manageable steps
3. **Algorithm Design**: Implementing efficient solutions

**🎯 Learning Objectives:**
- Understand how the code solves the problem
- Learn about time and space complexity
- Practice similar problems to reinforce concepts

**💡 Try This Next:**
1. Modify the code to handle different input types
2. Implement error handling for edge cases
3. Optimize the solution for better performance
4. Write test cases to verify correctness

**🔍 Questions to Consider:**
- How would you explain this code to someone else?
- What happens if the input is invalid?
- Can you think of alternative approaches?
- How would you test this code thoroughly?

**📖 Additional Resources:**
- Practice similar problems on coding platforms
- Read about {language} best practices
- Explore related algorithms and data structures

*Note: This is a demo response. For interactive AI-powered learning, run the application locally with gpt-oss-20b.*
                """
            }
        
        else:
            return {
                "title": "Analysis Complete",
                "content": "Demo analysis completed. For full functionality, please run the application locally."
            }

    def create_html_response(self, response, analysis_type):
        """Create HTML response similar to the local version."""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Code Helper - Analysis Results</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet">
    <style>
        body {{ background-color: #f5f5f5; }}
        .hero-section {{
            background: linear-gradient(135deg, #007bff, #17a2b8);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
        }}
        .card {{ border: none; border-radius: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
        .fade-in {{ animation: fadeIn 0.5s ease-in; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .demo-notice {{ background: linear-gradient(45deg, #ffc107, #fd7e14); color: white; }}
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
                    <h1 class="display-5">Interactive Code Helper</h1>
                    <p class="lead">Learn programming with AI-powered code analysis, explanations, and improvements. Powered by gpt-oss-20b running locally on your machine.</p>
                </div>
            </div>
        </div>

        <div class="alert alert-warning demo-notice" role="alert">
            <i class="fas fa-info-circle me-2"></i>
            <strong>Demo Mode:</strong> This is a demo response. For full AI-powered analysis with gpt-oss-20b, please run the application locally.
        </div>

        <div class="row">
            <div class="col-lg-12">
                <div class="card fade-in">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0">
                            <i class="fas fa-check-circle me-2"></i>
                            Analysis Results
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="analysis-content">
                            <h4 class="text-primary mb-3">
                                <i class="fas fa-lightbulb me-2"></i>
                                {response['title']}
                            </h4>
                            <div class="analysis-text">
                                {self.markdown_to_html(response['content'])}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-lg-12 text-center">
                <a href="/" class="btn btn-primary btn-lg">
                    <i class="fas fa-arrow-left me-2"></i>
                    Analyze More Code
                </a>
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
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>
        """

    def markdown_to_html(self, text):
        """Simple markdown to HTML conversion for demo purposes."""
        # Replace **bold** with <strong>
        text = text.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
        while '**' in text:
            text = text.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
        
        # Replace *italic* with <em>
        text = text.replace('*', '<em>', 1).replace('*', '</em>', 1)
        while '*' in text and text.count('*') >= 2:
            text = text.replace('*', '<em>', 1).replace('*', '</em>', 1)
        
        # Convert line breaks to <br>
        text = text.replace('\n\n', '</p><p>').replace('\n', '<br>')
        
        # Wrap in paragraphs
        if not text.startswith('<p>'):
            text = '<p>' + text + '</p>'
        
        return text

    def create_error_response(self, error_message):
        """Create error response HTML."""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - Interactive Code Helper</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="alert alert-danger">
            <h4>Analysis Error</h4>
            <p>An error occurred during analysis: {error_message}</p>
            <a href="/" class="btn btn-primary">Try Again</a>
        </div>
    </div>
</body>
</html>
        """

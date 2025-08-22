// Interactive Code Helper - JavaScript

// Example code snippets
const codeExamples = {
    python: {
        fibonacci: `def fibonacci(n):
    """Calculate the nth Fibonacci number using recursion."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test the function
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")`,

        class: `class BankAccount:
    """A simple bank account class."""

    def __init__(self, account_holder, initial_balance=0):
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited ${amount}")
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount}")
            return True
        return False

    def get_balance(self):
        return self.balance

# Example usage
account = BankAccount("John Doe", 1000)
account.deposit(500)
account.withdraw(200)
print(f"Balance: ${account.get_balance()}")`
    },

    javascript: {
        sorting: `// Bubble sort implementation with optimization
function bubbleSort(arr) {
    const n = arr.length;
    let swapped;

    for (let i = 0; i < n - 1; i++) {
        swapped = false;

        // Last i elements are already sorted
        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                // Swap elements
                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
                swapped = true;
            }
        }

        // If no swapping occurred, array is sorted
        if (!swapped) break;
    }

    return arr;
}

// Test the function
const numbers = [64, 34, 25, 12, 22, 11, 90];
console.log("Original array:", numbers);
console.log("Sorted array:", bubbleSort([...numbers]));`
    }
};

// DOM elements
let codeForm, codeTextarea, languageSelect, analysisTypeSelect, analyzeBtn, loadingModal;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeElements();
    setupEventListeners();
    setupFormValidation();
});

function initializeElements() {
    codeForm = document.getElementById('codeForm');
    codeTextarea = document.getElementById('code');
    languageSelect = document.getElementById('language');
    analysisTypeSelect = document.getElementById('analysis_type');
    analyzeBtn = document.getElementById('analyzeBtn');
    loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
}

function setupEventListeners() {
    // Form submission
    if (codeForm) {
        codeForm.addEventListener('submit', handleFormSubmit);
    }

    // Language change
    if (languageSelect) {
        languageSelect.addEventListener('change', updatePlaceholder);
    }

    // Analysis type change
    if (analysisTypeSelect) {
        analysisTypeSelect.addEventListener('change', updateAnalysisDescription);
    }

    // Code textarea enhancements
    if (codeTextarea) {
        codeTextarea.addEventListener('keydown', handleCodeInput);
        codeTextarea.addEventListener('input', validateCode);
    }
}

function setupFormValidation() {
    // Real-time validation
    const form = document.getElementById('codeForm');
    if (form) {
        form.addEventListener('input', validateForm);
    }
}

function handleFormSubmit(event) {
    event.preventDefault();

    if (!validateForm()) {
        return;
    }

    // Show loading modal
    showLoading();

    // Submit form
    const formData = new FormData(codeForm);

    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
    })
    .then(html => {
        // Replace the page content with the response
        document.documentElement.innerHTML = html;

        // Reinitialize after content replacement
        setTimeout(() => {
            initializeElements();
            setupEventListeners();
            setupFormValidation();

            // Trigger syntax highlighting
            if (typeof Prism !== 'undefined') {
                Prism.highlightAll();
            }

            // Add fade-in animation to results
            const resultCard = document.querySelector('.card .bg-success');
            if (resultCard) {
                resultCard.closest('.card').classList.add('fade-in');
            }
        }, 100);
    })
    .catch(error => {
        console.error('Error:', error);
        showError('Failed to analyze code. Please try again.');
    })
    .finally(() => {
        hideLoading();
    });
}

// Load example code
function loadExample(language, exampleType) {
    if (codeExamples[language] && codeExamples[language][exampleType]) {
        // Set language
        if (languageSelect) {
            languageSelect.value = language;
        }

        // Set code
        if (codeTextarea) {
            codeTextarea.value = codeExamples[language][exampleType];
        }

        // Set analysis type to explanation for examples
        if (analysisTypeSelect) {
            analysisTypeSelect.value = 'explanation';
        }

        // Validate form
        validateForm();

        // Add visual feedback
        if (codeTextarea) {
            codeTextarea.classList.add('slide-up');
            setTimeout(() => {
                codeTextarea.classList.remove('slide-up');
            }, 300);
        }
    }
}

// Utility functions
function validateForm() {
    const language = languageSelect?.value;
    const analysisType = analysisTypeSelect?.value;
    const code = codeTextarea?.value?.trim();

    let isValid = true;

    // Clear previous validation states
    clearValidationStates();

    // Validate language
    if (!language) {
        setFieldError(languageSelect, 'Please select a programming language');
        isValid = false;
    }

    // Validate analysis type
    if (!analysisType) {
        setFieldError(analysisTypeSelect, 'Please select an analysis type');
        isValid = false;
    }

    // Validate code
    if (!code) {
        setFieldError(codeTextarea, 'Please enter some code to analyze');
        isValid = false;
    } else if (code.length < 10) {
        setFieldError(codeTextarea, 'Code seems too short for meaningful analysis');
        isValid = false;
    }

    // Update button state
    if (analyzeBtn) {
        analyzeBtn.disabled = !isValid;
    }

    return isValid;
}

function clearValidationStates() {
    const fields = [languageSelect, analysisTypeSelect, codeTextarea];
    fields.forEach(field => {
        if (field) {
            field.classList.remove('is-invalid', 'is-valid');
            const feedback = field.parentNode.querySelector('.invalid-feedback');
            if (feedback) {
                feedback.remove();
            }
        }
    });
}

function setFieldError(field, message) {
    if (field) {
        field.classList.add('is-invalid');

        // Remove existing feedback
        const existingFeedback = field.parentNode.querySelector('.invalid-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }

        // Add new feedback
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        feedback.textContent = message;
        field.parentNode.appendChild(feedback);
    }
}

function showLoading() {
    if (loadingModal) {
        loadingModal.show();
    }

    if (analyzeBtn) {
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    }
}

function hideLoading() {
    if (loadingModal) {
        loadingModal.hide();
    }

    if (analyzeBtn) {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-magic"></i> Analyze Code';
    }
}

function showError(message) {
    // Create error alert
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show';
    alert.innerHTML = `
        <strong>Error:</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Insert at top of main content
    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(alert, main.firstChild);
    }
}

function updatePlaceholder() {
    if (codeTextarea && languageSelect) {
        const language = languageSelect.value;
        const placeholders = {
            python: 'def hello_world():\n    print("Hello, World!")\n\nhello_world()',
            javascript: 'function helloWorld() {\n    console.log("Hello, World!");\n}\n\nhelloWorld();',
            java: 'public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
            cpp: '#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello, World!" << endl;\n    return 0;\n}',
            default: 'Paste your code here...'
        };

        codeTextarea.placeholder = placeholders[language] || placeholders.default;
    }
}

function updateAnalysisDescription() {
    // Could add dynamic descriptions based on analysis type
    // For now, this is a placeholder for future enhancements
}

function handleCodeInput(event) {
    // Handle tab key for proper indentation
    if (event.key === 'Tab') {
        event.preventDefault();
        const start = event.target.selectionStart;
        const end = event.target.selectionEnd;

        // Insert tab character
        event.target.value = event.target.value.substring(0, start) +
                           '    ' +
                           event.target.value.substring(end);

        // Move cursor
        event.target.selectionStart = event.target.selectionEnd = start + 4;
    }
}

function validateCode() {
    // Real-time code validation could be added here
    // For now, just trigger form validation
    validateForm();
}

// Make loadExample globally available
window.loadExample = loadExample;

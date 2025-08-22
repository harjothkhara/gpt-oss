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
            self.transaction_history.append(f"Deposited $" + str(amount))
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew $" + str(amount))
            return True
        return False

    def get_balance(self):
        return self.balance

# Example usage
account = BankAccount("John Doe", 1000)
account.deposit(500)
account.withdraw(200)
print(f"Balance: $" + str(account.get_balance()))`
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

// Function to aggressively hide loading modal
function hideLoadingModal() {
    console.log('Hiding loading modal...');

    // Find modal element - try multiple approaches
    let modalElement = null;

    // Try to get the actual DOM element from Bootstrap modal
    if (loadingModal && loadingModal._element) {
        modalElement = loadingModal._element;
    } else {
        modalElement = document.getElementById('loadingModal');
    }

    // Force hide modal using multiple methods
    if (modalElement && modalElement.style) {
        modalElement.style.display = 'none';
        modalElement.style.visibility = 'hidden';
        modalElement.classList.remove('show', 'fade');
        modalElement.setAttribute('aria-hidden', 'true');
    }

    // Try Bootstrap modal hide method
    if (loadingModal && typeof loadingModal.hide === 'function') {
        try {
            loadingModal.hide();
        } catch (e) {
            console.log('Modal hide method failed:', e);
        }
    }

    // Remove all modal backdrops
    document.querySelectorAll('.modal-backdrop').forEach(el => {
        try {
            el.remove();
        } catch (e) {
            console.log('Error removing backdrop:', e);
        }
    });

    // Reset body
    document.body.classList.remove('modal-open');
    document.body.style.overflow = '';
    document.body.style.paddingRight = '';
    document.body.style.marginRight = '';

    console.log('Loading modal hidden');
}

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

    // Clear code button
    const clearCodeBtn = document.getElementById('clearCodeBtn');
    if (clearCodeBtn) {
        clearCodeBtn.addEventListener('click', clearCode);
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
        console.log('Analysis complete, received HTML response');
        console.log('Response length:', html.length);
        console.log('Response preview:', html.substring(0, 200));

        // Clear timer first
        if (loadingTimer) {
            clearTimeout(loadingTimer);
            loadingTimer = null;
        }

        // Hide loading modal immediately
        hideLoadingModal();

        // Small delay to ensure modal is fully hidden
        setTimeout(() => {
            // Replace the page content with the response
            try {
                // Parse the HTML response to extract just the body content
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newBody = doc.body;

                if (newBody) {
                    // Replace body content
                    document.body.innerHTML = newBody.innerHTML;
                    console.log('Page content replaced successfully');
                } else {
                    console.error('No body found in response HTML');
                    throw new Error('Invalid HTML response');
                }
            } catch (error) {
                console.error('Error replacing page content:', error);
                showError('Failed to display analysis results. Please try again.');
                return;
            }

            // Clean up any modal remnants after page replacement
            setTimeout(() => {
                const allBackdrops = document.querySelectorAll('.modal-backdrop');
                allBackdrops.forEach(backdrop => backdrop.remove());
                document.body.classList.remove('modal-open');
                document.body.style.overflow = '';
                document.body.style.paddingRight = '';
                document.body.style.marginRight = '';

                // Reinitialize after content replacement
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

                console.log('Page reinitialized successfully');
            }, 100);
        }, 100); // End of setTimeout for modal hiding delay
    })
    .catch(error => {
        console.error('Error:', error);
        showError('Failed to analyze code. Please try again.');
    })
    .finally(() => {
        hideLoading();
    });
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

function clearCode() {
    if (codeTextarea) {
        // Clear the textarea
        codeTextarea.value = '';

        // Clear any validation states
        codeTextarea.classList.remove('is-invalid', 'is-valid');
        const feedback = codeTextarea.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.remove();
        }

        // Focus back to textarea for immediate typing
        codeTextarea.focus();

        // Trigger validation to update form state
        validateForm();

        console.log('Code textarea cleared');
    }
}

let loadingTimer = null;

function showLoading() {
    if (loadingModal) {
        loadingModal.show();
    }

    if (analyzeBtn) {
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    }

    // Set 3-second timer as backup
    loadingTimer = setTimeout(() => {
        console.log('3-second timer: Force hiding loading modal');
        forceHideLoading();
    }, 3000);

    // Also start checking for results
    startResultsDetection();
}

function hideLoading() {
    // Clear the timer if it exists
    if (loadingTimer) {
        clearTimeout(loadingTimer);
        loadingTimer = null;
    }

    forceHideLoading();
}

function forceHideLoading() {
    console.log('Force hiding loading modal');

    // Find loading modal (might be different after page replacement)
    const modal = loadingModal || document.getElementById('loadingModal');
    if (modal) {
        // Try Bootstrap modal hide method first
        if (modal.hide && typeof modal.hide === 'function') {
            modal.hide();
        } else {
            // Fallback to manual hiding
            modal.style.display = 'none';
            modal.classList.remove('show');
        }

        // Remove any Bootstrap modal backdrop
        const backdrop = document.querySelector('.modal-backdrop');
        if (backdrop) {
            backdrop.remove();
        }

        // Reset body classes that Bootstrap modal adds
        document.body.classList.remove('modal-open');
        document.body.style.overflow = '';
        document.body.style.paddingRight = '';
    }

    // Reset button state
    const btn = analyzeBtn || document.querySelector('button[type="submit"]');
    if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-magic"></i> Analyze Code';
    }
}

function startResultsDetection() {
    let checkCount = 0;
    const maxChecks = 30; // Check for 3 seconds (100ms intervals)

    const checkForResults = () => {
        checkCount++;

        // Look for analysis results on the page
        const resultsCard = document.querySelector('.card .bg-success');
        const analysisContent = document.querySelector('.card-body p, .card-body div');

        if (resultsCard || (analysisContent && analysisContent.textContent.includes('What this code actually does'))) {
            console.log('Results detected! Hiding loading modal');
            forceHideLoading();
            return;
        }

        // Continue checking if we haven't reached max checks
        if (checkCount < maxChecks) {
            setTimeout(checkForResults, 100);
        }
    };

    // Start checking after a brief delay
    setTimeout(checkForResults, 200);
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

// Load example code function - defined at the end to ensure codeExamples is available
function loadExample(language, exampleType) {
    console.log('loadExample called with:', language, exampleType);

    if (codeExamples[language] && codeExamples[language][exampleType]) {
        console.log('Found example code');

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
        if (typeof validateForm === 'function') {
            validateForm();
        }

        // Add visual feedback
        if (codeTextarea) {
            codeTextarea.classList.add('slide-up');
            setTimeout(() => {
                codeTextarea.classList.remove('slide-up');
            }, 300);
        }
    } else {
        console.error('Example not found:', language, exampleType);
        console.log('Available examples:', codeExamples);
    }
}

// Make loadExample globally available
window.loadExample = loadExample;

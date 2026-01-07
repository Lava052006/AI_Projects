// Job Scam Detector Chrome Extension - Popup Script

const API_BASE_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', function() {
    console.log('Job Scam Detector Extension loaded');
    
    // Get DOM elements
    const analyzeBtn = document.getElementById('analyze-btn');
    const jobDescription = document.getElementById('job-description');
    const resultSection = document.getElementById('result-section');
    const verdict = document.getElementById('verdict');
    const riskScore = document.getElementById('risk-score');
    const flagsList = document.getElementById('flags-list');
    
    // Add event listener to analyze button
    analyzeBtn.addEventListener('click', handleAnalyzeClick);
    
    // Add event listener to textarea for input validation
    jobDescription.addEventListener('input', handleInputChange);
});

async function handleAnalyzeClick() {
    const jobDescription = document.getElementById('job-description');
    const analyzeBtn = document.getElementById('analyze-btn');
    const text = jobDescription.value.trim();
    
    // Handle empty input
    if (!text) {
        alert('Please enter a job description to analyze.');
        return;
    }
    
    // Disable button and show loading state
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = 'Analyzing...';
    
    try {
        // Make API call to backend
        const result = await analyzeJobPosting(text);
        displayResults(result);
    } catch (error) {
        handleErrors(error);
    } finally {
        // Re-enable button
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = 'Analyze Job';
    }
}

function handleInputChange() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const jobDescription = document.getElementById('job-description');
    
    // Enable/disable button based on input
    analyzeBtn.disabled = !jobDescription.value.trim();
}

async function analyzeJobPosting(jobText) {
    const requestBody = {
        job_text: jobText,
        company_url: "",
        recruiter_email: "",
        platform_source: "chrome"
    };
    
    const response = await fetch(`${API_BASE_URL}/api/v1/analyze-job`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
    });
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
}

function displayResults(results) {
    const resultSection = document.getElementById('result-section');
    const verdict = document.getElementById('verdict');
    const riskScore = document.getElementById('risk-score');
    const flagsList = document.getElementById('flags-list');
    
    // Update verdict with proper class mapping
    verdict.textContent = results.verdict;
    
    // Clear any existing verdict classes
    verdict.className = 'verdict';
    
    // Apply appropriate class based on verdict
    const verdictLower = results.verdict.toLowerCase();
    if (verdictLower === 'safe') {
        verdict.classList.add('safe');
    } else if (verdictLower === 'caution') {
        verdict.classList.add('caution');
    } else if (verdictLower === 'high risk') {
        verdict.classList.add('high-risk');
    }
    
    // Update risk score
    riskScore.textContent = results.risk_score + '/100';
    if (results.risk_score < 30) {
        riskScore.className = 'risk-score low';
    } else if (results.risk_score < 70) {
        riskScore.className = 'risk-score medium';
    } else {
        riskScore.className = 'risk-score high';
    }
    
    // Update flags
    flagsList.innerHTML = '';
    if (results.flags && results.flags.length > 0) {
        results.flags.forEach(flag => {
            const li = document.createElement('li');
            li.textContent = flag;
            flagsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.textContent = 'No specific warning flags detected.';
        li.style.color = '#666';
        li.style.fontStyle = 'italic';
        flagsList.appendChild(li);
    }
    
    // Show result section
    resultSection.classList.remove('hidden');
}

function handleErrors(error) {
    console.error('Analysis error:', error);
    
    // Hide any existing results
    const resultSection = document.getElementById('result-section');
    resultSection.classList.add('hidden');
    
    // Show user-friendly error message
    let errorMessage = 'Unable to analyze the job posting. ';
    
    if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        errorMessage += 'Please make sure the Job Analysis API is running on localhost:8000.';
    } else if (error.message.includes('400')) {
        errorMessage += 'The job description format is invalid.';
    } else if (error.message.includes('422')) {
        errorMessage += 'Please provide a valid job description.';
    } else if (error.message.includes('429')) {
        errorMessage += 'Too many requests. Please wait a moment and try again.';
    } else if (error.message.includes('500')) {
        errorMessage += 'Server error. Please try again later.';
    } else {
        errorMessage += 'Please try again later.';
    }
    
    alert(errorMessage);
}

// Keep the mock function for fallback/testing
function showMockResult() {
    const mockResult = {
        verdict: 'Caution',
        risk_score: 65,
        flags: [
            'Unusually high salary for entry-level position',
            'Vague job requirements',
            'Requests personal information upfront'
        ]
    };
    
    displayResults(mockResult);
}
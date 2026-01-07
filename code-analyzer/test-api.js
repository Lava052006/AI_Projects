// Simple test script to demonstrate the AI feedback API
const testCode = `def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(result)`;

const requestBody = {
    prompt: testCode
};

fetch('http://localhost:4000/api/ai/feedback', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestBody)
})
.then(response => response.json())
.then(data => {
    console.log('🤖 AI Feedback Response:');
    console.log('='.repeat(50));
    console.log(JSON.stringify(data, null, 2));
})
.catch(error => {
    console.error('❌ Error:', error);
});
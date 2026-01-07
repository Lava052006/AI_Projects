// Test error handling with invalid requests
console.log('🧪 Testing Error Handling:');
console.log('='.repeat(40));

// Test 1: Empty prompt
console.log('\n1️⃣ Testing with empty prompt...');
fetch('http://localhost:4000/api/ai/feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt: '' })
})
.then(response => response.json())
.then(data => {
    console.log('Response:', JSON.stringify(data, null, 2));
})
.catch(error => console.error('Error:', error));

// Test 2: Missing prompt field
setTimeout(() => {
    console.log('\n2️⃣ Testing with missing prompt field...');
    fetch('http://localhost:4000/api/ai/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: 'print("hello")' }) // wrong field name
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', JSON.stringify(data, null, 2));
    })
    .catch(error => console.error('Error:', error));
}, 1000);

// Test 3: Invalid JSON
setTimeout(() => {
    console.log('\n3️⃣ Testing with invalid JSON...');
    fetch('http://localhost:4000/api/ai/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: 'invalid json'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', JSON.stringify(data, null, 2));
    })
    .catch(error => console.error('Error:', error));
}, 2000);
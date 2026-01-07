// Test frontend-backend connection with security-focused example
console.log('🔗 Testing Frontend-Backend Connection');
console.log('='.repeat(45));

const securityTestCode = `def login(username, password):
    # SECURITY ISSUE: Plain text password comparison
    users = {
        'admin': 'password123',
        'user': 'qwerty'
    }
    
    # VULNERABILITY: No rate limiting or account lockout
    if username in users and users[username] == password:
        return {'success': True, 'role': 'admin' if username == 'admin' else 'user'}
    
    return {'success': False}

# Usage
result = login('admin', 'password123')
print(f"Login result: {result}")`;

async function testConnection() {
    console.log('📝 Testing with Security-Focused Python Code:');
    console.log('Code contains multiple security vulnerabilities...\n');
    
    console.log('🔄 Sending request to backend API...');
    
    try {
        const startTime = Date.now();
        
        // This simulates what the frontend does when user clicks "ANALYZE CODE"
        const response = await fetch('http://localhost:4000/api/ai/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                prompt: `Analyze this Python code for security vulnerabilities and best practices:\n\n${securityTestCode}` 
            })
        });
        
        const data = await response.json();
        const endTime = Date.now();
        const responseTime = ((endTime - startTime) / 1000).toFixed(2);
        
        console.log(`⚡ Response received in ${responseTime} seconds`);
        console.log(`📊 Status: ${response.status} ${response.statusText}`);
        
        if (data.feedback) {
            console.log('\n🤖 AI Security Analysis Output:');
            console.log('='.repeat(40));
            console.log(data.feedback);
            
            console.log('\n✅ Connection Test Results:');
            console.log('• Frontend → Backend: ✅ Connected');
            console.log('• API Endpoint: ✅ Responding');
            console.log('• AI Analysis: ✅ Working');
            console.log('• Security Focus: ✅ Implemented');
            
        } else if (data.error) {
            console.log('\n❌ API Error:');
            console.log(`Error: ${data.error}`);
            console.log(`Message: ${data.message}`);
        }
        
    } catch (error) {
        console.log('\n❌ Connection Failed:');
        console.log(`Error: ${error.message}`);
        console.log('\n💡 Troubleshooting:');
        console.log('• Make sure backend is running: npm run dev');
        console.log('• Check if port 4000 is accessible');
        console.log('• Verify CORS is properly configured');
    }
}

console.log('🌐 Frontend URL: http://localhost:5173');
console.log('🔧 Backend API: http://localhost:4000/api/ai/feedback');
console.log('');

testConnection();
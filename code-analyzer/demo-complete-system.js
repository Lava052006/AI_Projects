// Complete system demonstration
console.log('🚀 AI Code Feedback System Demo');
console.log('='.repeat(60));

// Test different types of code examples
const codeExamples = [
    {
        name: "Simple Function",
        code: `def greet(name):
    return "Hello, " + name

print(greet("World"))`
    },
    {
        name: "Class with Issues",
        code: `class BankAccount:
    def __init__(self, balance):
        self.balance = balance
    
    def withdraw(self, amount):
        self.balance = self.balance - amount  # No validation!
        return self.balance
    
    def deposit(self, amount):
        self.balance += amount
        return self.balance

# Usage
account = BankAccount(100)
print(account.withdraw(150))  # Allows overdraft!`
    },
    {
        name: "Algorithm Implementation",
        code: `def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers)
print(sorted_numbers)`
    }
];

async function testCodeExample(example, index) {
    console.log(`\n${index + 1}️⃣ Testing: ${example.name}`);
    console.log('-'.repeat(40));
    console.log('📝 Code:');
    console.log(example.code);
    console.log('\n🔄 Getting AI feedback...');
    
    const startTime = Date.now();
    
    try {
        const response = await fetch('http://localhost:4000/api/ai/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: example.code })
        });
        
        const data = await response.json();
        const endTime = Date.now();
        const duration = ((endTime - startTime) / 1000).toFixed(2);
        
        console.log(`⚡ Response time: ${duration}s`);
        console.log('\n🤖 AI Feedback:');
        
        if (data.feedback) {
            // Format the feedback nicely
            const feedback = data.feedback;
            console.log(feedback);
        } else if (data.error) {
            console.log(`❌ Error: ${data.error}`);
            console.log(`📝 Message: ${data.message}`);
        }
        
    } catch (error) {
        console.log(`❌ Network Error: ${error.message}`);
    }
    
    console.log('\n' + '='.repeat(60));
}

// Test all examples
async function runDemo() {
    // First check if server is running
    try {
        const healthCheck = await fetch('http://localhost:4000/health');
        const health = await healthCheck.json();
        console.log(`✅ Server Status: ${health.status}`);
        console.log('🌐 Server URL: http://localhost:4000');
        
        // Test each code example
        for (let i = 0; i < codeExamples.length; i++) {
            await testCodeExample(codeExamples[i], i);
            // Add delay between requests
            if (i < codeExamples.length - 1) {
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        }
        
        console.log('\n🎉 Demo Complete!');
        console.log('\n📋 Summary:');
        console.log('• Backend server running on port 4000');
        console.log('• Health endpoint: GET /health');
        console.log('• AI feedback endpoint: POST /api/ai/feedback');
        console.log('• Supports both mock and Ollama AI providers');
        console.log('• Proper error handling and validation');
        
    } catch (error) {
        console.log('❌ Server not running or not accessible');
        console.log('💡 Make sure to run: npm run dev');
    }
}

runDemo();
// Test with more complex code to demonstrate detailed feedback
const complexCode = `class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"Added {a} + {b} = {result}")
        return result
    
    def divide(self, a, b):
        result = a / b  # No error handling for division by zero
        self.history.append(f"Divided {a} / {b} = {result}")
        return result
    
    def get_history(self):
        return self.history

# Usage without proper error handling
calc = Calculator()
print(calc.add(5, 3))
print(calc.divide(10, 0))  # This will cause an error
print(calc.get_history())`;

const requestBody = {
    prompt: complexCode
};

console.log('📝 Testing with Complex Python Code:');
console.log('='.repeat(60));
console.log(complexCode);
console.log('\n🔄 Sending to AI for analysis...\n');

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
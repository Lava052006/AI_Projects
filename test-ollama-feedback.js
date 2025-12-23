// Test with Ollama AI provider for real AI feedback
const testCode = `def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# Test the function
scores = [85, 92, 78, 96, 88]
avg = calculate_average(scores)
print(f"Average score: {avg}")`;

console.log('🧠 Testing with Ollama AI Provider:');
console.log('='.repeat(50));
console.log('📝 Code to analyze:');
console.log(testCode);
console.log('\n🔄 Sending to Ollama AI for analysis...');
console.log('⏳ This may take a few seconds...\n');

const startTime = Date.now();

fetch('http://localhost:4000/api/ai/feedback', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt: testCode })
})
.then(response => {
    const endTime = Date.now();
    const duration = ((endTime - startTime) / 1000).toFixed(2);
    console.log(`⚡ Response received in ${duration} seconds`);
    return response.json();
})
.then(data => {
    console.log('\n🤖 Ollama AI Feedback:');
    console.log('='.repeat(50));
    if (data.feedback) {
        console.log(data.feedback);
    } else if (data.error) {
        console.log('❌ Error:', data.error);
        console.log('📝 Message:', data.message);
    }
})
.catch(error => {
    console.error('❌ Network Error:', error.message);
    console.log('\n💡 Note: Make sure Ollama is installed and running with the Mistral model');
    console.log('   Install: https://ollama.ai/');
    console.log('   Run: ollama run mistral');
});
// background.js
console.log("📡 Sending job to backend", jobData);
console.log("✅ Backend response", result);


chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'analyzeJob') {
    analyzeJob(request.data)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ error: error.message }));
    
    return true; // Keep message channel open for async response
  }
});

async function analyzeJob(jobData) {
  // Your existing AI analysis logic goes here
  // This is where you'd call your AI model or API
  
  const riskScore = calculateRiskScore(jobData);
  const flags = detectRedFlags(jobData);
  
  return {
    riskScore,
    riskLevel: getRiskLevel(riskScore),
    flags
  };
}

function calculateRiskScore(jobData) {
  let score = 0;
  const flags = [];
  
  const text = `${jobData.title} ${jobData.company} ${jobData.description || jobData.snippet}`.toLowerCase();
  
  // Add your existing detection logic here
  // Example red flags:
  
  if (text.includes('urgent') || text.includes('immediate start')) {
    score += 15;
    flags.push('Urgency pressure');
  }
  
  if (text.includes('no experience') && text.includes('high salary')) {
    score += 20;
    flags.push('Unrealistic compensation for experience level');
  }
  
  if (text.match(/\$\d{4,}.*week|weekly/)) {
    score += 15;
    flags.push('Suspicious compensation structure');
  }
  
  // Check for vague description
  if ((jobData.description || jobData.snippet).split(' ').length < 50) {
    score += 10;
    flags.push('Unusually brief job description');
  }
  
  return Math.min(score, 100);
}

function detectRedFlags(jobData) {
  const flags = [];
  const text = `${jobData.title} ${jobData.company} ${jobData.description || ''}`.toLowerCase();
  
  // Add all your red flag checks
  if (text.includes('pay to apply') || text.includes('application fee')) {
    flags.push('🚨 Requests upfront payment');
  }
  
  if (text.includes('work from home') && text.includes('no experience')) {
    flags.push('⚠️ Remote work with no requirements');
  }
  
  // Add more checks based on your existing logic
  
  return flags;
}

function getRiskLevel(score) {
  if (score < 30) return 'low';
  if (score < 60) return 'medium';
  return 'high';
}
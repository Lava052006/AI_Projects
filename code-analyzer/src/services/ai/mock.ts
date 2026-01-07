import { StructuredAIFeedback } from './index.js';

export async function generateMockFeedback(prompt: string) {
  return {
    feedback: `Mock feedback:
Your project idea is well structured. To improve:
• Add clear README documentation
• Include edge-case handling
• Write basic tests
• Improve code readability
Prompt received: "${prompt}"`
  };
}

/**
 * Generates mock structured feedback for testing
 */
export function generateMockStructuredFeedback(prompt: string): StructuredAIFeedback {
  // Simulate different scores based on prompt content
  const score = prompt.length > 50 ? 85 : 70;
  
  return {
    score,
    strengths: [
      'Clear problem statement',
      'Good use of TypeScript interfaces',
      'Well-structured code organization'
    ],
    weaknesses: [
      'Missing error handling in some areas',
      'Could benefit from more comprehensive testing',
      'Documentation could be more detailed'
    ],
    improvements: [
      'Add input validation for all endpoints',
      'Implement comprehensive unit tests',
      'Add API documentation with examples',
      'Consider adding logging for better debugging'
    ],
    summary: `Overall, this is a solid implementation with room for improvement in testing and documentation. The code structure is clean and follows TypeScript best practices.`,
    confidence: 0.9
  };
}

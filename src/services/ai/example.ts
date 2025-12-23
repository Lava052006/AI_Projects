/**
 * Example usage of the structured AI feedback interfaces
 */

import { 
  generateStructuredAIFeedback, 
  parseStructuredFeedback,
  StructuredAIFeedback,
  StructuredAIFeedbackResponse 
} from './index.js';
import { generateMockStructuredFeedback } from './mock.js';

/**
 * Example: Generate structured feedback for code review
 */
export async function exampleCodeReview() {
  const codeToReview = `
    function calculateTotal(items) {
      let total = 0;
      for (let i = 0; i < items.length; i++) {
        total += items[i].price;
      }
      return total;
    }
  `;

  try {
    const response: StructuredAIFeedbackResponse = await generateStructuredAIFeedback({
      prompt: `Please review this JavaScript function for code quality, best practices, and potential improvements:\n\n${codeToReview}`
    });

    console.log('Structured Feedback Analysis:');
    console.log('Score:', response.analysis.score);
    console.log('Strengths:', response.analysis.strengths);
    console.log('Weaknesses:', response.analysis.weaknesses);
    console.log('Improvements:', response.analysis.improvements);
    console.log('Summary:', response.analysis.summary);
    console.log('Confidence:', response.analysis.confidence);

    return response.analysis;
  } catch (error) {
    console.error('Error generating structured feedback:', error);
    throw error;
  }
}

/**
 * Example: Parse existing feedback text into structured format
 */
export function exampleParseExistingFeedback() {
  const existingFeedback = `
    SCORE: 78
    STRENGTHS:
    - Clean function structure
    - Clear variable naming
    WEAKNESSES:
    - No input validation
    - Missing TypeScript types
    IMPROVEMENTS:
    - Add parameter type checking
    - Use TypeScript for better type safety
    - Consider using reduce() for more functional approach
    SUMMARY: Good basic implementation but needs type safety improvements
  `;

  const structured: StructuredAIFeedback = parseStructuredFeedback(existingFeedback);
  
  console.log('Parsed Structured Feedback:');
  console.log(JSON.stringify(structured, null, 2));
  
  return structured;
}

/**
 * Example: Generate mock structured feedback for testing
 */
export function exampleMockFeedback() {
  const mockFeedback = generateMockStructuredFeedback(
    'Review this TypeScript interface for API responses'
  );
  
  console.log('Mock Structured Feedback:');
  console.log(JSON.stringify(mockFeedback, null, 2));
  
  return mockFeedback;
}

/**
 * Example: Validate structured feedback format
 */
export function validateStructuredFeedback(feedback: StructuredAIFeedback): boolean {
  const isValid = 
    typeof feedback.score === 'number' &&
    feedback.score >= 0 && feedback.score <= 100 &&
    Array.isArray(feedback.strengths) &&
    Array.isArray(feedback.weaknesses) &&
    Array.isArray(feedback.improvements) &&
    feedback.strengths.every(s => typeof s === 'string') &&
    feedback.weaknesses.every(w => typeof w === 'string') &&
    feedback.improvements.every(i => typeof i === 'string');

  console.log('Feedback validation result:', isValid);
  return isValid;
}
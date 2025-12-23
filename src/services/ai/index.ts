import { generateMockFeedback } from './mock';
import { generateOllamaFeedback } from './ollama';

export interface AIFeedbackRequest {
  prompt: string;
}

export interface AIFeedbackResponse {
  feedback: string;
}

/**
 * Structured AI feedback interface with detailed analysis
 */
export interface StructuredAIFeedback {
  /** Overall quality score from 0-100 */
  score: number;
  
  /** Array of identified strengths */
  strengths: string[];
  
  /** Array of identified weaknesses or areas of concern */
  weaknesses: string[];
  
  /** Array of specific improvement suggestions */
  improvements: string[];
  
  /** Optional overall summary comment */
  summary?: string;
  
  /** Optional confidence level in the analysis (0-1) */
  confidence?: number;
}

/**
 * Response interface for structured AI feedback
 */
export interface StructuredAIFeedbackResponse {
  /** The structured feedback analysis */
  analysis: StructuredAIFeedback;
  
  /** Raw AI response text (optional, for debugging) */
  rawFeedback?: string;
}

const AI_PROVIDER = (process.env.AI_PROVIDER || 'mock').trim();
console.log('AI_PROVIDER =', AI_PROVIDER);

export async function generateAIFeedback(
  request: AIFeedbackRequest
): Promise<AIFeedbackResponse> {
  const prompt = request.prompt.trim();

  if (!prompt) {
    throw new Error('Prompt must be a non-empty string');
  }

  if (AI_PROVIDER === 'ollama') {
    return generateOllamaFeedback(prompt);
  }

  // Default → mock (safe, fast)
  return generateMockFeedback(prompt);
}

/**
 * Generates structured AI feedback with detailed analysis
 */
export async function generateStructuredAIFeedback(
  request: AIFeedbackRequest
): Promise<StructuredAIFeedbackResponse> {
  const enhancedPrompt = `
Please analyze the following and provide structured feedback:

${request.prompt}

Format your response as follows:
SCORE: [0-100]
STRENGTHS:
- [strength 1]
- [strength 2]
WEAKNESSES:
- [weakness 1]
- [weakness 2]
IMPROVEMENTS:
- [improvement 1]
- [improvement 2]
SUMMARY: [brief overall assessment]
`;

  const response = await generateAIFeedback({ prompt: enhancedPrompt });
  const structured = parseStructuredFeedback(response.feedback);
  
  return {
    analysis: structured,
    rawFeedback: response.feedback
  };
}

/**
 * Parses unstructured AI feedback text into structured format
 */
export function parseStructuredFeedback(feedbackText: string): StructuredAIFeedback {
  const lines = feedbackText.split('\n').map(line => line.trim());
  
  let score = 75; // Default score
  const strengths: string[] = [];
  const weaknesses: string[] = [];
  const improvements: string[] = [];
  let summary = '';
  
  let currentSection = '';
  
  for (const line of lines) {
    if (line.startsWith('SCORE:')) {
      const scoreMatch = line.match(/SCORE:\s*(\d+)/);
      if (scoreMatch) {
        score = Math.min(100, Math.max(0, parseInt(scoreMatch[1], 10)));
      }
    } else if (line.startsWith('STRENGTHS:')) {
      currentSection = 'strengths';
    } else if (line.startsWith('WEAKNESSES:')) {
      currentSection = 'weaknesses';
    } else if (line.startsWith('IMPROVEMENTS:')) {
      currentSection = 'improvements';
    } else if (line.startsWith('SUMMARY:')) {
      summary = line.replace('SUMMARY:', '').trim();
      currentSection = '';
    } else if (line.startsWith('- ') && currentSection) {
      const item = line.substring(2).trim();
      if (item) {
        switch (currentSection) {
          case 'strengths':
            strengths.push(item);
            break;
          case 'weaknesses':
            weaknesses.push(item);
            break;
          case 'improvements':
            improvements.push(item);
            break;
        }
      }
    }
  }
  
  // Fallback parsing if structured format not found
  if (strengths.length === 0 && weaknesses.length === 0 && improvements.length === 0) {
    return parseUnstructuredFeedback(feedbackText);
  }
  
  return {
    score,
    strengths,
    weaknesses,
    improvements,
    summary: summary || undefined,
    confidence: 0.8 // Default confidence for parsed structured feedback
  };
}

/**
 * Fallback parser for unstructured feedback text
 */
function parseUnstructuredFeedback(feedbackText: string): StructuredAIFeedback {
  // Simple heuristic parsing for unstructured text
  const text = feedbackText.toLowerCase();
  
  // Estimate score based on positive/negative keywords
  const positiveWords = ['good', 'great', 'excellent', 'well', 'strong', 'clear'];
  const negativeWords = ['poor', 'weak', 'unclear', 'missing', 'needs', 'should'];
  
  const positiveCount = positiveWords.reduce((count, word) => 
    count + (text.split(word).length - 1), 0);
  const negativeCount = negativeWords.reduce((count, word) => 
    count + (text.split(word).length - 1), 0);
  
  const score = Math.max(30, Math.min(90, 60 + (positiveCount - negativeCount) * 10));
  
  return {
    score,
    strengths: ['Analysis provided in feedback text'],
    weaknesses: ['Detailed analysis not available in structured format'],
    improvements: ['Consider requesting structured feedback format'],
    summary: feedbackText.length > 200 ? 
      feedbackText.substring(0, 200) + '...' : feedbackText,
    confidence: 0.5 // Lower confidence for unstructured parsing
  };
}

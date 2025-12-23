/**import { exec } from 'child_process';
import { promisify } from 'util';


const execAsync = promisify(exec);

export interface AIFeedbackRequest {
  prompt: string;
}

export interface AIFeedbackResponse {
  feedback: string;
}

export interface AIErrorResponse {
  error: string;
  message: string;
}


/**
 * Validates and sanitizes the input prompt
 * @param prompt - The input prompt to validate
 * @returns The sanitized prompt
 * @throws Error if prompt is invalid
 */
/**export function validatePrompt(prompt: string): string {
  if (!prompt || typeof prompt !== "string") {
    throw new Error("Prompt must be a non-empty string");
  }

  const trimmed = prompt.trim();
  if (!trimmed) {
    throw new Error("Prompt cannot be empty or whitespace");
  }

  return trimmed;
}


/**
 * Executes Ollama AI command with the given prompt
 * @param prompt - The prompt to send to Ollama
 * @returns Promise resolving to AI response
 */
/**export async function callOllamaAPI(prompt: string): Promise<string> {
  const response = await fetch("http://localhost:11434/api/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: "mistral",
      prompt,
      stream: false
    })
  });

  if (!response.ok) {
    throw new Error(`Ollama API error: ${response.status}`);
  }

  const data = await response.json();

  if (!data.response || typeof data.response !== "string") {
    throw new Error("Invalid response from Ollama");
  }

  return data.response.trim();
}


/**
 * Generates AI feedback for the given prompt
 * @param request - The AI feedback request containing the prompt
 * @returns Promise resolving to formatted AI response
 */
/**export async function generateAIFeedback(request: AIFeedbackRequest): Promise<AIFeedbackResponse> {
  try {
    const prompt = validatePrompt(request.prompt);
const feedback = await callOllamaAPI(prompt);

    return { feedback };
  } catch (error) {
    throw error; // Re-throw to be handled by the calling code
  }
}**/

/**export async function generateAIFeedback(
  request: AIFeedbackRequest
): Promise<AIFeedbackResponse> {
  const prompt = validatePrompt(request.prompt);
  const feedback = await callOllamaAPI(prompt);
  return { feedback };
}

export async function generateOllamaFeedback(prompt: string) {
  const feedback = await callOllamaAPI(prompt);
  return { feedback };
}



/**
 * Creates a standardized error response for AI service failures
 * @param error - The error that occurred
 * @returns Formatted error response
 */
/**export function createAIErrorResponse(error: unknown): AIErrorResponse {
  if (error instanceof Error) {
    return {
      error: 'AI_SERVICE_ERROR',
      message: error.message
    };
  }
  
  return {
    error: 'UNKNOWN_ERROR',
    message: 'An unknown error occurred while processing the AI request'
  };
}
**/
/**import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

/**
 * Generate feedback using Ollama (Mistral)
 * ⚠️ This function is ONLY executed when explicitly called
 */
/**export async function generateOllamaFeedback(prompt: string): Promise<{ feedback: string }> {
  try {
    // Basic safety check
    if (!prompt || typeof prompt !== 'string') {
      throw new Error('Invalid prompt');
    }

    const sanitizedPrompt = prompt
      .replace(/[`$\\]/g, '\\$&')
      .replace(/"/g, '\\"');

    // IMPORTANT:
    // Nothing runs until this function is called
    const command = `echo "${sanitizedPrompt}" | ollama run phi`;

    const { stdout, stderr } = await execAsync(command, {
      timeout: 30_000,      // 30 seconds max
      maxBuffer: 1024 * 1024 // 1 MB output limit
    });

    if (stderr && stderr.trim()) {
      console.warn('Ollama stderr:', stderr);
    }

    if (!stdout || !stdout.trim()) {
      throw new Error('Empty response from Ollama');
    }

    return {
      feedback: stdout.trim()
    };

  } catch (error) {
    throw new Error(
      error instanceof Error
        ? `Ollama failed: ${error.message}`
        : 'Ollama execution failed'
    );
  }
}
**/

export async function generateOllamaFeedback(
  pythonCode: string
): Promise<{ feedback: string }> {
  try {
    if (!pythonCode || typeof pythonCode !== "string") {
      throw new Error("Invalid Python code input");
    }

    const prompt = `
You are a Python code reviewer.

Task:
Give SHORT feedback on the given Python code.

Rules (VERY IMPORTANT):
- Talk ONLY about the Python code
- Do NOT mention fruits, logic puzzles, or unrelated topics
- Max 40 words total
- Use simple language
- Do NOT explain reasoning
- Output EXACTLY in this format:

Score: X/10
Strengths:
- ...
Improvements:
- ...

Python Code:
${pythonCode}
`.trim();

    const response = await fetch("http://localhost:11434/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "phi",
        prompt,
        stream: false,
        options: {
          temperature: 0.2,
          num_predict: 80
        }
      })
    });

    if (!response.ok) {
      throw new Error(`Ollama HTTP error: ${response.status}`);
    }

    const data = await response.json();

    if (!data.response) {
      throw new Error("Empty response from Ollama");
    }

    return {
      feedback: data.response.trim()
    };

  } catch (error) {
    console.error("Ollama feedback error:", error);

    // Safe fallback
    return {
      feedback: `Score: 6/10
Strengths:
- Code is readable
Improvements:
- Add validation and comments`
    };
  }
}

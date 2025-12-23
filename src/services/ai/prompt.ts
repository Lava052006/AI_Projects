export function buildPythonReviewPrompt(code: string): string {
  return `
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
- Write 1 short bullet only

Improvements:
- Write at most 2 short bullets

Python Code:
${code}
`
}

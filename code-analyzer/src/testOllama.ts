import { generateOllamaFeedback } from "./services/ai/ollama";

async function test() {
  const code = `
def add(a, b):
    return a + b
  `;

  const result = await generateOllamaFeedback(code);
  console.log(result.feedback);
}

test();

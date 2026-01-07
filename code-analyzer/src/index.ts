import 'dotenv/config';

import express from 'express';
import cors from 'cors';
import { generateAIFeedback } from './services/ai';

const app = express();
const PORT = 4000;

app.use(cors());
app.use(express.json());

app.get('/health', (_req, res) => {
  res.json({ status: 'ok' });
});

// AI feedback endpoint
app.post('/api/ai/feedback', async (req, res) => {
  try {
    if (!req.body || typeof req.body !== 'object') {
      return res.status(400).json({
        error: 'INVALID_REQUEST',
        message: 'Request body must be a valid JSON object'
      });
    }

    const { prompt } = req.body;

    if (!prompt || typeof prompt !== 'string' || !prompt.trim()) {
      return res.status(400).json({
        error: 'INVALID_PROMPT',
        message: 'Prompt field is required and must be a non-empty string'
      });
    }

    const result = await generateAIFeedback({
      prompt: prompt.trim()
    });

    res.json(result);

  } catch (error) {
    console.error('AI feedback error:', error);

    res.status(500).json({
      error: 'AI_SERVICE_ERROR',
      message: error instanceof Error
        ? error.message
        : 'Unknown AI error'
    });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

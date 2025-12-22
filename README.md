##🧠 AI Code Feedback System

An **AI-powered code review platform** that analyzes user-written code and provides **structured, actionable feedback** on code quality, readability, best practices, and potential issues.

This project is designed as a **long-term resume project**, focusing on **clean system design, AI integration, and developer-focused UI/UX**, rather than relying solely on proprietary APIs.

---

## ✨ Motivation

Writing correct code is not enough — writing **clean, readable, and maintainable code** is equally important.

This project aims to:

* Help developers improve their code quality
* Simulate feedback from a **senior software engineer**
* Explore the practical use of **LLMs for automated code review**
* Compare proprietary and open-source AI models in later phases

---

## 🚀 Phase 1 Overview (Current)

**Phase 1 focuses on building a reliable, end-to-end baseline system** using an LLM to provide structured code feedback.

> Later phases will introduce open-source models, static analysis, and model comparison.

---

## 🧩 Features (Phase 1)

### ✅ Code Input Interface

* VS Code–like editor using **Monaco Editor**
* Syntax highlighting
* Language selection (Python, JavaScript, C++)
* Clean, developer-friendly UI (Dark mode)

---

### 🤖 AI-Powered Code Review

* Uses **GPT-3.5** as a baseline reviewer
* AI is prompted to behave like a **senior software engineer**
* Reviews code for:

  * Readability
  * Logical correctness (basic)
  * Naming conventions
  * Code structure
  * Best practices
  * Potential edge cases

---

### 📊 Structured Feedback Output

Feedback is returned in **structured JSON format**, not plain text:

* ✅ Strengths
* ⚠️ Issues
* 💡 Suggestions
* 🚀 Optimization opportunities
* 🧠 Edge cases to consider

This makes feedback:

* Easy to display
* Easy to extend
* Easy to compare across models (future phases)

---

### 🛡️ Error Handling

* Empty code input validation
* Unsupported language handling
* Graceful fallback for AI/API failures

---

## 🔄 System Flow Diagram

```text
User
 │
 │ writes code
 ▼
Frontend (React + Monaco Editor)
 │
 │ POST /analyze
 ▼
Backend API (Node.js / FastAPI)
 │
 │ build prompt
 │ call LLM (GPT-3.5)
 ▼
LLM Response (JSON)
 │
 │ parse & validate
 ▼
Structured Feedback
 │
 ▼
Frontend Feedback Dashboard
```

---

## 🧱 Tech Stack

### Frontend

* **React (Vite)**
* **Tailwind CSS**
* **Monaco Editor**
* Axios / Fetch API

---

### Backend

* **Node.js + Express**
  *(FastAPI alternative supported)*
* REST API architecture
* Environment-based configuration (`.env`)

---

### AI / LLM

* **GPT-3.5 (Baseline Model)**
* Prompt-engineered for structured code reviews
* JSON-only response format for reliability

---

## 📦 API Design

### `POST /analyze`

#### Request Body

```json
{
  "language": "python",
  "code": "def add(a, b): return a + b"
}
```

#### Response Body

```json
{
  "strengths": [],
  "issues": [],
  "suggestions": [],
  "optimizations": [],
  "edge_cases": []
}
```

---

## 🧠 Prompt Design Strategy

The LLM is instructed to:

* Act as a **senior software engineer**
* Review code written by a junior developer
* Return feedback **strictly in JSON format**

This ensures:

* Consistency
* Easy parsing
* Extensibility for future phases

---

## 📁 Project Structure

```text
ai-code-feedback/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│
├── backend/
│   ├── routes/
│   ├── services/
│   │   └── aiService.js
│   ├── app.js
│   └── .env
│
├── README.md
└── .gitignore
```

---

## ✅ Phase 1 Completion Criteria

Phase 1 is considered complete when:

* Code editor works smoothly
* Feedback is structured and readable
* UI is clean and professional
* AI responses are fast and reliable
* No crashes during normal usage

---

## 🔮 Roadmap

* **Phase 2:** Integrate open-source LLMs (Code LLaMA via cloud inference)
* **Phase 3:** Hybrid system (static code analysis + AI reasoning)
* **Phase 4:** Model comparison & optimization analysis
* **Phase 5:** Technical blog and evaluation report

---

## 📌 Resume Highlight

> Built a full-stack AI-powered code review platform that analyzes user-submitted code and provides structured feedback on readability, correctness, and best practices using large language models.

---

## 🧠 Key Learnings (So Far)

* Designing AI systems requires **structure and constraints**
* Model-agnostic architecture enables easy upgrades
* UI clarity is as important as AI accuracy
* Structured outputs dramatically improve reliability

---

## 📜 License

This project is for educational and portfolio purposes.

---



<<<<<<< HEAD
# 🛡️ CyberSec Code Analyzer

A comprehensive AI-powered code feedback platform with a cybersecurity focus, featuring real-time code analysis and a sleek dark-themed interface.

## 🚀 Features

### 🎯 **Core Functionality**
- **AI-Powered Code Analysis**: Real-time security vulnerability detection
- **Multi-Language Support**: Python, JavaScript, C, C++, Java, Go, Rust
- **Dual AI Providers**: Mock (fast testing) and Ollama (real AI analysis)
- **Security-Focused**: Specialized prompts for cybersecurity analysis

### 🎨 **Cybersecurity-Themed UI**
- **Dark Cyber Aesthetic**: Matrix-style background with green accents
- **Professional Interface**: Clean, modern design with cyber elements
- **Real-time Feedback**: Live analysis results with loading states
- **Responsive Design**: Works on desktop, tablet, and mobile

### 🔧 **Technical Stack**
- **Backend**: Express.js + TypeScript
- **Frontend**: React + TypeScript + Tailwind CSS
- **AI Integration**: Ollama (Phi model) + Mock provider
- **Database**: PostgreSQL with Prisma ORM

## 📦 Installation

### Prerequisites
- Node.js (v18 or higher)
- npm or yarn
- Ollama (for AI analysis)
- PostgreSQL (optional, for database features)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai_proj1
```

### 2. Install Backend Dependencies
```bash
npm install
```

### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
# AI Configuration
AI_PROVIDER=ollama  # or 'mock' for testing

# Database (optional)
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

### 5. Install and Set Up Ollama
```bash
# Install Ollama (visit https://ollama.ai for installation instructions)
# Pull the Phi model
ollama pull phi
```

## 🚀 Running the Application

### Start Backend Server
```bash
# For Ollama AI provider
npm run dev:ollama

# For Mock AI provider (testing)
npm run dev
```

### Start Frontend Development Server
```bash
cd frontend
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:4000
- **Health Check**: http://localhost:4000/health

## 🧪 Testing

The project includes comprehensive test scripts:

```bash
# Test full system integration
node test-full-system.js

# Test Ollama AI feedback
node test-ollama-feedback.js

# Test frontend-backend connection
node test-frontend-backend-connection.js

# Test error handling
node test-error-handling.js

# Demo complete system
node demo-complete-system.js
```

## 📡 API Endpoints

### Health Check
```http
GET /health
```

### AI Feedback Analysis
```http
POST /api/ai/feedback
Content-Type: application/json

{
  "prompt": "Analyze this code for security vulnerabilities: def login(user, pwd): return user == 'admin' and pwd == '123'"
}
```

## 🎨 UI Components

### Code Input Section
- **Language Selector**: Dropdown with 7 programming languages
- **Code Editor**: Syntax-highlighted textarea with cyber styling
- **Analysis Button**: Triggers AI security analysis

### Output Section
- **Loading States**: Animated scanning indicators
- **Error Handling**: Professional error messages
- **Success Display**: Structured AI feedback with timestamps
- **Provider Indication**: Shows whether using Mock or Ollama AI

## 🔧 Configuration

### AI Provider Selection
The system supports two AI providers:

1. **Mock Provider** (Default for testing)
   - Fast responses
   - Consistent output
   - No external dependencies

2. **Ollama Provider** (Real AI analysis)
   - Uses Phi model
   - Security-focused analysis
   - Requires Ollama installation

Switch between providers using the `AI_PROVIDER` environment variable.

### Customization
- **Themes**: Modify `frontend/src/index.css` for styling
- **Languages**: Add new languages in `frontend/src/pages/Home.tsx`
- **AI Prompts**: Customize analysis prompts in `src/services/ai/ollama.ts`

## 🛡️ Security Features

### Code Analysis Focus Areas
- **Vulnerability Detection**: SQL injection, XSS, buffer overflows
- **Best Practices**: Secure coding patterns
- **Input Validation**: Parameter sanitization
- **Authentication**: Password security, session management

### Security Measures
- **Input Sanitization**: All user inputs are validated
- **CORS Configuration**: Proper cross-origin resource sharing
- **Error Handling**: Secure error messages without information leakage

## 📁 Project Structure

```
ai_proj1/
├── src/                    # Backend source code
│   ├── services/ai/        # AI service implementations
│   └── index.ts           # Express server
├── frontend/              # React frontend
│   ├── src/
│   │   ├── pages/         # React pages
│   │   └── components/    # Reusable components
│   └── public/           # Static assets
├── prisma/               # Database schema
├── test-*.js            # Test scripts
└── demo-*.js           # Demo scripts
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the ISC License.

## 🙏 Acknowledgments

- **Ollama**: For providing the AI inference engine
- **Tailwind CSS**: For the utility-first CSS framework
- **React**: For the frontend framework
- **Express.js**: For the backend framework

---

**Built with ❤️ for cybersecurity-focused code analysis**

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


>>>>>>> 9edd764fb87e21736d831f37a7c2b0820b113179

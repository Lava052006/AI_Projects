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
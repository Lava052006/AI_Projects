/**
 * CyberSec Code Analyzer
 * 
 * Cybersecurity-themed code analysis application
 * Features:
 * - Dark cybersecurity aesthetic with green accents
 * - Language selection dropdown
 * - Code input area
 * - AI feedback display
 * - Real-time connection to backend API
 */

import { useState } from 'react';

interface FeedbackData {
  feedback: string;
}

const languages = [
  { value: 'python', label: '🐍 Python', extension: 'py' },
  { value: 'javascript', label: '🟨 JavaScript', extension: 'js' },
  { value: 'c', label: '⚡ C', extension: 'c' },
  { value: 'cpp', label: '⚡ C++', extension: 'cpp' },
  { value: 'java', label: '☕ Java', extension: 'java' },
  { value: 'go', label: '🔵 Go', extension: 'go' },
  { value: 'rust', label: '🦀 Rust', extension: 'rs' },
];

const placeholderCode = {
  python: `# Enter your Python code here
def secure_hash(password):
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

# Example usage
hashed = secure_hash("mypassword")
print(f"Hash: {hashed}")`,
  
  javascript: `// Enter your JavaScript code here
function validateInput(userInput) {
    // Basic XSS prevention
    return userInput.replace(/<script.*?>/gi, '');
}

// Example usage
const cleanInput = validateInput(userInput);
console.log(cleanInput);`,
  
  c: `// Enter your C code here
#include <stdio.h>
#include <string.h>

int secure_strcmp(const char* a, const char* b) {
    return strcmp(a, b) == 0;
}

int main() {
    char password[] = "secret";
    printf("Secure comparison\\n");
    return 0;
}`,
  
  cpp: `// Enter your C++ code here
#include <iostream>
#include <string>

class SecureString {
private:
    std::string data;
public:
    SecureString(const std::string& str) : data(str) {}
    void clear() { data.clear(); }
};

int main() {
    SecureString secure("password");
    return 0;
}`,
  
  java: `// Enter your Java code here
import java.security.MessageDigest;

public class SecurityUtils {
    public static String hashPassword(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(password.getBytes());
            return bytesToHex(hash);
        } catch (Exception e) {
            return null;
        }
    }
}`,
  
  go: `// Enter your Go code here
package main

import (
    "crypto/sha256"
    "fmt"
)

func hashPassword(password string) string {
    hash := sha256.Sum256([]byte(password))
    return fmt.Sprintf("%x", hash)
}

func main() {
    hashed := hashPassword("mypassword")
    fmt.Println("Hash:", hashed)
}`,
  
  rust: `// Enter your Rust code here
use sha2::{Sha256, Digest};

fn hash_password(password: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(password.as_bytes());
    format!("{:x}", hasher.finalize())
}

fn main() {
    let hashed = hash_password("mypassword");
    println!("Hash: {}", hashed);
}`
};

export default function CyberSecAnalyzer() {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [feedback, setFeedback] = useState<FeedbackData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeCode = async () => {
    if (!code.trim()) return;

    setIsLoading(true);
    setError(null);
    setFeedback(null);

    try {
      const response = await fetch('http://localhost:4000/api/ai/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          prompt: `Analyze this ${language} code for security vulnerabilities and best practices:\n\n${code}` 
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.message || 'Analysis failed');
      }
      
      setFeedback(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLanguageChange = (newLanguage: string) => {
    setLanguage(newLanguage);
    if (!code.trim()) {
      setCode(placeholderCode[newLanguage as keyof typeof placeholderCode] || '');
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 matrix-bg">
      {/* Header */}
      <div className="border-b border-green-500/30 bg-gray-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center space-x-4">
            <div className="text-2xl">🛡️</div>
            <div>
              <h1 className="text-2xl font-bold text-green-400 cyber-glow">
                CyberSec Code Analyzer
              </h1>
              <p className="text-green-300/70 text-sm">
                AI-Powered Security Code Review System
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-8 max-w-7xl">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Code Input Section */}
          <div className="space-y-6">
            <div className="cyber-card">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                  <h2 className="text-xl font-semibold text-green-400">
                    ENTER CODE
                  </h2>
                </div>
                
                {/* Language Selector */}
                <div className="flex items-center space-x-3">
                  <label className="text-sm font-medium text-green-300">
                    LANG:
                  </label>
                  <select
                    value={language}
                    onChange={(e) => handleLanguageChange(e.target.value)}
                    className="cyber-select"
                  >
                    {languages.map((lang) => (
                      <option key={lang.value} value={lang.value}>
                        {lang.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Code Textarea */}
              <textarea
                className="cyber-input h-80 md:h-96"
                placeholder={placeholderCode[language as keyof typeof placeholderCode]}
                value={code}
                onChange={(e) => setCode(e.target.value)}
                spellCheck={false}
              />

              {/* Stats and Action */}
              <div className="flex items-center justify-between mt-4">
                <div className="text-sm text-green-300/70 font-mono">
                  CHARS: {code.length} | LINES: {code.split('\n').length} | LANG: {language.toUpperCase()}
                </div>
                
                <button
                  onClick={analyzeCode}
                  disabled={!code.trim() || isLoading}
                  className="cyber-button disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center space-x-2"
                >
                  {isLoading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin"></div>
                      <span>ANALYZING...</span>
                    </>
                  ) : (
                    <>
                      <span>🔍</span>
                      <span>ANALYZE CODE</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Output Section */}
          <div className="space-y-6">
            <div className="cyber-card">
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                <h2 className="text-xl font-semibold text-green-400">
                  OUTPUT
                </h2>
              </div>

              {/* Loading State */}
              {isLoading && (
                <div className="text-center py-12">
                  <div className="inline-flex items-center justify-center w-16 h-16 border-2 border-green-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                  <h3 className="text-lg font-semibold text-green-400 mb-2">
                    SCANNING CODE...
                  </h3>
                  <p className="text-green-300/70 font-mono text-sm">
                    AI SECURITY ANALYSIS IN PROGRESS
                  </p>
                  <div className="mt-4 flex justify-center space-x-1">
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-green-500 rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              )}

              {/* Error State */}
              {error && (
                <div className="bg-red-950/50 border border-red-500/50 rounded-lg p-6">
                  <div className="flex items-center mb-4">
                    <div className="text-2xl mr-3">⚠️</div>
                    <h3 className="text-lg font-semibold text-red-400">
                      ANALYSIS FAILED
                    </h3>
                  </div>
                  <p className="text-red-300 font-mono text-sm">{error}</p>
                  <div className="mt-4 text-xs text-red-400/70">
                    ERROR_CODE: ANALYSIS_FAILURE | TIMESTAMP: {new Date().toISOString()}
                  </div>
                </div>
              )}

              {/* Success State */}
              {feedback && !isLoading && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-green-400 font-semibold">ANALYSIS COMPLETE</span>
                    </div>
                    <div className="text-xs text-green-300/70 font-mono">
                      TIMESTAMP: {new Date().toLocaleTimeString()}
                    </div>
                  </div>
                  
                  <div className="bg-gray-950/50 border border-green-500/30 rounded-lg p-4">
                    <div className="text-sm text-green-300 mb-2 font-mono">
                      AI_FEEDBACK_OUTPUT:
                    </div>
                    <pre className="text-green-400 text-sm leading-relaxed whitespace-pre-wrap font-mono">
                      {feedback.feedback}
                    </pre>
                  </div>
                  
                  <div className="text-xs text-green-300/50 font-mono">
                    STATUS: SUCCESS | PROVIDER: {feedback.feedback.includes('Mock') ? 'MOCK_AI' : 'OLLAMA_AI'} | LANG: {language.toUpperCase()}
                  </div>
                </div>
              )}

              {/* Default State */}
              {!feedback && !isLoading && !error && (
                <div className="text-center py-12">
                  <div className="text-6xl mb-4">🤖</div>
                  <h3 className="text-lg font-semibold text-green-400 mb-2">
                    READY FOR ANALYSIS
                  </h3>
                  <p className="text-green-300/70 font-mono text-sm">
                    ENTER CODE AND CLICK ANALYZE TO BEGIN SECURITY SCAN
                  </p>
                  <div className="mt-6 grid grid-cols-2 gap-4 text-xs text-green-300/50">
                    <div>✓ VULNERABILITY DETECTION</div>
                    <div>✓ BEST PRACTICES CHECK</div>
                    <div>✓ CODE QUALITY ANALYSIS</div>
                    <div>✓ SECURITY RECOMMENDATIONS</div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-12 text-center">
          <div className="inline-flex items-center space-x-4 text-green-300/50 text-sm font-mono">
            <div>🛡️ SECURE</div>
            <div>•</div>
            <div>🔒 ENCRYPTED</div>
            <div>•</div>
            <div>⚡ FAST</div>
            <div>•</div>
            <div>🤖 AI-POWERED</div>
          </div>
          <div className="mt-2 text-xs text-green-300/30">
            CyberSec Code Analyzer v1.0 | Powered by AI Security Intelligence
          </div>
        </div>
      </div>
    </div>
  );
}
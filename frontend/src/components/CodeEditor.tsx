/**
 * CodeEditor Component
 * 
 * Provides a large code input area with language selection
 * Features:
 * - Monospace font (JetBrains Mono)
 * - Language selector for Python, C, C++, JavaScript
 * - Dark mode styling with proper contrast
 * - Responsive design
 */

interface CodeEditorProps {
  code: string;
  setCode: (code: string) => void;
  language: string;
  setLanguage: (language: string) => void;
  onAnalyze: () => void;
  isLoading: boolean;
}

const languages = [
  { value: 'python', label: 'Python' },
  { value: 'c', label: 'C' },
  { value: 'cpp', label: 'C++' },
  { value: 'javascript', label: 'JavaScript' },
];

export default function CodeEditor({ 
  code, 
  setCode, 
  language, 
  setLanguage, 
  onAnalyze, 
  isLoading 
}: CodeEditorProps) {
  return (
    <div className="card mb-8">
      {/* Header with language selector */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
        <h2 className="text-xl font-semibold text-white mb-4 sm:mb-0">
          Code Input
        </h2>
        
        <div className="flex items-center space-x-4">
          <label htmlFor="language" className="text-sm font-medium text-zinc-300">
            Language:
          </label>
          <select
            id="language"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-zinc-800 border border-zinc-700 text-white px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {languages.map((lang) => (
              <option key={lang.value} value={lang.value}>
                {lang.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Code textarea */}
      <textarea
        className="code-editor h-64 md:h-80"
        placeholder={`// Paste your ${language} code here...
// Example:
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}`}
        value={code}
        onChange={(e) => setCode(e.target.value)}
        spellCheck={false}
      />

      {/* Action buttons */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mt-6">
        <div className="text-sm text-zinc-400 mb-4 sm:mb-0">
          {code.length} characters • {code.split('\n').length} lines
        </div>
        
        <button
          onClick={onAnalyze}
          disabled={!code.trim() || isLoading}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
        >
          {isLoading ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing...
            </>
          ) : (
            'Analyze Code'
          )}
        </button>
      </div>
    </div>
  );
}
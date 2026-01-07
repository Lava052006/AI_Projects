/**
 * FeedbackCard Component
 * 
 * Displays AI feedback results in a clean, organized format
 * Features:
 * - Overall score (0-10) with visual indicator
 * - Strengths list with positive styling
 * - Improvements list with constructive styling
 * - Suggested code improvements in formatted code blocks
 * - Loading and error states
 */

interface FeedbackData {
  score: number;
  strengths: string[];
  improvements: string[];
  suggestedCode?: string;
}

interface FeedbackCardProps {
  feedback: FeedbackData | null;
  isLoading: boolean;
  error: string | null;
}

export default function FeedbackCard({ feedback, isLoading, error }: FeedbackCardProps) {
  // Loading state
  if (isLoading) {
    return (
      <div className="card text-center py-12">
        <div className="flex items-center justify-center mb-4">
          <svg className="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
        <h3 className="text-xl font-semibold text-white mb-2">
          Analyzing your code...
        </h3>
        <p className="text-zinc-400">
          This may take a few moments
        </p>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="error-card">
        <div className="flex items-center mb-4">
          <svg className="h-6 w-6 text-red-400 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 className="text-lg font-semibold text-red-200">
            Analysis Failed
          </h3>
        </div>
        <p className="text-red-300">{error}</p>
      </div>
    );
  }

  // No feedback yet
  if (!feedback) {
    return (
      <div className="card text-center py-12">
        <div className="text-6xl mb-4">🤖</div>
        <h3 className="text-xl font-semibold text-white mb-2">
          Ready to analyze your code
        </h3>
        <p className="text-zinc-400">
          Paste your code above and click "Analyze Code" to get started
        </p>
      </div>
    );
  }

  // Success state with feedback
  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-400';
    if (score >= 6) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getScoreBg = (score: number) => {
    if (score >= 8) return 'bg-green-500/20 border-green-500/30';
    if (score >= 6) return 'bg-yellow-500/20 border-yellow-500/30';
    return 'bg-red-500/20 border-red-500/30';
  };

  return (
    <div className="space-y-6">
      {/* Overall Score */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-semibold text-white">Overall Score</h3>
          <div className={`px-4 py-2 rounded-lg border ${getScoreBg(feedback.score)}`}>
            <span className={`text-2xl font-bold ${getScoreColor(feedback.score)}`}>
              {feedback.score}/10
            </span>
          </div>
        </div>
        
        {/* Score bar */}
        <div className="w-full bg-zinc-800 rounded-full h-3">
          <div 
            className={`h-3 rounded-full transition-all duration-1000 ${
              feedback.score >= 8 ? 'bg-green-500' : 
              feedback.score >= 6 ? 'bg-yellow-500' : 'bg-red-500'
            }`}
            style={{ width: `${(feedback.score / 10) * 100}%` }}
          />
        </div>
      </div>

      {/* Strengths */}
      {feedback.strengths.length > 0 && (
        <div className="card">
          <div className="flex items-center mb-4">
            <svg className="h-6 w-6 text-green-400 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 className="text-xl font-semibold text-white">
              Strengths ({feedback.strengths.length})
            </h3>
          </div>
          <ul className="space-y-2">
            {feedback.strengths.map((strength, index) => (
              <li key={index} className="flex items-start">
                <span className="text-green-400 mr-3 mt-1">•</span>
                <span className="text-zinc-300">{strength}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Improvements */}
      {feedback.improvements.length > 0 && (
        <div className="card">
          <div className="flex items-center mb-4">
            <svg className="h-6 w-6 text-blue-400 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <h3 className="text-xl font-semibold text-white">
              Improvements ({feedback.improvements.length})
            </h3>
          </div>
          <ul className="space-y-2">
            {feedback.improvements.map((improvement, index) => (
              <li key={index} className="flex items-start">
                <span className="text-blue-400 mr-3 mt-1">•</span>
                <span className="text-zinc-300">{improvement}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Suggested Code */}
      {feedback.suggestedCode && (
        <div className="card">
          <div className="flex items-center mb-4">
            <svg className="h-6 w-6 text-purple-400 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
            <h3 className="text-xl font-semibold text-white">
              Suggested Improvements
            </h3>
          </div>
          <pre className="bg-zinc-950 border border-zinc-800 rounded-lg p-4 overflow-x-auto">
            <code className="text-sm font-mono text-zinc-300">
              {feedback.suggestedCode}
            </code>
          </pre>
        </div>
      )}
    </div>
  );
}
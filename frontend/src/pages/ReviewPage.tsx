import { useState } from "react";

export default function ReviewPage() {
  const [code, setCode] = useState("");

  return (
    <div className="min-h-screen p-8 bg-base-100">
      <h1 className="text-3xl font-bold mb-6">Code Review</h1>

      <textarea
        className="textarea textarea-bordered w-full h-60 font-mono"
        placeholder="Paste your Python code here..."
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />

      <div className="mt-4">
        <button className="btn btn-primary">
          Analyze Code
        </button>
      </div>

      {/* Feedback */}
      <div className="card bg-base-200 shadow-xl mt-8">
        <div className="card-body">
          <h2 className="card-title">AI Feedback</h2>
          <p><strong>Score:</strong> 8/10</p>
          <p><strong>Strengths:</strong> Clean and readable logic.</p>
          <p><strong>Improvements:</strong> Add type hints.</p>
        </div>
      </div>
    </div>
  );
}

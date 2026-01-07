export default function LandingPage() {
  return (
    <div className="min-h-screen bg-base-100">
      <div className="hero min-h-screen">
        <div className="hero-content text-center">
          <div className="max-w-2xl">
            <h1 className="text-5xl font-bold">
              AI Code Mentor
            </h1>
            <p className="py-6 text-lg opacity-80">
              Get instant AI-powered feedback on your code.
              Built for learning, hackathons, and growth.
            </p>

            <div className="flex justify-center gap-4">
              <button className="btn btn-primary btn-lg">
                Try Now
              </button>
              <button className="btn btn-outline btn-lg">
                Learn More
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 px-8 pb-16">
        <div className="card bg-base-200 shadow-xl">
          <div className="card-body">
            <h2 className="card-title">AI Feedback</h2>
            <p>Structured, short, actionable feedback.</p>
          </div>
        </div>

        <div className="card bg-base-200 shadow-xl">
          <div className="card-body">
            <h2 className="card-title">Auto Grading</h2>
            <p>Score code quality instantly.</p>
          </div>
        </div>

        <div className="card bg-base-200 shadow-xl">
          <div className="card-body">
            <h2 className="card-title">Hackathon Ready</h2>
            <p>Fast, clean, and impressive UI.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

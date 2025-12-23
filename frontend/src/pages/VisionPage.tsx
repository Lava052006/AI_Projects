export default function Dashboard() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

      <div className="stats shadow bg-base-200">
        <div className="stat">
          <div className="stat-title">Submissions</div>
          <div className="stat-value">12</div>
        </div>

        <div className="stat">
          <div className="stat-title">Average Score</div>
          <div className="stat-value text-primary">82%</div>
        </div>

        <div className="stat">
          <div className="stat-title">XP</div>
          <div className="stat-value">1,240</div>
        </div>
      </div>
    </div>
  );
}

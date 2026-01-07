export default function Navbar() {
  return (
    <div className="navbar bg-base-200">
      <div className="flex-1">
        <a className="btn btn-ghost text-xl">
          AI Mentor
        </a>
      </div>
      <div className="flex gap-2">
        <button className="btn btn-sm btn-outline">
          Dashboard
        </button>
        <button className="btn btn-sm btn-primary">
          Review
        </button>
      </div>
    </div>
  );
}

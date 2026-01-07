/**
 * Header Component
 * 
 * Displays the main project title and subtitle for CodeSense AI
 * Uses clean typography with proper contrast for dark mode
 */

export default function Header() {
  return (
    <header className="text-center mb-12">
      <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
        CodeSense AI
      </h1>
      <p className="text-xl text-zinc-400 max-w-2xl mx-auto">
        Instant AI feedback on your code
      </p>
    </header>
  );
}
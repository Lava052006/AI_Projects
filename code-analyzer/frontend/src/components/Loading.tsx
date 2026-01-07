import { motion } from "framer-motion";
import { Brain, Loader2 } from "lucide-react";

interface LoadingProps {
  message?: string;
  size?: "sm" | "md" | "lg";
}

export default function Loading({ message = "Loading...", size = "md" }: LoadingProps) {


  const containerClasses = {
    sm: "p-4",
    md: "p-8",
    lg: "p-12"
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      className={`flex flex-col items-center justify-center ${containerClasses[size]}`}
    >
      <div className="relative mb-4">
        {/* Outer spinning ring */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="w-16 h-16 border-2 border-primary-500/20 border-t-primary-500 rounded-full"
        />
        
        {/* Inner brain icon */}
        <div className="absolute inset-0 flex items-center justify-center">
          <motion.div
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
          >
            <Brain className="w-6 h-6 text-primary-400" />
          </motion.div>
        </div>
      </div>
      
      <motion.p
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
        className="text-gray-300 text-sm font-medium"
      >
        {message}
      </motion.p>
    </motion.div>
  );
}

// Simple inline loader for buttons
export function ButtonLoader({ className = "w-4 h-4" }: { className?: string }) {
  return (
    <Loader2 className={`animate-spin ${className}`} />
  );
}

// Full screen loading overlay
export function LoadingOverlay({ message }: { message?: string }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center z-50"
    >
      <div className="card max-w-sm mx-4">
        <Loading message={message} size="lg" />
      </div>
    </motion.div>
  );
}
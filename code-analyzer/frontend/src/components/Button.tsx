import { motion } from "framer-motion";
import type { ReactNode } from "react";
import { ButtonLoader } from "./Loading";

interface ButtonProps {
  children: ReactNode;
  variant?: "primary" | "secondary" | "outline" | "ghost";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  className?: string;
  icon?: ReactNode;
}

export default function Button({
  children,
  variant = "primary",
  size = "md",
  loading = false,
  disabled = false,
  onClick,
  type = "button",
  className = "",
  icon
}: ButtonProps) {
  const baseClasses = "inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-300 focus:outline-none focus:ring-4 transform hover:scale-105 disabled:hover:scale-100 disabled:opacity-50 disabled:cursor-not-allowed active:scale-95";
  
  const variantClasses = {
    primary: "btn-primary",
    secondary: "btn-secondary", 
    outline: "btn-outline",
    ghost: "text-gray-300 hover:text-white hover:bg-slate-700/50 focus:ring-slate-500/50 px-4 py-2 rounded-xl transition-all duration-300"
  };
  
  const sizeClasses = {
    sm: "px-4 py-2 text-sm space-x-1",
    md: "px-6 py-3 text-base space-x-2",
    lg: "px-8 py-4 text-lg space-x-3"
  };

  const isDisabled = disabled || loading;

  return (
    <motion.button
      whileHover={!isDisabled ? { scale: 1.05 } : {}}
      whileTap={!isDisabled ? { scale: 0.95 } : {}}
      type={type}
      onClick={onClick}
      disabled={isDisabled}
      className={`${baseClasses} ${variantClasses[variant]} ${variant !== 'primary' && variant !== 'secondary' && variant !== 'outline' ? sizeClasses[size] : ''} ${className}`}
    >
      {loading ? (
        <>
          <ButtonLoader />
          <span>Loading...</span>
        </>
      ) : (
        <>
          {icon && <span>{icon}</span>}
          <span>{children}</span>
        </>
      )}
    </motion.button>
  );
}
import React from 'react';

interface ButtonProps {
  onClick: () => void;
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
}

export const Button: React.FC<ButtonProps> = ({ onClick, children, variant = 'primary' }) => {
  const baseStyle = "px-4 py-2 rounded-md font-semibold";
  const variantStyle = variant === 'primary'
    ? "bg-blue-500 text-white hover:bg-blue-600"
    : "bg-gray-200 text-gray-800 hover:bg-gray-300";

  return (
    <button
      className={`${baseStyle} ${variantStyle}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};

import React from 'react';

interface ButtonProps {
  onClick: () => void;
  label: string;
  disabled?: boolean;
  primary?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  onClick,
  label,
  disabled = false,
  primary = false,
}) => {
  const baseStyle = "px-4 py-2 rounded-md font-semibold";
  const primaryStyle = primary ? "bg-blue-500 text-white hover:bg-blue-600" : "bg-gray-200 text-gray-800 hover:bg-gray-300";
  const disabledStyle = disabled ? "opacity-50 cursor-not-allowed" : "";

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`${baseStyle} ${primaryStyle} ${disabledStyle}`.trim()}
    >
      {label}
    </button>
  );
};

export default Button;

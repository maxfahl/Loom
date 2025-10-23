import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from '../../../../../../examples/typescript/react-component/src/components/Button';

describe('Button', () => {
  it('renders with the correct label', () => {
    render(<Button onClick={() => {}} label="Click Me" />);
    expect(screen.getByText("Click Me")).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick} label="Click Me" />);
    fireEvent.click(screen.getByText("Click Me"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick} label="Click Me" disabled />);
    const button = screen.getByText("Click Me");
    expect(button).toBeDisabled();
    fireEvent.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('applies primary styling when primary prop is true', () => {
    render(<Button onClick={() => {}} label="Primary Button" primary />);
    const button = screen.getByText("Primary Button");
    expect(button).toHaveClass("bg-blue-500");
    expect(button).toHaveClass("text-white");
  });

  it('applies default styling when primary prop is false', () => {
    render(<Button onClick={() => {}} label="Default Button" primary={false} />);
    const button = screen.getByText("Default Button");
    expect(button).toHaveClass("bg-gray-200");
    expect(button).toHaveClass("text-gray-800");
  });
});

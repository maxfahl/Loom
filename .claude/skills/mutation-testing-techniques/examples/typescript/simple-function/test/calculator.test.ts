import { add, subtract, multiply, divide } from '../../../../../examples/typescript/simple-function/src/calculator';

describe('Calculator', () => {
  describe('add', () => {
    it('should return the sum of two numbers', () => {
      expect(add(1, 2)).toBe(3);
      expect(add(-1, 1)).toBe(0);
      expect(add(-1, -2)).toBe(-3);
      expect(add(0, 0)).toBe(0);
    });
  });

  describe('subtract', () => {
    it('should return the difference of two numbers', () => {
      expect(subtract(5, 2)).toBe(3);
      expect(subtract(2, 5)).toBe(-3);
      expect(subtract(0, 0)).toBe(0);
    });
  });

  describe('multiply', () => {
    it('should return the product of two numbers', () => {
      expect(multiply(2, 3)).toBe(6);
      expect(multiply(-2, 3)).toBe(-6);
      expect(multiply(0, 5)).toBe(0);
    });
  });

  describe('divide', () => {
    it('should return the quotient of two numbers', () => {
      expect(divide(6, 3)).toBe(2);
      expect(divide(10, 2)).toBe(5);
    });

    it('should throw an error when dividing by zero', () => {
      expect(() => divide(1, 0)).toThrow("Cannot divide by zero");
    });
  });
});

import { useState, useCallback } from 'react';

/**
 * @function useToggle
 * @description A custom React hook to manage a boolean state, providing a toggle function.
 * @param {boolean} initialValue - The initial boolean value for the toggle.
 * @returns {[boolean, () => void]} A tuple containing the current boolean value and a toggle function.
 * @example
 * const [isOn, toggle] = useToggle(false);
 * // ...
 * <button onClick={toggle}>{isOn ? 'ON' : 'OFF'}</button>
 */
export function useToggle(initialValue: boolean = false): [boolean, () => void] {
  const [value, setValue] = useState<boolean>(initialValue);

  const toggle = useCallback(() => {
    setValue(prevValue => !prevValue);
  }, []); // No dependencies, so `toggle` function is stable

  return [value, toggle];
}

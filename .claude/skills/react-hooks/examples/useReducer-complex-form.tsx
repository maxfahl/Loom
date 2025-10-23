import React, { useReducer } from 'react';

// 1. Define State and Action Types
interface FormState {
  firstName: string;
  lastName: string;
  email: string;
  age: number;
  newsletter: boolean;
}

type FormAction =
  | { type: 'SET_FIELD'; field: keyof FormState; value: any }
  | { type: 'RESET_FORM' };

// 2. Define Initial State
const initialFormState: FormState = {
  firstName: '',
  lastName: '',
  email: '',
  age: 0,
  newsletter: false,
};

// 3. Create the Reducer Function
function formReducer(state: FormState, action: FormAction): FormState {
  switch (action.type) {
    case 'SET_FIELD':
      return { ...state, [action.field]: action.value };
    case 'RESET_FORM':
      return initialFormState;
    default:
      return state;
  }
}

/**
 * @function UseReducerComplexForm
 * @description Demonstrates `useReducer` for managing complex form state.
 */
const UseReducerComplexForm: React.FC = () => {
  const [state, dispatch] = useReducer(formReducer, initialFormState);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    dispatch({
      type: 'SET_FIELD',
      field: name as keyof FormState,
      value: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form Submitted:', state);
    alert('Form Submitted! Check console for data.');
  };

  const handleReset = () => {
    dispatch({ type: 'RESET_FORM' });
  };

  return (
    <div>
      <h2>useReducer Example: Complex Form</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>First Name:</label>
          <input
            type="text"
            name="firstName"
            value={state.firstName}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Last Name:</label>
          <input
            type="text"
            name="lastName"
            value={state.lastName}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={state.email}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>Age:</label>
          <input
            type="number"
            name="age"
            value={state.age}
            onChange={handleChange}
          />
        </div>
        <div>
          <label>
            <input
              type="checkbox"
              name="newsletter"
              checked={state.newsletter}
              onChange={handleChange}
            />
            Subscribe to Newsletter
          </label>
        </div>
        <button type="submit">Submit</button>
        <button type="button" onClick={handleReset}>Reset</button>
      </form>

      <h3>Current Form State:</h3>
      <pre>{JSON.stringify(state, null, 2)}</pre>
    </div>
  );
};

export default UseReducerComplexForm;

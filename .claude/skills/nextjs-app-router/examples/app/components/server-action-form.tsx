"use client";

import React, { useState } from 'react';
import { submitFormAction } from '../actions/form-actions';

export default function ServerActionForm() {
  const [message, setMessage] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (formData: FormData) => {
    setIsSubmitting(true);
    const result = await submitFormAction(formData);
    setMessage(result.message);
    setIsSubmitting(false);
  };

  return (
    <div>
      <h1>Server Action Form</h1>
      <form action={handleSubmit}>
        <div>
          <label htmlFor="name">Name:</label>
          <input type="text" id="name" name="name" required />
        </div>
        <div>
          <label htmlFor="email">Email:</label>
          <input type="email" id="email" name="email" required />
        </div>
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Submitting...' : 'Submit'}
        </button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

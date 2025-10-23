# Good Example: Atomic Commit

## Scenario
You're adding a new feature to validate user email addresses.

## The RIGHT Way: Atomic Commits

### Commit 1: Add email validation utility
```bash
git add src/utils/email-validator.ts tests/utils/email-validator.test.ts
git commit -m "feat: Add email validation utility with RFC 5322 compliance"
```

**Files changed:**
- `src/utils/email-validator.ts` (new)
- `tests/utils/email-validator.test.ts` (new)

**Why it's atomic:**
- Single purpose: Add email validation
- Complete: Implementation + tests work together
- Minimal: Only includes validation logic
- Testable: All tests pass independently

**Code:**
```typescript
// src/utils/email-validator.ts
export interface EmailValidationResult {
  isValid: boolean;
  errors: string[];
}

export function validateEmail(email: string): EmailValidationResult {
  const errors: string[] = [];

  if (!email) {
    return { isValid: false, errors: ['Email is required'] };
  }

  // Basic RFC 5322 pattern
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!emailPattern.test(email)) {
    errors.push('Invalid email format');
  }

  if (email.length > 254) {
    errors.push('Email exceeds maximum length of 254 characters');
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}
```

```typescript
// tests/utils/email-validator.test.ts
import { validateEmail } from '@/utils/email-validator';

describe('validateEmail', () => {
  it('should validate correct email addresses', () => {
    const result = validateEmail('user@example.com');
    expect(result.isValid).toBe(true);
    expect(result.errors).toHaveLength(0);
  });

  it('should reject empty email', () => {
    const result = validateEmail('');
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain('Email is required');
  });

  it('should reject invalid format', () => {
    const result = validateEmail('not-an-email');
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain('Invalid email format');
  });

  it('should reject emails exceeding max length', () => {
    const longEmail = 'a'.repeat(250) + '@example.com';
    const result = validateEmail(longEmail);
    expect(result.isValid).toBe(false);
  });
});
```

---

### Commit 2: Integrate email validation in registration form
```bash
git add src/components/RegistrationForm.tsx
git commit -m "feat: Add email validation to registration form"
```

**Files changed:**
- `src/components/RegistrationForm.tsx` (modified)

**Why it's atomic:**
- Single purpose: Use the validator in the form
- Complete: Form now validates emails properly
- Minimal: Only touches the registration form
- Depends on: Previous commit (validator exists)

**Code:**
```typescript
// src/components/RegistrationForm.tsx
import { useState } from 'react';
import { validateEmail } from '@/utils/email-validator';

export function RegistrationForm() {
  const [email, setEmail] = useState('');
  const [emailErrors, setEmailErrors] = useState<string[]>([]);

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setEmail(value);

    // Validate on change
    const validation = validateEmail(value);
    setEmailErrors(validation.errors);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const validation = validateEmail(email);
    if (!validation.isValid) {
      setEmailErrors(validation.errors);
      return;
    }

    // Proceed with registration...
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        value={email}
        onChange={handleEmailChange}
        aria-invalid={emailErrors.length > 0}
      />

      {emailErrors.length > 0 && (
        <div role="alert" className="errors">
          {emailErrors.map(error => (
            <p key={error}>{error}</p>
          ))}
        </div>
      )}

      <button type="submit">Register</button>
    </form>
  );
}
```

---

### Commit 3: Document email validation in README
```bash
git add README.md
git commit -m "docs: Document email validation feature"
```

**Files changed:**
- `README.md` (modified)

**Why it's atomic:**
- Single purpose: Document the feature
- Complete: Docs are comprehensive
- Minimal: Only touches documentation
- Separate from: Implementation (different concern)

**Changes:**
```markdown
## Email Validation

The application includes RFC 5322 compliant email validation.

### Usage

```typescript
import { validateEmail } from '@/utils/email-validator';

const result = validateEmail('user@example.com');
if (result.isValid) {
  // Email is valid
} else {
  // Handle errors: result.errors
}
```

### Features

- RFC 5322 compliance
- Maximum length validation (254 characters)
- Clear error messages
- Type-safe API
```

---

## Summary

**Why this approach works:**

1. **Clear narrative**: Story flows logically
   - First: Create the utility
   - Second: Use the utility
   - Third: Document the feature

2. **Easy review**: Each commit is small and focused
   - Reviewer can approve validator independently
   - Form integration can be reviewed separately
   - Docs are trivial to approve

3. **Safe revert**: Can roll back any piece
   - Remove form integration but keep validator
   - Remove validator (after removing form integration)
   - Update docs independently

4. **Better debugging**: Each commit compiles and tests pass
   - Can use `git bisect` effectively
   - Can identify exactly when a bug was introduced

5. **Flexible workflow**: Can cherry-pick commits
   - Want just the validator? Cherry-pick commit 1
   - Want to reorder? Easy with clean history

import argparse
import os
import re

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def generate_custom_error(error_name, error_code, error_message):
    camel_name = error_name
    lower_name = error_name.lower()

    content = f"""package errors

import (
	"fmt"
	"errors"
)

// {camel_name} represents a custom error type for {lower_name} scenarios.
type {camel_name} struct {{
	Code    int    `json:"code"`
	Message string `json:"message"`
	Err     error  `json:"-"` // Original error, if wrapped
}}

// New{camel_name} creates a new {camel_name} error.
func New{camel_name}(msg string, errs ...error) *{camel_name} {{
	var wrappedErr error
	if len(errs) > 0 && errs[0] != nil {{
		wrappedErr = errs[0]
	}}
	return &{camel_name}{{
		Code:    {error_code},
		Message: msg,
		Err:     wrappedErr,
	}}
}}

// Error implements the error interface.
func (e *{camel_name}) Error() string {{
	if e.Err != nil {{
		return fmt.Sprintf("{camel_name}: %s: %v", e.Message, e.Err)
	}}
	return fmt.Sprintf("{camel_name}: %s", e.Message)
}}

// Unwrap provides compatibility for Go 1.13 error chains.
func (e *{camel_name}) Unwrap() error {{
	return e.Err
}}

// Is checks if the target error is of type {camel_name}.
func (e *{camel_name}) Is(target error) bool {{
	var t *{camel_name}
	return errors.As(target, &t)
}}

// As checks if the target error can be unwrapped to {camel_name}.
func (e *{camel_name}) As(target interface{{}}) bool {{
	_, ok := target.(*{camel_name})
	return ok
}}

// Example usage:
// var ErrInvalidInput = New{camel_name}("{error_message}")
"""
    return content

def main():
    parser = argparse.ArgumentParser(
        description="Generate a custom Go error type with wrapping, Is, and As methods.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--name", required=True,
                        help="The name of the error type (e.g., ValidationError, NotFoundError). Should be in CamelCase.")
    parser.add_argument("--code", type=int, default=500,
                        help="The error code (e.g., HTTP status code or custom code).")
    parser.add_argument("--message", default="An unexpected error occurred.",
                        help="A default message for the error type.")
    parser.add_argument("--file-path",
                        help="Optional. The output file path (e.g., internal/errors/validation_error.go). "
                             "If not provided, defaults to internal/errors/<snake_case_name>_error.go.")

    args = parser.parse_args()

    error_name = args.name
    error_code = args.code
    error_message = args.message
    output_file_path = args.file_path

    if not re.match(r'^[A-Z][a-zA-Z0-9]*Error$', error_name):
        print(f"Error: Error name '{error_name}' must be in CamelCase and end with 'Error' (e.g., ValidationError).")
        exit(1)

    if not output_file_path:
        output_dir = os.path.join("internal", "errors")
        os.makedirs(output_dir, exist_ok=True)
        output_file_path = os.path.join(output_dir, f"{to_snake_case(error_name)}_error.go")

    content = generate_custom_error(error_name, error_code, error_message)

    with open(output_file_path, "w") as f:
        f.write(content)
    print(f"Successfully generated custom error type '{error_name}' at: {output_file_path}")

if __name__ == "__main__":
    main()
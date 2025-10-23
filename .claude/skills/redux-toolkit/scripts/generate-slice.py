import argparse
import os
import re

def to_camel_case(snake_str):
    components = snake_str.split('-')
    return components[0] + ''.join(x.title() for x in components[1:])

def to_pascal_case(snake_str):
    return ''.join(x.title() for x in snake_str.split('-'))

def generate_slice_file(slice_name, output_dir, async_thunk=False):
    camel_slice_name = to_camel_case(slice_name)
    pascal_slice_name = to_pascal_case(slice_name)

    file_content = f"""import {{ createSlice, PayloadAction{', createAsyncThunk' if async_thunk else ''} }} from '@reduxjs/toolkit';

interface {pascal_slice_name}State {{
  // Define your slice state interface here
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
  // Example: data: any[];
}}

const initialState: {pascal_slice_name}State = {{
  status: 'idle',
  error: null,
  // Example: data: [],
}};

{f'''// Async thunk example
export const fetch{pascal_slice_name} = createAsyncThunk(
  '{camel_slice_name}/fetch{pascal_slice_name}',
  async (_, {{ rejectWithValue }}) => {{
    try {{
      // Perform your async operation here, e.g., API call
      const response = await fetch('/api/{camel_slice_name}');
      if (!response.ok) {{
        throw new Error('Failed to fetch {camel_slice_name}');
      }}
      const data = await response.json();
      return data; // This will be the action.payload in fulfilled
    }} catch (error: any) {{
      return rejectWithValue(error.message);
    }}
  }}
);

''' if async_thunk else ''}export const {camel_slice_name}Slice = createSlice({{
  name: '{camel_slice_name}',
  initialState,
  reducers: {{
    // Define your synchronous reducers here
    // Example:
    // itemAdded: (state, action: PayloadAction<Item>) => {
    //   state.items.push(action.payload);
    // },
  }},
{f'''  extraReducers: (builder) => {{
    builder
      .addCase(fetch{pascal_slice_name}.pending, (state) => {{
        state.status = 'loading';
      }})
      .addCase(fetch{pascal_slice_name}.fulfilled, (state, action) => {{
        state.status = 'succeeded';
        // Handle fulfilled state, e.g., state.data = action.payload;
      }})
      .addCase(fetch{pascal_slice_name}.rejected, (state, action) => {{
        state.status = 'failed';
        state.error = action.payload as string;
      }});
  }},
''' if async_thunk else ''}});

export const {{ /* actions here */ }} = {camel_slice_name}Slice.actions;

export default {camel_slice_name}Slice.reducer;
"""

    filepath = os.path.join(output_dir, f"{camel_slice_name}Slice.ts")
    os.makedirs(output_dir, exist_ok=True)

    with open(filepath, 'w') as f:
        f.write(file_content)
    print(f"Successfully generated slice: {filepath}")

def main():
    parser = argparse.ArgumentParser(
        description="Generates a new Redux Toolkit slice file with boilerplate."
    )
    parser.add_argument(
        "name",
        help="Name of the slice (e.g., 'user-auth', 'products')."
    )
    parser.add_argument(
        "-o", "--output-dir",
        default="src/features",
        help="Output directory for the slice file. Default is 'src/features'."
    )
    parser.add_argument(
        "-a", "--async-thunk",
        action="store_true",
        help="Include boilerplate for createAsyncThunk."
    )

    args = parser.parse_args()

    # Validate slice name
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", args.name):
        print("Error: Slice name must be in kebab-case (e.g., 'user-auth', 'product-details').")
        sys.exit(1)

    slice_output_dir = os.path.join(args.output_dir, args.name)
    generate_slice_file(args.name, slice_output_dir, args.async_thunk)

if __name__ == "__main__":
    main()

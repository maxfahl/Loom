#!/usr/bin/env python3
"""
generate-adaptive-component.py: Generates boilerplate for a platform-adaptive React Native component.

This script creates a React Native component that can have different implementations
for Android (following Material Design) and iOS (following Human Interface Guidelines),
while sharing a common interface. This saves time by setting up the basic structure
and ensuring platform-specific considerations are addressed from the start.
"""

import argparse
import os
from pathlib import Path

def create_adaptive_component(component_name, output_dir):
    """
    Creates the necessary files for an adaptive React Native component.

    Args:
        component_name (str): The name of the component (e.g., "MyButton").
        output_dir (Path): The root directory where the component will be created.
    """
    component_dir = output_dir / component_name
    component_dir.mkdir(parents=True, exist_ok=True)

    # Common interface file
    interface_content = f"""import {{ ViewProps }} from 'react-native';

export interface {component_name}Props extends ViewProps {{
  title: string;
  onPress: () => void;
  // Add other common props here
}}
"""
    (component_dir / f'{component_name}.interface.ts').write_text(interface_content)

    # Android implementation (Material Design)
    android_content = f"""import React from 'react';
import {{ Platform, StyleSheet }} from 'react-native';
import {{ Button, useTheme, MD3Theme }} from 'react-native-paper'; // Assuming react-native-paper for Material 3
import {{ {component_name}Props }} from './{component_name}.interface';

const {component_name}Android: React.FC<{component_name}Props> = ({{ title, onPress, ...rest }}) => {{
  const theme = useTheme<MD3Theme>();

  return (
    <Button
      mode="contained"
      onPress={onPress}
      style={{ backgroundColor: theme.colors.primary }}
      labelStyle={{ color: theme.colors.onPrimary }}
      {{...rest}}
    >
      {{title}}
    </Button>
  );
}};

const styles = StyleSheet.create({{
  // Add Android-specific styles here if needed
}});

export default {component_name}Android;
"""
    (component_dir / f'{component_name}.android.tsx').write_text(android_content)

    # iOS implementation (Human Interface Guidelines)
    ios_content = f"""import React from 'react';
import {{ Platform, StyleSheet, TouchableOpacity, Text }} from 'react-native';
import {{ {component_name}Props }} from './{component_name}.interface';

const {component_name}IOS: React.FC<{component_name}Props> = ({{ title, onPress, ...rest }}) => {{
  return (
    <TouchableOpacity
      onPress={onPress}
      style={styles.button}
      activeOpacity={0.7}
      {{...rest}}
    >
      <Text style={styles.buttonText}>{{title}}</Text>
    </TouchableOpacity>
  );
}};

const styles = StyleSheet.create({{
  button: {{
    backgroundColor: '#007AFF', // iOS blue
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
  }},
  buttonText: {{
    color: '#FFFFFF',
    fontSize: 17,
    fontWeight: '600',
  }},
  // Add iOS-specific styles here if needed
}});

export default {component_name}IOS;
"""
    (component_dir / f'{component_name}.ios.tsx').write_text(ios_content)

    # Index file to export the correct platform-specific component
    index_content = f"""import {{ Platform }} from 'react-native';
import {{ {component_name}Props }} from './{component_name}.interface';
import {component_name}Android from './{component_name}.android';
import {component_name}IOS from './{component_name}.ios';

const {component_name}: React.FC<{component_name}Props> = Platform.select({{
  ios: {component_name}IOS,
  android: {component_name}Android,
  default: {component_name}Android, // Fallback
}});

export default {component_name};
"""
    (component_dir / 'index.ts').write_text(index_content)

    print(f"Successfully generated adaptive component '{component_name}' in '{component_dir}'")
    print(f"Files created: {component_name}.interface.ts, {component_name}.android.tsx, {component_name}.ios.tsx, index.ts")

def main():
    parser = argparse.ArgumentParser(
        description="Generate boilerplate for a platform-adaptive React Native component.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "name",
        help="The name of the component to generate (e.g., MyButton)."
    )
    parser.add_argument(
        "-o", "--output",
        default=".",
        help="Output directory for the component. Defaults to current directory."
    )
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Show what would be done without actually creating files."
    )

    args = parser.parse_args()

    component_name = args.name
    output_dir = Path(args.output)

    if args.dry_run:
        print(f"Dry run: Would create adaptive component '{component_name}' in '{output_dir / component_name}'")
        print(f"  - {component_name}.interface.ts")
        print(f"  - {component_name}.android.tsx")
        print(f"  - {component_name}.ios.tsx")
        print(f"  - index.ts")
        return

    try:
        create_adaptive_component(component_name, output_dir)
    except Exception as e:
        print(f"Error generating component: {e}")
        exit(1)

if __name__ == "__main__":
    main()

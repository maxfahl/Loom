import axios from 'axios';
import * as fs from 'fs';
import * as path from 'path';

const FIGMA_API_BASE_URL = 'https://api.figma.com/v1';

interface FigmaVariable {
  id: string;
  name: string;
  key: string;
  remote: boolean;
  variableCollectionId: string;
  resolvedType: string;
  valuesByMode: { [modeId: string]: any };
  // Add other properties as needed
}

interface FigmaVariableCollection {
  id: string;
  name: string;
  modes: Array<{ modeId: string; name: string }>;
  // Add other properties as needed
}

interface FigmaVariablesResponse {
  meta: {
    variables: FigmaVariable[];
    variableCollections: FigmaVariableCollection[];
  };
}

/**
 * Extracts Figma Design Variables from a file and converts them into a structured JSON format.
 * @param fileKey The key of the Figma file.
 * @param accessToken Your Figma Personal Access Token.
 * @param outputPath The path to save the generated JSON file.
 * @returns A Promise that resolves when the JSON file is written.
 */
async function extractFigmaVariablesToJson(
  fileKey: string,
  accessToken: string,
  outputPath: string
): Promise<void> {
  try {
    const response = await axios.get<FigmaVariablesResponse>(
      `${FIGMA_API_BASE_URL}/files/${fileKey}/variables/local`,
      {
        headers: {
          'X-Figma-Token': accessToken,
        },
      }
    );

    const { variables, variableCollections } = response.data.meta;

    const output: { [collectionName: string]: { [modeName: string]: { [variableName: string]: any } } } = {};

    variableCollections.forEach(collection => {
      output[collection.name] = {};
      collection.modes.forEach(mode => {
        output[collection.name][mode.name] = {};
      });
    });

    variables.forEach(variable => {
      const collection = variableCollections.find(col => col.id === variable.variableCollectionId);
      if (collection) {
        collection.modes.forEach(mode => {
          const value = variable.valuesByMode[mode.modeId];
          if (output[collection.name] && output[collection.name][mode.name]) {
            output[collection.name][mode.name][variable.name] = value;
          }
        });
      }
    });

    fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), 'utf-8');
    console.log(`Successfully extracted Figma variables to ${outputPath}`);
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error(`Error extracting Figma variables: ${error.message}`);
      if (error.response) {
        console.error(`Status: ${error.response.status}`);
        console.error(`Data: ${JSON.stringify(error.response.data, null, 2)}`);
      }
    } else {
      console.error('An unexpected error occurred:', error);
    }
    throw error;
  }
}

// Example Usage (replace with your actual file key and token)
const MY_FIGMA_FILE_KEY = 'YOUR_FILE_KEY'; // e.g., 'abcd1234567890'
const MY_FIGMA_ACCESS_TOKEN = 'YOUR_PERSONAL_ACCESS_TOKEN'; // e.g., 'figd_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
const OUTPUT_FILE_PATH = path.join(__dirname, 'figma-variables.json');

if (MY_FIGMA_FILE_KEY === 'YOUR_FILE_KEY' || MY_FIGMA_ACCESS_TOKEN === 'YOUR_PERSONAL_ACCESS_TOKEN') {
  console.warn('Please replace YOUR_FILE_KEY and YOUR_PERSONAL_ACCESS_TOKEN with actual values.');
} else {
  extractFigmaVariablesToJson(MY_FIGMA_FILE_KEY, MY_FIGMA_ACCESS_TOKEN, OUTPUT_FILE_PATH)
    .catch((error) => {
      console.error('Failed to extract Figma variables:', error.message);
    });
}

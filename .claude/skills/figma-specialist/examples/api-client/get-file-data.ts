import axios from 'axios';

const FIGMA_API_BASE_URL = 'https://api.figma.com/v1';

interface FigmaFileResponse {
  name: string;
  lastModified: string;
  thumbnailUrl: string;
  version: string;
  document: {
    id: string;
    name: string;
    type: string;
    children: any[]; // Simplified for example
  };
  components: { [key: string]: any }; // Simplified
  componentSets: { [key: string]: any }; // Simplified
  styles: { [key: string]: any }; // Simplified
}

/**
 * Fetches the content of a Figma file.
 * @param fileKey The key of the Figma file.
 * @param accessToken Your Figma Personal Access Token.
 * @returns A Promise that resolves to the Figma file data.
 */
async function getFigmaFileData(fileKey: string, accessToken: string): Promise<FigmaFileResponse> {
  try {
    const response = await axios.get<FigmaFileResponse>(
      `${FIGMA_API_BASE_URL}/files/${fileKey}`,
      {
        headers: {
          'X-Figma-Token': accessToken,
        },
      }
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error(`Error fetching Figma file data: ${error.message}`);
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

if (MY_FIGMA_FILE_KEY === 'YOUR_FILE_KEY' || MY_FIGMA_ACCESS_TOKEN === 'YOUR_PERSONAL_ACCESS_TOKEN') {
  console.warn('Please replace YOUR_FILE_KEY and YOUR_PERSONAL_ACCESS_TOKEN with actual values.');
} else {
  getFigmaFileData(MY_FIGMA_FILE_KEY, MY_FIGMA_ACCESS_TOKEN)
    .then((fileData) => {
      console.log('Successfully fetched Figma file:', fileData.name);
      console.log('Last Modified:', fileData.lastModified);
      // console.log('Document structure (first child):', JSON.stringify(fileData.document.children[0], null, 2));
      // You can explore fileData.document, fileData.components, fileData.styles further
    })
    .catch((error) => {
      console.error('Failed to get Figma file data:', error.message);
    });
}

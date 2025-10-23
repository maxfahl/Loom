/**
 * This is the main entry point for the Figma plugin's backend logic.
 * It runs in a separate thread from the UI and interacts directly with the Figma API.
 */

// This shows the HTML page in "ui.html".
figma.showUI(__html__);

// Calls to "parent.postMessage" from the HTML page will trigger this
// callback. The callback receives a JSON object with the message as the event.data.pluginMessage.
figma.ui.onmessage = (msg) => {
  // One way to send data from the plugin to the UI is using `figma.ui.postMessage`
  // For example, if the UI sends a 'create-rectangles' message, we can respond.
  if (msg.type === 'create-rectangles') {
    const nodes: SceneNode[] = [];
    for (let i = 0; i < msg.count; i++) {
      const rect = figma.createRectangle();
      rect.x = i * 150;
      rect.fills = [{ type: 'SOLID', color: { r: 1, g: 0.5, b: 0 } }];
      figma.currentPage.appendChild(rect);
      nodes.push(rect);
    }
    figma.currentPage.selection = nodes;
    figma.viewport.scrollAndZoomIntoView(nodes);

    // Send a message back to the UI to confirm creation
    figma.ui.postMessage({ type: 'rectangles-created', count: msg.count });
  }

  // If the UI sends a 'close' message, close the plugin
  if (msg.type === 'close') {
    figma.closePlugin();
  }
};

// Example of sending initial data to the UI when it loads
figma.ui.on('load', () => {
  figma.ui.postMessage({ type: 'initial-data', message: 'Plugin loaded successfully!' });
});

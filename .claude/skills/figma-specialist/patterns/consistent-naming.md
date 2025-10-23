# Consistent Naming Conventions in Figma

Consistent naming is crucial for maintaining a scalable and automatable design system in Figma. It enables easier navigation, searchability, and programmatic access via the Figma API. Adhering to a clear naming strategy significantly improves collaboration between designers and developers.

## General Principles

-   **Be Descriptive**: Names should clearly indicate the purpose or content of the layer/component.
-   **Be Consistent**: Use the same naming structure across similar elements.
-   **Be Predictable**: Names should follow a logical pattern that can be easily understood and anticipated.
-   **Avoid Ambiguity**: Ensure names are unique enough to prevent confusion.
-   **Keep it Concise**: While descriptive, avoid overly long names that are hard to read.

## Recommended Naming Structure

Use a hierarchical naming convention, typically separated by slashes (`/`), to categorize and group elements. This mirrors folder structures and is well-supported by Figma's asset panel and API.

### Components

For components, especially those with variants, a common structure is `Category/Subcategory/Component Name/Variant Property 1=Value/Variant Property 2=Value`.

**GOOD:**

-   `Button/Primary/Default`
-   `Button/Primary/Hover`
-   `Button/Secondary/Default`
-   `Button/Secondary/Disabled`
-   `Input/Textfield/Default/State=Active`
-   `Input/Textfield/Default/State=Error`
-   `Icon/Size=24px/Name=ArrowRight`
-   `Avatar/Size=Medium/Type=Image`

**BAD:**

-   `Primary Button`
-   `Button 2`
-   `Active Text Input`
-   `Arrow Icon`

### Layers within Components/Frames

Layers within components or frames should also follow a consistent, descriptive naming convention. Use `kebab-case` or `camelCase` for individual layer names.

**GOOD:**

-   `button-label`
-   `icon-left`
-   `background-shape`
-   `text-input-field`
-   `error-message`

**BAD:**

-   `Rectangle 1`
-   `Text Copy`
-   `Group 5`
-   `Layer 12`

### Styles (Colors, Text, Effects)

Styles should also be organized hierarchically. This helps in grouping them logically in the Figma UI and makes them easier to reference programmatically.

**GOOD:**

-   `Color/Brand/Primary`
-   `Color/Grayscale/Dark`
-   `Text/Heading/H1`
-   `Text/Body/Small`
-   `Effect/Shadow/Elevation 1`

**BAD:**

-   `Blue`
-   `Headline`
-   `Small Text`
-   `Shadow`

### Pages

Organize pages logically, often by feature, status, or design phase.

**GOOD:**

-   `01 - Design System`
-   `02 - Components`
-   `03 - Feature X`
-   `WIP - Feature Y`
-   `Archive`

**BAD:**

-   `Page 1`
-   `New Stuff`
-   `Final`

## Benefits of Consistent Naming

-   **Improved Collaboration**: Designers and developers can quickly understand the purpose of elements.
-   **Enhanced Searchability**: Easily find components, layers, and styles in Figma.
-   **Streamlined Automation**: Figma API scripts can reliably target elements based on predictable names.
-   **Better Code Generation**: Tools that generate code from Figma can produce cleaner, more semantic output.
-   **Easier Maintenance**: Reduces design debt and makes updates more manageable.

By adopting and enforcing consistent naming conventions, teams can unlock the full potential of Figma as a central hub for design and development workflows.

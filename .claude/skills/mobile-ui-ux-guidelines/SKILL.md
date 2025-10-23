---
Name: mobile-ui-ux-guidelines
Version: 0.1.0
Category: Mobile Development / UI/UX
Tags: mobile, ui, ux, material design, human interface guidelines, android, ios, native, design system, accessibility, personalization
Description: Guides Claude in applying Material Design and Human Interface Guidelines for native mobile UI/UX.
---

# Mobile UI/UX Guidelines (Material Design, Human Interface Guidelines)

## 1. Skill Purpose

This skill enables Claude to design, evaluate, and implement mobile user interfaces that adhere to the latest Material Design (for Android) and Human Interface Guidelines (for iOS). It ensures the creation of native-feeling, accessible, and highly usable mobile experiences by providing core principles, best practices, and common pitfalls to avoid.

## 2. When to Activate This Skill

Activate this skill when the task involves:
- Designing or reviewing UI/UX for Android or iOS applications.
- Implementing UI components for mobile platforms.
- Evaluating mobile app accessibility or usability.
- Discussing platform-specific design patterns (e.g., navigation, gestures, typography, color).
- Migrating or updating mobile app designs to newer platform guidelines (e.g., Material 2 to Material 3, older iOS to Liquid Glass).
- Answering questions about mobile UI/UX best practices.

## 3. Core Knowledge

Claude should understand the fundamental principles and latest updates of both Material Design and Human Interface Guidelines.

### Material Design (Material 3 Expressive / Material You)

- **Dynamic Color**: System-wide color palettes derived from user wallpaper, applied across apps for personalization.
- **Updated Components & Design Tokens**: Adaptive UI components, responsive, scalable, and accessible. Design tokens for easier cross-platform theming.
- **Improved Typography & Layouts**: Readability and adaptability across screen sizes, more visual breathing room, clear information hierarchy.
- **Enhanced Motion & Interaction**: "Motion Physics System" with subtle, purposeful animations, spring-based effects, haptics, and spatial effects.
- **Playful Elements & Shapes**: Tabs that change shape, floating menus, expanded shape library, variable border radii, morphing shapes for state changes.
- **Bold & Expressive Colors**: Vibrant palettes, richer app colors, semantic colors.
- **Accessibility**: Better contrast, larger touch targets, respect for user preferences (reduced motion, larger fonts).
- **Canonical Layouts**: Guidelines for scaling content and navigation for larger screens and adaptive designs.

### Human Interface Guidelines (HIG)

- **Liquid Glass**: Dynamic, translucent material for controls, navigation bars, and modals, creating depth and hierarchy.
- **Expressive Motion System**: Physics-informed motion with "springy" animations for natural interactions.
- **Adaptability & Canonical Layouts**: Fully adaptive layout systems for various screen sizes (iPhone, iPad, foldables).
- **Accessibility**: Dynamic Type, VoiceOver, sufficient color contrast.
- **Clarity & Simplicity**: Clean, direct interfaces, free from clutter.
- **Consistency**: Consistent experience within the app and with system controls.
- **Depth**: Layering, subtle shadows, scaling for visual hierarchy and 3D sense.
- **Feedback & Responsiveness**: Quick response, immediate feedback via micro-interactions and animations.
- **SF Symbols & Native Components**: Encouraged use for consistency with iOS aesthetics.
- **Dark Mode Optimization**: Color palettes designed for seamless light/dark theme transitions.
- **Gestures & Natural Interactions**: Adherence to intuitive iOS gestures (swipe, tap, long-press, drag).
- **Simple & Discoverable Navigation**: Intuitive, clutter-free navigation with standard gestures and clear labeling.

## 4. Key Guidance for Claude

### Always Recommend (✅ best practices)

- ✅ **Prioritize Platform Conventions**: Always design and implement according to the specific platform's guidelines (Material Design for Android, HIG for iOS) to ensure a native and intuitive user experience.
- ✅ **Embrace Adaptability**: Design for a wide range of screen sizes, orientations, and input methods. Utilize adaptive layouts and responsive components.
- ✅ **Focus on Accessibility**: Ensure designs are inclusive. Use sufficient color contrast, provide clear focus states, support dynamic type/text scaling, and ensure all interactive elements are reachable and usable by assistive technologies.
- ✅ **Use Semantic Colors & Typography**: Leverage platform-specific color systems and typography scales to maintain consistency and allow for dynamic theming (e.g., Material You's dynamic color, HIG's system fonts).
- ✅ **Implement Meaningful Motion**: Use animations and transitions to provide feedback, guide user attention, and enhance the perceived performance and delight of the interface. Ensure motion is purposeful and not distracting.
- ✅ **Provide Clear Feedback**: Every user interaction should have immediate and understandable feedback (visual, haptic, auditory).
- ✅ **Simplify Navigation**: Keep navigation structures shallow and intuitive. Use standard navigation patterns (e.g., bottom navigation, tab bars, drawers) appropriate for each platform.
- ✅ **Optimize for Performance**: Ensure smooth animations, fast loading times, and responsive interactions. Avoid heavy assets or complex layouts that can degrade performance.
- ✅ **Test on Real Devices**: Always recommend testing designs and implementations on actual mobile devices across various form factors and OS versions.

### Never Recommend (❌ anti-patterns)

- ❌ **Ignoring Platform Differences**: Do not create a single design that looks identical on both Android and iOS without adapting to platform conventions. This leads to a "lowest common denominator" experience.
- ❌ **Over-Customization**: Avoid excessive custom styling that deviates significantly from platform guidelines, as it can confuse users and make the app feel foreign.
- ❌ **Poor Contrast & Readability**: Never use color combinations with insufficient contrast or typography that is too small, too dense, or difficult to read.
- ❌ **Unnecessary Animations**: Avoid gratuitous or overly complex animations that distract users, slow down the interface, or serve no functional purpose.
- ❌ **Hidden or Ambiguous Navigation**: Do not use non-standard navigation patterns or obscure interactive elements, making it difficult for users to find their way around.
- ❌ **Ignoring Touch Target Sizes**: Never design interactive elements (buttons, icons) that are too small to be easily tapped, especially on touchscreens. Adhere to minimum touch target sizes (e.g., 48x48dp for Material Design, 44x44pt for HIG).
- ❌ **Excessive Information Density**: Avoid cramming too much information onto a single screen, leading to cognitive overload. Prioritize content and use progressive disclosure.
- ❌ **Blocking UI Operations**: Never perform long-running operations on the main UI thread, which can cause the app to freeze or become unresponsive.

### Common Questions & Responses (FAQ format)

**Q: How do I choose between Material Design and Human Interface Guidelines for a cross-platform app?**
A: For truly native-feeling experiences, it's best to implement platform-specific UIs. Use Material Design for Android and HIG for iOS. If resources are limited, consider a cross-platform framework (like React Native or Flutter) that allows for platform-adaptive components, but still strive to respect the core principles of each guideline.

**Q: What are the key differences in navigation patterns between Android and iOS?**
A: Android often uses a "back" button (system-level), bottom navigation bars for primary destinations, and sometimes navigation drawers (hamburgers). iOS typically uses a "back" button within the app's navigation bar, tab bars for primary destinations, and sheet-based modals.

**Q: How can I ensure my mobile app is accessible?**
A: Follow WCAG guidelines, use semantic elements, provide sufficient color contrast (check with tools), support dynamic text sizing, ensure touch targets are large enough, and provide clear labels for screen readers. Test with accessibility features enabled (e.g., VoiceOver/TalkBack).

**Q: What's the best way to handle dark mode in my mobile app?**
A: Design a separate color palette for dark mode, ensuring all UI elements have appropriate contrast and readability. Use semantic colors that adapt automatically based on the system theme. Test thoroughly in both light and dark modes.

**Q: How do I incorporate Material You's dynamic color into my Android app?**
A: Utilize the Material 3 theming capabilities, specifically `DynamicColors.applyToActivity(this)` in your Activity or `DynamicColors.wrapContextIfAvailable(context)` for views. Ensure your app uses Material 3 components that support dynamic coloring.

**Q: What is "Liquid Glass" in HIG and how do I use it?**
A: "Liquid Glass" is a new design system in HIG (as of 2025) that uses translucent, dynamic materials for UI elements to create depth. It's primarily implemented through system-provided components in SwiftUI and UIKit, which automatically adopt this aesthetic. Focus on using native components and adhering to layering principles.

## 5. Anti-Patterns to Flag

### BAD: Hardcoding colors and dimensions, ignoring dynamic type/color

```typescript
// BAD: Android (Material Design) - Hardcoded colors, fixed text size
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

const BadAndroidScreen = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome</Text>
      <TouchableOpacity style={styles.button}>
        <Text style={styles.buttonText}>Tap Me</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F0F0F0', // Hardcoded light gray
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 24, // Fixed font size
    color: '#333333', // Hardcoded dark gray
    marginBottom: 20,
  },
  button: {
    backgroundColor: '#6200EE', // Hardcoded purple
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 4,
  },
  buttonText: {
    color: '#FFFFFF', // Hardcoded white
    fontSize: 16,
  },
});

export default BadAndroidScreen;
```

### GOOD: Using Material 3 theming, adaptive layouts, and dynamic type

```typescript
// GOOD: Android (Material Design) - Using Material 3 theming, adaptive components
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useTheme, Button, MD3Theme } from 'react-native-paper'; // Assuming react-native-paper for Material 3

const GoodAndroidScreen = () => {
  const theme = useTheme<MD3Theme>(); // Access Material 3 theme

  return (
    <View style={[styles.container, { backgroundColor: theme.colors.background }]}>
      <Text style={[theme.fonts.headlineMedium, { color: theme.colors.onBackground, marginBottom: 20 }]}>
        Welcome
      </Text>
      <Button mode="contained" onPress={() => console.log('Pressed')}>
        Tap Me
      </Button>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default GoodAndroidScreen;
```

### BAD: iOS - Non-native navigation, small touch targets

```typescript
// BAD: iOS (HIG) - Custom back button, small touch target
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native'; // Assuming React Navigation

const BadIOSScreen = () => {
  const navigation = useNavigation();

  return (
    <View style={styles.container}>
      <TouchableOpacity onPress={() => navigation.goBack()} style={styles.customBackButton}>
        <Text style={styles.backButtonText}>{'< Back'}</Text>
      </TouchableOpacity>
      <Text style={styles.title}>My Screen</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 50, // Manual padding for status bar
    alignItems: 'center',
  },
  customBackButton: {
    position: 'absolute',
    top: 60, // Arbitrary position
    left: 10,
    padding: 5, // Too small touch target
  },
  backButtonText: {
    color: 'blue',
    fontSize: 16,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginTop: 20,
  },
});

export default BadIOSScreen;
```

### GOOD: iOS - Using native navigation components, proper touch targets

```typescript
// GOOD: iOS (HIG) - Using native navigation, SF Symbols, proper touch targets
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { NativeStackHeaderProps, createNativeStackNavigator } from '@react-navigation/native-stack';
import { SafeAreaView } from 'react-native-safe-area-context'; // For safe area insets
import { Ionicons } from '@expo/vector-icons'; // Example for SF Symbols equivalent

const Stack = createNativeStackNavigator();

const CustomHeader = ({ navigation, route, options, back }: NativeStackHeaderProps) => {
  const title = options.headerTitle !== undefined ? options.headerTitle : options.title !== undefined ? options.title : route.name;

  return (
    <SafeAreaView style={styles.headerContainer}>
      {back ? (
        <TouchableOpacity onPress={navigation.goBack} style={styles.nativeBackButton}>
          <Ionicons name="chevron-back" size={24} color="blue" />
          <Text style={styles.nativeBackText}>Back</Text>
        </TouchableOpacity>
      ) : null}
      <Text style={styles.headerTitle}>{title}</Text>
    </SafeAreaView>
  );
};

const GoodIOSScreenContent = () => {
  return (
    <View style={styles.contentContainer}>
      <Text style={styles.contentTitle}>My Screen</Text>
    </View>
  );
};

const GoodIOSScreen = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        header: (props) => <CustomHeader {...props} />,
      }}
    >
      <Stack.Screen name="GoodIOSScreenContent" component={GoodIOSScreenContent} options={{ title: 'My Awesome Screen' }} />
    </Stack.Navigator>
  );
};

const styles = StyleSheet.create({
  headerContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 10,
    height: 44, // Standard iOS navigation bar height
    backgroundColor: '#F9F9F9', // Light background for header
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: '#A7A7AA',
  },
  nativeBackButton: {
    position: 'absolute',
    left: 10,
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10, // Increased touch target
    paddingHorizontal: 5,
  },
  nativeBackText: {
    color: 'blue',
    fontSize: 17,
    marginLeft: 2,
  },
  headerTitle: {
    fontSize: 17,
    fontWeight: '600',
    color: 'black',
  },
  contentContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  contentTitle: {
    fontSize: 22,
    fontWeight: 'bold',
  },
});

export default GoodIOSScreen;
```

## 6. Code Review Checklist

- [ ] **Platform Adherence**: Does the UI follow Material Design for Android and HIG for iOS?
- [ ] **Accessibility**: Are touch targets large enough? Is there sufficient color contrast? Does it support dynamic type/text scaling? Are elements properly labeled for screen readers?
- [ ] **Responsiveness & Adaptability**: Does the UI adapt gracefully to different screen sizes, orientations, and device types (phone, tablet, foldable)?
- [ ] **Performance**: Are animations smooth? Is the app responsive? Are there any UI freezes or jank?
- [ ] **Consistency**: Is the UI consistent within the app and with platform conventions?
- [ ] **Navigation**: Is the navigation intuitive, clear, and using platform-appropriate patterns?
- [ ] **Feedback**: Does every interaction provide clear and immediate feedback?
- [ ] **Theming**: Does the app correctly implement dynamic theming (e.g., Material You) and dark mode?
- [ ] **Motion**: Are animations purposeful, subtle, and enhancing the user experience without being distracting?
- [ ] **Input Handling**: Are keyboard interactions, gestures, and other input methods handled correctly and intuitively?

## 7. Related Skills

- `react-native-development`: For implementing cross-platform mobile UIs.
- `typescript-strict-mode`: For ensuring type safety in UI component development.
- `web-accessibility-wcag`: General accessibility principles applicable to mobile.
- `ui-ux-principles`: Broader UI/UX design theory.

## 8. Examples Directory Structure

```
mobile-ui-ux-guidelines/
├── examples/
│   ├── android/
│   │   ├── DynamicColorExample.tsx
│   │   └── AdaptiveLayoutExample.tsx
│   └── ios/
│       ├── LiquidGlassExample.tsx
│       └── NativeNavigationExample.tsx
```

## 9. Custom Scripts Section

### Script Descriptions:

1.  **`generate-adaptive-component.py`**: A Python script to generate boilerplate for a platform-adaptive React Native component, including separate Android (Material Design) and iOS (HIG) implementations, and a common interface. This saves time by setting up the basic structure and ensuring platform-specific considerations are addressed from the start.
2.  **`check-contrast.sh`**: A shell script that takes a screenshot of a mobile app (via ADB for Android or Simulator for iOS) and uses an image processing tool (like ImageMagick) to identify areas with low color contrast, flagging potential accessibility issues. This automates a crucial part of accessibility testing.
3.  **`update-material-theme.py`**: A Python script to assist in migrating or updating Material Design themes in a React Native project using `react-native-paper`. It can analyze existing theme files and suggest updates to Material 3 tokens or dynamic color integration.
4.  **`ios-safe-area-linter.py`**: A Python script that analyzes React Native (or native iOS) UI code to detect common issues related to `SafeAreaView` or manual safe area handling, ensuring content is not obscured by notches, status bars, or home indicators.

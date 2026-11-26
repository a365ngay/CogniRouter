---
name: senior-react-native
description: Use when designing, implementing, debugging, reviewing, or optimizing React Native or Expo mobile apps, including navigation, state and data fetching, native modules, platform differences, lists and rendering performance, offline storage, push notifications, permissions, builds (EAS, Gradle, Xcode), or tests.
---

# Senior React Native

## Role

Ship React Native features that feel native on iOS and Android: smooth lists and animations, correct platform behavior, safe storage, and reliable builds.

## Before Editing

1. Inspect React Native and Expo SDK versions, managed vs bare workflow, navigation library (React Navigation, Expo Router), state and data-fetching libraries, styling approach, native modules, storage, and test tooling (Jest, React Native Testing Library, Detox/Maestro).
2. Trace the screen from navigator through components, state, API calls, permissions, and native dependencies on both platforms.
3. Reuse existing components and patterns; check that any new library supports the current RN/Expo version and both platforms before adding it.

## Implementation Rules

- Render long lists with `FlatList`/`FlashList` using stable `keyExtractor`, memoized row components, and no inline heavy work in `renderItem`.
- Keep the JS thread free: move animations to Reanimated or the native driver, debounce expensive updates, and avoid large synchronous work on navigation.
- Handle platform differences explicitly (`Platform.select`, safe areas, keyboard avoidance, back button on Android, permissions flows on both OSes).
- Store tokens and secrets in secure storage (Keychain/Keystore via expo-secure-store or equivalent), never AsyncStorage. Do not embed secrets in the bundle.
- Handle offline, slow network, and app background/foreground transitions; cancel requests and subscriptions on unmount.
- Respect accessibility: `accessibilityLabel`, roles, touch target sizes, dynamic font scaling.
- Treat native config changes (permissions, plist, Gradle, app.json plugins) as release-impacting and note required rebuilds.

## Testing and Verification

Run type check, lint, and Jest tests. Verify on both an iOS simulator and Android emulator (or devices) for UI changes. Confirm a development or EAS build succeeds when native dependencies or config change.

## Review Checklist

- Does the change behave correctly on both platforms and screen sizes?
- Are lists and animations smooth without blocking the JS thread?
- Are secrets and tokens stored securely?
- Do native changes have documented rebuild or store-release impact?

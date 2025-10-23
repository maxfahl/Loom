---
name: swiftui-uikit-development-ios
version: 1.0.0
category: Mobile Development / iOS
tags: SwiftUI, UIKit, iOS, Swift, Mobile, UI/UX
description: Enables Claude to assist with developing iOS applications using SwiftUI, UIKit, and their interoperability.
---

## Skill Purpose

This skill enables Claude to provide comprehensive guidance and code examples for developing iOS applications, leveraging both SwiftUI for modern declarative UI and UIKit for established components and complex integrations. It covers best practices for building new applications, migrating existing ones, and effectively combining the two frameworks.

## When to Activate This Skill

Activate this skill when the user's request involves:
- Developing new iOS features or applications.
- Migrating existing UIKit codebases to SwiftUI.
- Integrating SwiftUI views into UIKit projects or vice-versa.
- Discussing iOS UI/UX patterns, state management, or navigation.
- Troubleshooting issues related to SwiftUI, UIKit, or their interoperability.
- Generating boilerplate code for SwiftUI views, UIKit representables, or asset management.

## Core Knowledge

The fundamental concepts, patterns, and APIs Claude needs to know include:

### SwiftUI
- **Declarative UI:** Understanding how SwiftUI describes UI based on state.
- **State Management:** `@State`, `@Binding`, `@ObservedObject`, `@StateObject`, `@EnvironmentObject`, `@Environment`, `@AppStorage`, `@SceneStorage`, `@Observable` (Swift 5.9+).
- **View Composition:** Modifiers, `ViewBuilder`, custom views.
- **Layout System:** `VStack`, `HStack`, `ZStack`, `GeometryReader`, `alignmentGuide`, `fixedSize`, `frame`.
- **Navigation:** `NavigationStack`, `NavigationLink`, `sheet`, `fullScreenCover`.
- **Data Flow:** `Combine` framework basics, `PassthroughSubject`, `CurrentValueSubject`.
- **Swift Concurrency:** `async/await` for asynchronous operations.
- **Xcode Previews:** Usage for rapid UI iteration.

### UIKit
- **Imperative UI:** Understanding how UIKit builds UI programmatically or with Storyboards/Nibs.
- **View Hierarchy:** `UIView`, `UIViewController`, `UINavigationController`, `UITabBarController`.
- **Delegation & Data Sources:** Common patterns for handling events and data.
- **Auto Layout:** `NSLayoutConstraint`, `UIStackView`, visual format language.
- **Lifecycle:** `UIViewController` lifecycle methods.
- **Target-Action:** Event handling mechanism.
- **Modern UIKit Features:** `UIScene`, `UICollectionViewCompositionalLayout`, `DiffableDataSource`.

### Interoperability
- **Embedding SwiftUI in UIKit:** `UIHostingController`.
- **Embedding UIKit in SwiftUI:** `UIViewRepresentable`, `UIViewControllerRepresentable`.
- **Data Sharing:** Bridging data between SwiftUI and UIKit using `Combine` or shared models.
- **Architectural Patterns:** MVVM, VIPER, Clean Architecture, and how they apply to hybrid apps.

## Key Guidance for Claude

### Always Recommend (✅ best practices)
- ✅ **SwiftUI-First for New Development:** For new features or applications, prioritize SwiftUI due to its declarative nature, faster development, and cross-platform potential.
- ✅ **Hybrid Approach for Existing Apps:** For existing UIKit applications, advocate for a gradual migration using `UIHostingController` to embed new SwiftUI features.
- ✅ **Clear Separation of Concerns:** Encourage architectural patterns (e.g., MVVM) where models and view models are UI-agnostic, facilitating reuse between SwiftUI and UIKit.
- ✅ **Leverage Swift Concurrency:** Utilize `async/await` for all asynchronous operations in both SwiftUI and modern UIKit code.
- ✅ **Type-Safe Asset Access:** Recommend generating Swift code for `Assets.xcassets` to prevent runtime errors.
- ✅ **Modular Design:** Promote breaking down complex UIs into smaller, reusable components/views.
- ✅ **Accessibility:** Always consider accessibility from the start, using SwiftUI's built-in modifiers and UIKit's accessibility APIs.
- ✅ **Xcode Previews:** Emphasize the use of Xcode Previews for rapid UI development and testing.

### Never Recommend (❌ anti-patterns)
- ❌ **Mixing UI Logic:** Avoid directly manipulating UIKit views from SwiftUI or vice-versa without proper representable wrappers or `UIHostingController`.
- ❌ **Massive Views/View Controllers:** Discourage large, monolithic views or view controllers. Break them down into smaller, manageable components.
- ❌ **Force Unwrapping Optionals:** Advise against excessive force unwrapping (`!`) without proper validation or fallback mechanisms.
- ❌ **Hardcoding Strings/Colors:** Never hardcode strings or colors; use `Localizable.strings` and `Assets.xcassets` for proper management.
- ❌ **Ignoring Performance:** Do not neglect performance considerations, especially in list views or complex animations. Profile and optimize.
- ❌ **Directly Accessing `AppDelegate`/`SceneDelegate`:** Avoid direct access; use environment objects or proper dependency injection.

### Common Questions & Responses (FAQ format)

**Q: How do I embed a SwiftUI view into an existing UIKit `UIViewController`?**
A: Use `UIHostingController`. Instantiate it with your SwiftUI view, then add its view as a child to your `UIViewController`'s view hierarchy.
```swift
import SwiftUI
import UIKit

class MyUIKitViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()

        let swiftUIContentView = MySwiftUIView()
        let hostingController = UIHostingController(rootView: swiftUIContentView)

        addChild(hostingController)
        view.addSubview(hostingController.view)
        hostingController.didMove(toParent: self)

        // Set up constraints for the SwiftUI view
        hostingController.view.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            hostingController.view.topAnchor.constraint(equalTo: view.topAnchor),
            hostingController.view.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            hostingController.view.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            hostingController.view.bottomAnchor.constraint(equalTo: view.bottomAnchor)
        ])
    }
}

struct MySwiftUIView: View {
    var body: some View {
        Text("Hello from SwiftUI!")
            .font(.largeTitle)
            .padding()
            .background(Color.blue)
            .foregroundColor(.white)
            .cornerRadius(10)
    }
}
```

**Q: How can I use a UIKit `UIView` (e.g., `MKMapView`) in SwiftUI?**
A: Wrap the `UIView` using `UIViewRepresentable`.
```swift
import SwiftUI
import MapKit

struct MapView: UIViewRepresentable {
    @Binding var coordinate: CLLocationCoordinate2D

    func makeUIView(context: Context) -> MKMapView {
        MKMapView(frame: .zero)
    }

    func updateUIView(_ uiView: MKMapView, context: Context) {
        let span = MKCoordinateSpan(latitudeDelta: 0.02, longitudeDelta: 0.02)
        let region = MKCoordinateRegion(center: coordinate, span: span)
        uiView.setRegion(region, animated: true)
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, MKMapViewDelegate {
        var parent: MapView

        init(_ parent: MapView) {
            self.parent = parent
        }

        // Implement MKMapViewDelegate methods if needed
    }
}

struct MapView_Previews: PreviewProvider {
    @State static var location = CLLocationCoordinate2D(latitude: 34.011_286, longitude: -116.166_868)

    static var previews: some View {
        MapView(coordinate: $location)
    }
}
```

**Q: What's the best way to manage state in SwiftUI?**
A: It depends on the scope and ownership of the state:
- `@State`: For simple, local view-specific state.
- `@Binding`: For two-way connections to state owned by a parent view.
- `@ObservedObject` / `@StateObject`: For reference types (classes) that hold more complex, shared state. Use `@StateObject` for initial ownership, `@ObservedObject` for observing an object passed from a parent.
- `@EnvironmentObject`: For sharing state across multiple views in a view hierarchy without explicit passing.
- `@Observable` (Swift 5.9+): The modern approach for observable reference types, replacing `ObservableObject` and `Published` for cleaner code.

## Anti-Patterns to Flag

### 1. Massive View Controllers (UIKit) / Massive Views (SwiftUI)
**BAD:**
```swift
// UIKit - Massive ViewController
class ComplexViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, UITextFieldDelegate, CLLocationManagerDelegate {
    // Hundreds of lines of UI setup, business logic, network calls, and delegate methods
    // ...
}

// SwiftUI - Massive View
struct ComplexView: View {
    @State private var data: [String] = []
    @State private var isLoading = false
    @State private var searchText = ""
    @State private var showingAlert = false

    var body: some View {
        NavigationView {
            VStack {
                TextField("Search", text: $searchText)
                    .padding()
                    .onChange(of: searchText) { newValue in
                        // Complex filtering logic
                    }
                if isLoading {
                    ProgressView()
                } else {
                    List(data, id: \.self) { item in
                        Text(item)
                            .onTapGesture {
                                // Complex navigation and data manipulation
                            }
                    }
                }
            }
            .navigationTitle("Items")
            .onAppear {
                // Complex data fetching
            }
            .alert("Error", isPresented: $showingAlert) {
                Button("OK") { }
            }
        }
    }
}
```
**GOOD:**
```swift
// UIKit - Decomposed ViewController with MVVM
class ItemListViewController: UIViewController {
    var viewModel: ItemListViewModel!
    let tableView = UITableView()

    override func viewDidLoad() {
        super.viewDidLoad()
        setupTableView()
        bindViewModel()
        viewModel.fetchItems()
    }

    private func setupTableView() { /* ... */ }
    private func bindViewModel() { /* ... */ }
    // Delegate/DataSource methods are concise and defer to viewModel
}

class ItemListViewModel {
    // Business logic, data fetching, state management
    // ...
}

// SwiftUI - Decomposed View with MVVM
struct ItemListView: View {
    @StateObject var viewModel = ItemListViewModel() // Using @StateObject for ownership

    var body: some View {
        NavigationView {
            VStack {
                SearchBar(searchText: $viewModel.searchText) // Extracted component
                if viewModel.isLoading {
                    ProgressView()
                } else {
                    ItemList(items: viewModel.filteredItems) { item in
                        viewModel.selectItem(item) // Delegate action to viewModel
                    }
                }
            }
            .navigationTitle("Items")
            .onAppear(perform: viewModel.fetchItems)
            .alert("Error", isPresented: $viewModel.showingAlert) {
                Button("OK") { }
            }
        }
    }
}

struct SearchBar: View { /* ... */ } // Reusable component
struct ItemList: View { /* ... */ } // Reusable component
```

### 2. Force Unwrapping Optionals Without Justification
**BAD:**
```swift
let imageUrl: URL! = URL(string: "https://example.com/image.png") // Force unwrapped at declaration
imageView.image = UIImage(data: try! Data(contentsOf: imageUrl)) // Force unwrapped Data
```
**GOOD:**
```swift
if let imageUrl = URL(string: "https://example.com/image.png") {
    Task {
        do {
            let (data, _) = try await URLSession.shared.data(from: imageUrl)
            if let image = UIImage(data: data) {
                // Update UI on main actor
                await MainActor.run {
                    imageView.image = image
                }
            }
        } catch {
            print("Error loading image: \(error)")
            // Handle error, e.g., show placeholder image
        }
    }
} else {
    print("Invalid image URL")
}
```

## Code Review Checklist

- [ ] **Architecture:** Is the code structured according to established patterns (MVVM, etc.)? Are concerns clearly separated?
- [ ] **State Management (SwiftUI):** Are appropriate property wrappers (`@State`, `@StateObject`, `@Binding`, `@EnvironmentObject`, `@Observable`) used correctly?
- [ ] **Interoperability:** If mixing SwiftUI and UIKit, are `UIHostingController`, `UIViewRepresentable`, or `UIViewControllerRepresentable` used correctly and efficiently?
- [ ] **Asynchronous Operations:** Are `async/await` and `Task` used for concurrency? Is UI updated on the main actor?
- [ ] **Error Handling:** Are failable operations (e.g., network requests, JSON decoding) handled gracefully with `do-catch` or `guard let`?
- [ ] **Optionals:** Are optionals handled safely using `if let`, `guard let`, or nil coalescing, avoiding unnecessary force unwrapping?
- [ ] **Performance:** Are list views optimized (e.g., `LazyVStack`, `LazyHStack`, `UITableViewCell` reuse)? Are heavy computations offloaded from the main thread?
- [ ] **Accessibility:** Are accessibility labels, hints, and traits provided for UI elements?
- [ ] **Localization:** Are all user-facing strings localized using `NSLocalizedString` or SwiftUI's `Text` initializer with a key?
- [ ] **Code Style:** Does the code adhere to Swift API Design Guidelines and project-specific style guides?
- [ ] **Testing:** Are unit and UI tests present for critical components and logic?
- [ ] **Documentation:** Is complex logic or public API documented with comments?

## Related Skills

- `swift-concurrency`
- `mvvm-architecture`
- `clean-architecture`
- `testing-ios` (future skill)

## Examples Directory Structure

```
examples/
├── SwiftUI/
│   ├── SimpleCounterView.swift
│   ├── DataFetchingView.swift
│   └── CustomModifierExample.swift
├── UIKit/
│   ├── LoginViewController.swift
│   └── CustomTableView.swift
└── Interoperability/
    ├── SwiftUIInUIKitViewController.swift
    └── UIKitInSwiftUIView.swift
```

## Custom Scripts Section

For this skill, the following automation scripts would save significant time for iOS developers:

1.  **`generate-swiftui-view.sh`**: Automates the creation of a new SwiftUI View file with a basic structure and Xcode Preview.
2.  **`generate-representable.sh`**: Generates boilerplate for `UIViewRepresentable` or `UIViewControllerRepresentable` to easily embed UIKit components in SwiftUI.
3.  **`generate-asset-enum.py`**: A Python script that scans `Assets.xcassets` and generates a type-safe Swift enum for image and color assets.

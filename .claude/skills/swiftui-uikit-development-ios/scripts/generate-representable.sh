#!/bin/bash

# generate-representable.sh
#
# Description:
#   Generates boilerplate code for UIViewRepresentable or UIViewControllerRepresentable.
#   This script streamlines the process of integrating UIKit views or view controllers
#   into SwiftUI, ensuring correct structure and common patterns.
#
# Usage:
#   ./generate-representable.sh -n MyMapView -t UIView
#   ./generate-representable.sh --name MyCameraVC --type UIViewController -d ./Representables
#
# Arguments:
#   -n, --name      <RepresentableName> (Required) The name of the Representable struct (e.g., "MyMapView").
#                                         Will create <RepresentableName>.swift.
#   -t, --type      <RepresentableType> (Required) The type of UIKit component to represent:
#                                         "UIView" for UIViewRepresentable or
#                                         "UIViewController" for UIViewControllerRepresentable.
#   -d, --directory <Path>              (Optional) The directory where the file should be created.
#                                         Defaults to the current directory.
#   -h, --help                          Display this help message.
#
# Example:
#   To create a UIViewRepresentable named "PDFViewRepresentable" in the "Sources/Representables" directory:
#   ./generate-representable.sh -n PDFViewRepresentable -t UIView -d Sources/Representables
#
# Production-ready features:
# - Argument parsing for flexibility.
# - Validation for required arguments and type.
# - Error handling for missing arguments or directory creation failures.
# - Informative output messages.
# - Cross-platform compatibility (standard bash commands).

# --- Configuration ---
DEFAULT_DIR="."

# --- Functions ---

# Function to display help message
display_help() {
    echo "Usage: $0 -n <RepresentableName> -t <RepresentableType> [-d <Path>]"
    echo ""
    echo "Arguments:"
    echo "  -n, --name      <RepresentableName> (Required) The name of the Representable struct."
    echo "  -t, --type      <RepresentableType> (Required) Type: 'UIView' or 'UIViewController'."
    echo "  -d, --directory <Path>              (Optional) Directory to create the file in. Defaults to current."
    echo "  -h, --help                          Display this help message."
    echo ""
    echo "Example:"
    echo "  $0 -n MyMapView -t UIView"
    echo "  $0 --name MyCameraVC --type UIViewController --directory Sources/Representables"
    exit 0
}

# Function to generate UIViewRepresentable content
generate_uiview_representable_content() {
    local representable_name=$1
    local uikit_view_name="${representable_name/Representable/}" # Attempt to infer UIKit view name
    if [[ "${uikit_view_name}" == "${representable_name}" ]]; then
        uikit_view_name="MyUIKitView" # Fallback if no 'Representable' suffix
    fi

    cat << EOF
import SwiftUI
import UIKit

struct ${representable_name}: UIViewRepresentable {
    // MARK: - Configuration Properties
    // Add properties here that your UIKit view needs to be configured with.
    // Example: @Binding var data: String

    func makeUIView(context: Context) -> ${uikit_view_name} {
        // Return the UIKit view you want to present.
        // Example: return ${uikit_view_name}()
        fatalError("Implement makeUIView to return your UIKit view")
    }

    func updateUIView(_ uiView: ${uikit_view_name}, context: Context) {
        // Update the UIKit view with new data from SwiftUI.
        // This method is called when SwiftUI needs to update the view.
        // Example: uiView.text = data
    }

    // MARK: - Coordinator (Optional)
    // Use a Coordinator to communicate changes from your UIKit view back to SwiftUI.
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject { // Add UIKit delegates here if needed, e.g., UITableViewDelegate
        var parent: ${representable_name}

        init(_ parent: ${representable_name}) {
            self.parent = parent
        }

        // Implement delegate methods here and communicate back to parent.e.g.,
        // @objc func someAction(_ sender: UIButton) {
        //     parent.someBinding = "New Value"
        // }
    }
}

// MARK: - Previews
struct ${representable_name}_Previews: PreviewProvider {
    static var previews: some View {
        // Provide a preview for your representable.
        // Example: ${representable_name}(data: .constant("Preview Data"))
        Text("Preview for ${representable_name}") // Placeholder
    }
}
EOF
}

# Function to generate UIViewControllerRepresentable content
generate_uiviewcontroller_representable_content() {
    local representable_name=$1
    local uikit_vc_name="${representable_name/Representable/}" # Attempt to infer UIKit VC name
    if [[ "${uikit_vc_name}" == "${representable_name}" ]]; then
        uikit_vc_name="MyUIKitViewController" # Fallback if no 'Representable' suffix
    fi

    cat << EOF
import SwiftUI
import UIKit

struct ${representable_name}: UIViewControllerRepresentable {
    // MARK: - Configuration Properties
    // Add properties here that your UIKit view controller needs to be configured with.
    // Example: @Binding var data: String

    func makeUIViewController(context: Context) -> ${uikit_vc_name} {
        // Return the UIKit view controller you want to present.
        // Example: return ${uikit_vc_name}()
        fatalError("Implement makeUIViewController to return your UIKit view controller")
    }

    func updateUIViewController(_ uiViewController: ${uikit_vc_name}, context: Context) {
        // Update the UIKit view controller with new data from SwiftUI.
        // This method is called when SwiftUI needs to update the view controller.
        // Example: uiViewController.data = data
    }

    // MARK: - Coordinator (Optional)
    // Use a Coordinator to communicate changes from your UIKit view controller back to SwiftUI.
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject { // Add UIKit delegates here if needed, e.g., UINavigationControllerDelegate
        var parent: ${representable_name}

        init(_ parent: ${representable_name}) {
            self.parent = parent
        }

        // Implement delegate methods here and communicate back to parent.e.g.,
        // func someViewControllerDelegateMethod(_ vc: ${uikit_vc_name}, didDoSomething data: String) {
        //     parent.someBinding = data
        // }
    }
}

// MARK: - Previews
struct ${representable_name}_Previews: PreviewProvider {
    static var previews: some View {
        // Provide a preview for your representable.
        // Example: ${representable_name}(data: .constant("Preview Data"))
        Text("Preview for ${representable_name}") // Placeholder
    }
}
EOF
}

# --- Main Script Logic ---

REPRESENTABLE_NAME=""
REPRESENTABLE_TYPE=""
OUTPUT_DIR="${DEFAULT_DIR}"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -n|--name)
            REPRESENTABLE_NAME="$2"
            shift # past argument
            ;;
        -t|--type)
            REPRESENTABLE_TYPE="$2"
            shift # past argument
            ;;
        -d|--directory)
            OUTPUT_DIR="$2"
            shift # past argument
            ;;
        -h|--help)
            display_help
            ;;
        *)
            echo "Error: Unknown parameter passed: $1"
            display_help
            ;;
    esac
    shift # past argument or value
done

# Validate REPRESENTABLE_NAME and REPRESENTABLE_TYPE
if [ -z "${REPRESENTABLE_NAME}" ] || [ -z "${REPRESENTABLE_TYPE}" ]; then
    echo "Error: Representable name and type are required. Use -n/--name and -t/--type."
    display_help
fi

if [[ "${REPRESENTABLE_TYPE}" != "UIView" && "${REPRESENTABLE_TYPE}" != "UIViewController" ]]; then
    echo "Error: Invalid representable type. Must be 'UIView' or 'UIViewController'."
    display_help
fi

# Create directory if it doesn't exist
mkdir -p "${OUTPUT_DIR}"
if [ $? -ne 0 ]; then
    echo "Error: Could not create directory '${OUTPUT_DIR}'."
    exit 1
fi

FILE_PATH="${OUTPUT_DIR}/${REPRESENTABLE_NAME}.swift"

# Check if file already exists
if [ -f "${FILE_PATH}" ]; then
    echo "Error: File '${FILE_PATH}' already exists. Aborting to prevent overwrite."
    exit 1
fi

# Generate content and write to file
if [ "${REPRESENTABLE_TYPE}" == "UIView" ]; then
    generate_uiview_representable_content "${REPRESENTABLE_NAME}" > "${FILE_PATH}"
else
    generate_uiviewcontroller_representable_content "${REPRESENTABLE_NAME}" > "${FILE_PATH}"
fi

if [ $? -eq 0 ]; then
    echo "Successfully created ${REPRESENTABLE_TYPE}Representable: '${FILE_PATH}'"
else
    echo "Error: Failed to create Representable file."
    exit 1
fi

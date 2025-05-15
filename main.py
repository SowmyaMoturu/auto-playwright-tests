from pathlib import Path
import argparse
import os
from config import load_framework_config
from utils.framework_analyzer import FrameworkAnalyzer
from chains.convert_manual_to_script import generate_feature_and_steps, load_manual_test
from utils.file_writer import write_test_components
from generate_mfe_templates import MFETemplateGenerator


def get_repo_root() -> Path:
    """Get the automation repository root directory"""
    # Start from current directory and look for src/features or package.json
    current = Path.cwd()
    while current != current.parent:
        if (current / "src" / "features").exists() or (current / "package.json").exists():
            return current
        current = current.parent
    return Path.cwd()  # Fallback to current directory


def analyze_framework(framework_path: str | Path):
    """Analyze the existing framework structure"""
    config = load_framework_config(framework_path)
    analyzer = FrameworkAnalyzer(config)
    analysis = analyzer.analyze_framework()
    return analysis


def setup_required_folders():
    """Ensure required folders exist"""
    folders = [
        "data/manual_tests",
        "data/har",
        "data/dom",
        "prompts",
        "outputs"
    ]
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)


def extract_feature_name(manual_test_path: str) -> str:
    """Extract feature name from manual test file"""
    content = Path(manual_test_path).read_text()
    if "Feature:" in content:
        feature_line = [line for line in content.split('\n') if "Feature:" in line][0]
        return feature_line.split("Feature:")[1].strip().lower().replace(" ", "_")
    return Path(manual_test_path).stem


def validate_paths(framework_path: Path, manual_test_path: Path):
    """Validate that all required paths and files exist"""
    # Check framework path
    if not framework_path.exists():
        raise FileNotFoundError(f"Framework path does not exist: {framework_path}")
    
    # Check manual test file
    if not manual_test_path.exists():
        raise FileNotFoundError(f"Manual test file does not exist: {manual_test_path}")
    
    # Check prompts directory
    prompts_dir = Path("prompts")
    required_prompts = [
        "feature_file_prompt.md",
        "step_definition_prompt.md",
        "test_generation_prompt.md"
    ]
    
    for prompt in required_prompts:
        prompt_path = prompts_dir / prompt
        if not prompt_path.exists():
            raise FileNotFoundError(f"Required prompt file not found: {prompt_path}")


def main(framework_path: str | None, manual_test_path: str, mfe_path: str = None):
    """Main entry point for test generation"""
    try:
        # If framework_path not provided, use repo root
        if not framework_path:
            framework_path = get_repo_root()
        
        # Convert to absolute paths
        framework_path = Path(framework_path).resolve()
        manual_test_path = Path(manual_test_path).resolve()
        if mfe_path:
            mfe_path = Path(mfe_path).resolve()

        # Ensure we're in the framework directory
        os.chdir(framework_path)
        
        # Ensure required folders exist
        setup_required_folders()
        
        # Validate all required paths and files
        validate_paths(framework_path, manual_test_path)
        
        # Generate MFE templates if MFE path is provided
        if mfe_path:
            try:
                generator = MFETemplateGenerator(mfe_path)
                generator.analyze_mfe()
                generator.generate_templates()
                print("✓ Generated MFE templates successfully")
            except Exception as e:
                print(f"! Warning: Failed to generate MFE templates: {e}")
                print("  Proceeding with test generation without MFE templates")
        
        # Analyze framework structure
        framework_analysis = analyze_framework(framework_path)
        
        # Generate test components
        components = generate_feature_and_steps(
            manual_test_path,
            framework_analysis=framework_analysis
        )
        
        # Extract feature name
        feature_name = extract_feature_name(manual_test_path)
        
        # Write components to framework
        write_test_components(
            components,
            framework_path,
            feature_name
        )
        
        print(f"\nSuccessfully generated test components for feature: {feature_name}")
        print(f"- Feature file: src/features/{feature_name}.feature")
        print(f"- Step definitions: src/step-definitions/{feature_name}.steps.ts")
        print("- Page objects: " + ", ".join(f"src/pages/{page}.ts" for page in components.page_objects))
        if components.page_objects_updates:
            print("- Updated PageObjects.ts with new getters")
            
    except Exception as e:
        print(f"\n❌ Error during test generation: {str(e)}")
        raise


def parse_args():
    parser = argparse.ArgumentParser(description="Generate Playwright tests from manual instructions")
    parser.add_argument(
        "--framework-path",
        type=str,
        help="Path to your Playwright-Cucumber framework (default: auto-detect)"
    )
    parser.add_argument(
        "--manual-test",
        type=str,
        required=True,
        help="Path to the manual test instructions file"
    )
    parser.add_argument(
        "--mfe-path",
        type=str,
        help="Optional: Path to MFE project for template generation"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.framework_path, args.manual_test, args.mfe_path)


    
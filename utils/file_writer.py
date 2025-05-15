from pathlib import Path
from typing import Dict

from chains.convert_manual_to_script import TestComponents


def write_test_components(
    components: TestComponents,
    framework_path: Path,
    feature_name: str
) -> None:
    """Write generated test components to the framework"""
    # Ensure directories exist
    feature_dir = framework_path / "src" / "features"
    step_def_dir = framework_path / "src" / "step-definitions"
    page_dir = framework_path / "src" / "pages"
    
    feature_dir.mkdir(parents=True, exist_ok=True)
    step_def_dir.mkdir(parents=True, exist_ok=True)
    page_dir.mkdir(parents=True, exist_ok=True)
    
    # Write feature file
    feature_file = feature_dir / f"{feature_name}.feature"
    feature_file.write_text(components.feature_file)
    
    # Write step definitions
    step_def_file = step_def_dir / f"{feature_name}.steps.ts"
    step_def_file.write_text(components.step_definitions)
    
    # Write page objects
    for page_name, content in components.page_objects.items():
        page_file = page_dir / f"{page_name}.ts"
        if not page_file.exists():  # Only write if file doesn't exist
            page_file.write_text(content)
            
    # Update PageObjects.ts if needed
    if components.page_objects_updates:
        page_objects_file = page_dir / "PageObjects.ts"
        if page_objects_file.exists():
            # Append updates to existing file
            current_content = page_objects_file.read_text()
            if not current_content.endswith('\n'):
                current_content += '\n'
            page_objects_file.write_text(current_content + components.page_objects_updates)
        else:
            # Create new file
            page_objects_file.write_text(components.page_objects_updates) 
from pathlib import Path
import ast
import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
import yaml

@dataclass
class ComponentInfo:
    name: str
    path: str
    props: List[str]
    state: Dict[str, dict]
    test_id: Optional[str]
    children: Dict[str, 'ComponentInfo']
    events: Dict[str, dict]
    api_endpoints: Dict[str, dict]

class MFETemplateGenerator:
    def __init__(self, mfe_root: Path):
        self.mfe_root = Path(mfe_root)
        self.components: Dict[str, ComponentInfo] = {}
        self.redux_store: Dict[str, dict] = {}
        self.api_endpoints: Dict[str, dict] = {}

    def analyze_mfe(self):
        """Analyze the MFE codebase and extract component information"""
        # Analyze components
        self._analyze_components()
        # Analyze Redux store
        self._analyze_redux_store()
        # Analyze API endpoints
        self._analyze_api_endpoints()

    def _analyze_components(self):
        """Extract component information from React components"""
        for tsx_file in self.mfe_root.rglob("*.tsx"):
            if "node_modules" in str(tsx_file):
                continue

            with open(tsx_file) as f:
                content = f.read()

            # Extract component name
            component_name = self._extract_component_name(content)
            if not component_name:
                continue

            # Extract props
            props = self._extract_props(content)

            # Extract test IDs
            test_id = self._extract_test_id(content)

            # Extract state usage
            state = self._extract_state_usage(content)

            # Extract children components
            children = self._extract_children(content)

            # Extract event handlers
            events = self._extract_events(content)

            # Extract API endpoints
            api_endpoints = self._extract_api_usage(content)

            self.components[component_name] = ComponentInfo(
                name=component_name,
                path=str(tsx_file.relative_to(self.mfe_root)),
                props=props,
                state=state,
                test_id=test_id,
                children=children,
                events=events,
                api_endpoints=api_endpoints
            )

    def _analyze_redux_store(self):
        """Analyze Redux store structure"""
        for ts_file in self.mfe_root.rglob("*store*.ts"):
            if "node_modules" in str(ts_file):
                continue

            with open(ts_file) as f:
                content = f.read()

            # Extract reducers
            reducers = self._extract_reducers(content)
            # Extract selectors
            selectors = self._extract_selectors(content)
            # Extract actions
            actions = self._extract_actions(content)

            self.redux_store.update({
                "reducers": reducers,
                "selectors": selectors,
                "actions": actions
            })

    def _analyze_api_endpoints(self):
        """Analyze API endpoint definitions"""
        for ts_file in self.mfe_root.rglob("*api*.ts"):
            if "node_modules" in str(ts_file):
                continue

            with open(ts_file) as f:
                content = f.read()

            endpoints = self._extract_endpoints(content)
            self.api_endpoints.update(endpoints)

    def generate_templates(self):
        """Generate all required templates"""
        self._generate_component_context()
        self._generate_test_mapping()
        self._generate_framework_integration()

    def _generate_component_context(self):
        """Generate MFE Component Context template"""
        template = {
            "componentName": self.components[list(self.components.keys())[0]].name,
            "type": "container",
            "path": self.components[list(self.components.keys())[0]].path,
            "testId": self.components[list(self.components.keys())[0]].test_id,
            "children": self._format_children(self.components),
            "store": self._format_store(),
            "userInteractions": self._format_events(),
            "endpoints": self._format_endpoints()
        }

        with open(self.mfe_root / "data" / "manual_tests" / "mfe_component_context.md", "w") as f:
            f.write("# MFE Component Context Template\n\n")
            f.write("## Component Structure\n```json\n")
            json.dump(template, f, indent=4)
            f.write("\n```\n")

    def _generate_test_mapping(self):
        """Generate React Component Test Mapping template"""
        mapping = {
            self.components[list(self.components.keys())[0]].name: {
                "testScenarios": self._generate_test_scenarios(),
                "stateMapping": self._generate_state_mapping(),
                "eventSequences": self._generate_event_sequences()
            }
        }

        with open(self.mfe_root / "data" / "manual_tests" / "react_component_test_mapping.md", "w") as f:
            f.write("# React Component Test Mapping\n\n")
            f.write("## Component to Test Mapping\n```json\n")
            json.dump(mapping, f, indent=4)
            f.write("\n```\n")

    def _generate_framework_integration(self):
        """Generate Framework Integration template"""
        integration = {
            "mfeConfig": {
                "name": self.mfe_root.name,
                "type": "react",
                "version": self._get_package_version(),
                "dependencies": self._get_dependencies()
            },
            "discovery": {
                "patterns": {
                    "components": "src/components/**/*.{tsx,jsx}",
                    "tests": "src/**/*.test.{ts,tsx}",
                    "testData": "test_data/**/*.json"
                }
            },
            "generation": {
                "templates": {
                    "component": {
                        "source": "mfe_component_context.md",
                        "variables": ["componentName", "testId", "props"]
                    }
                }
            }
        }

        with open(self.mfe_root / "data" / "manual_tests" / "mfe_framework_integration.md", "w") as f:
            f.write("# MFE Framework Integration\n\n")
            f.write("## Framework Configuration\n```json\n")
            json.dump(integration, f, indent=4)
            f.write("\n```\n")

    # Helper methods for extraction
    def _extract_component_name(self, content: str) -> Optional[str]:
        pattern = r"export\s+(?:default\s+)?(?:const|function|class)\s+(\w+)"
        match = re.search(pattern, content)
        return match.group(1) if match else None

    def _extract_props(self, content: str) -> List[str]:
        pattern = r"interface\s+\w+Props\s*\{([^}]+)\}"
        match = re.search(pattern, content)
        if not match:
            return []
        props_content = match.group(1)
        return [prop.strip().split(':')[0].strip() for prop in props_content.split(';') if prop.strip()]

    def _extract_test_id(self, content: str) -> Optional[str]:
        pattern = r'data-testid=["\']([^"\']+)["\']'
        match = re.search(pattern, content)
        return match.group(1) if match else None

    def _extract_state_usage(self, content: str) -> Dict[str, dict]:
        state = {}
        # Extract useState hooks
        use_state_pattern = r"const\s+\[(\w+),\s*set\w+\]\s*=\s*useState[<\w+>]*\((.*)\)"
        for match in re.finditer(use_state_pattern, content):
            state[match.group(1)] = {
                "type": "local",
                "default": match.group(2)
            }
        # Extract useSelector hooks
        use_selector_pattern = r"useSelector\(\s*(?:state\s*=>\s*)?state\.(\w+)\.(\w+)"
        for match in re.finditer(use_selector_pattern, content):
            state[f"{match.group(1)}.{match.group(2)}"] = {
                "type": "redux",
                "selector": f"state.{match.group(1)}.{match.group(2)}"
            }
        return state

    def _format_children(self, components: Dict[str, ComponentInfo]) -> Dict[str, dict]:
        children = {}
        for name, info in components.items():
            if info.children:
                children[name] = {
                    "type": "component",
                    "testId": info.test_id,
                    "props": info.props,
                    "children": self._format_children(info.children)
                }
        return children

    def _format_store(self) -> Dict[str, dict]:
        return {
            "store": self.redux_store,
            "local": {
                name: info for name, info in 
                next(iter(self.components.values())).state.items() 
                if info["type"] == "local"
            }
        }

    def _format_events(self) -> Dict[str, dict]:
        events = {}
        for component in self.components.values():
            for event_name, event_info in component.events.items():
                events[event_name] = event_info
        return events

    def _format_endpoints(self) -> Dict[str, dict]:
        return self.api_endpoints

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate MFE templates from React components")
    parser.add_argument("mfe_root", help="Root directory of the MFE project")
    args = parser.parse_args()

    generator = MFETemplateGenerator(args.mfe_root)
    generator.analyze_mfe()
    generator.generate_templates() 
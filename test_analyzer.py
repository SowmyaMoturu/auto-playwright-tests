from pathlib import Path
import json
import re
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from enum import Enum
import ast

class TestLevel(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"

@dataclass
class ComponentCoverage:
    name: str
    unit_tests: List[str]
    integration_tests: List[str]
    e2e_tests: List[str]
    complexity: int  # Component complexity score
    data_dependencies: List[str]  # Data/state dependencies
    api_calls: List[str]  # API endpoints used
    user_interactions: List[str]  # User interaction points

@dataclass
class TestAnalysis:
    missing_coverage: List[str]
    test_placement_suggestions: Dict[str, TestLevel]
    refactoring_suggestions: List[str]
    pyramid_violations: List[str]

class TestAnalyzer:
    def __init__(self, mfe_paths: List[Path], automation_repo_path: Path):
        self.mfe_paths = [Path(p) for p in mfe_paths]
        self.automation_path = Path(automation_repo_path)
        self.component_coverage: Dict[str, ComponentCoverage] = {}
        self.test_pyramid_ratios = {
            TestLevel.UNIT: 0.70,  # 70% unit tests
            TestLevel.INTEGRATION: 0.20,  # 20% integration tests
            TestLevel.E2E: 0.10,  # 10% E2E tests
        }

    def analyze_test_coverage(self) -> TestAnalysis:
        """Analyze test coverage across all layers"""
        # Analyze MFE components and their unit tests
        self._analyze_mfe_components()
        
        # Analyze automation repo tests
        self._analyze_automation_tests()
        
        # Generate analysis and suggestions
        return self._generate_analysis()

    def _analyze_mfe_components(self):
        """Analyze React components and their unit tests"""
        for mfe_path in self.mfe_paths:
            for tsx_file in mfe_path.rglob("*.tsx"):
                if "node_modules" in str(tsx_file):
                    continue

                component_name = self._extract_component_name(tsx_file)
                if not component_name:
                    continue

                # Find corresponding test file
                test_file = self._find_test_file(tsx_file)
                
                # Analyze component complexity
                complexity = self._analyze_component_complexity(tsx_file)
                
                # Analyze dependencies
                dependencies = self._analyze_dependencies(tsx_file)
                
                # Analyze API calls
                api_calls = self._analyze_api_usage(tsx_file)
                
                # Analyze user interactions
                interactions = self._analyze_user_interactions(tsx_file)
                
                # Record coverage
                self.component_coverage[component_name] = ComponentCoverage(
                    name=component_name,
                    unit_tests=self._extract_unit_tests(test_file) if test_file else [],
                    integration_tests=[],  # Will be populated from automation repo
                    e2e_tests=[],  # Will be populated from automation repo
                    complexity=complexity,
                    data_dependencies=dependencies,
                    api_calls=api_calls,
                    user_interactions=interactions
                )

    def _analyze_automation_tests(self):
        """Analyze Playwright tests from automation repo"""
        # Analyze feature files
        feature_files = list(self.automation_path.rglob("*.feature"))
        
        for feature_file in feature_files:
            scenarios = self._extract_scenarios(feature_file)
            for scenario in scenarios:
                # Determine test type (integration or E2E)
                test_type = self._determine_test_type(scenario)
                
                # Find affected components
                components = self._find_affected_components(scenario)
                
                # Update component coverage
                for component in components:
                    if component in self.component_coverage:
                        if test_type == TestLevel.INTEGRATION:
                            self.component_coverage[component].integration_tests.append(str(feature_file))
                        else:
                            self.component_coverage[component].e2e_tests.append(str(feature_file))

    def _generate_analysis(self) -> TestAnalysis:
        """Generate test coverage analysis and suggestions"""
        missing_coverage = []
        test_placement = {}
        refactoring = []
        pyramid_violations = []

        # Analyze each component
        for name, coverage in self.component_coverage.items():
            # Check for missing coverage
            if not coverage.unit_tests:
                missing_coverage.append(f"{name}: Missing unit tests")
            if not coverage.integration_tests and coverage.complexity > 5:
                missing_coverage.append(f"{name}: Complex component missing integration tests")
            if not coverage.e2e_tests and len(coverage.user_interactions) > 3:
                missing_coverage.append(f"{name}: High user interaction component missing E2E tests")

            # Suggest test placement
            test_placement[name] = self._suggest_test_level(coverage)

            # Check for potential refactoring
            if coverage.complexity > 10:
                refactoring.append(f"{name}: Consider breaking down component (complexity: {coverage.complexity})")
            if len(coverage.data_dependencies) > 5:
                refactoring.append(f"{name}: Consider reducing data dependencies")

        # Analyze test pyramid ratios
        pyramid_violations.extend(self._analyze_test_pyramid())

        return TestAnalysis(
            missing_coverage=missing_coverage,
            test_placement_suggestions=test_placement,
            refactoring_suggestions=refactoring,
            pyramid_violations=pyramid_violations
        )

    def _suggest_test_level(self, coverage: ComponentCoverage) -> TestLevel:
        """Suggest appropriate test level based on component characteristics"""
        # Components with high user interaction and API calls should have E2E tests
        if len(coverage.user_interactions) > 3 and coverage.api_calls:
            return TestLevel.E2E
        
        # Complex components with data dependencies should have integration tests
        if coverage.complexity > 5 or len(coverage.data_dependencies) > 2:
            return TestLevel.INTEGRATION
        
        # Simple, pure components should have unit tests
        return TestLevel.UNIT

    def _analyze_test_pyramid(self) -> List[str]:
        """Analyze if test distribution follows the pyramid model"""
        violations = []
        
        total_tests = sum(
            len(c.unit_tests) + len(c.integration_tests) + len(c.e2e_tests)
            for c in self.component_coverage.values()
        )
        
        if total_tests == 0:
            return ["No tests found"]

        # Calculate actual ratios
        unit_ratio = sum(len(c.unit_tests) for c in self.component_coverage.values()) / total_tests
        integration_ratio = sum(len(c.integration_tests) for c in self.component_coverage.values()) / total_tests
        e2e_ratio = sum(len(c.e2e_tests) for c in self.component_coverage.values()) / total_tests

        # Check for violations
        if unit_ratio < self.test_pyramid_ratios[TestLevel.UNIT]:
            violations.append(f"Insufficient unit tests: {unit_ratio:.1%} vs target {self.test_pyramid_ratios[TestLevel.UNIT]:.1%}")
        if e2e_ratio > self.test_pyramid_ratios[TestLevel.E2E]:
            violations.append(f"Too many E2E tests: {e2e_ratio:.1%} vs target {self.test_pyramid_ratios[TestLevel.E2E]:.1%}")

        return violations

    # Helper methods for extraction and analysis
    def _extract_component_name(self, file_path: Path) -> Optional[str]:
        """Extract React component name from file"""
        pattern = r"export\s+(?:default\s+)?(?:const|function|class)\s+(\w+)"
        content = file_path.read_text()
        match = re.search(pattern, content)
        return match.group(1) if match else None

    def _analyze_component_complexity(self, file_path: Path) -> int:
        """Analyze component complexity based on various factors"""
        content = file_path.read_text()
        # Basic complexity metrics
        complexity = 0
        complexity += len(re.findall(r"if|else|for|while|switch|case", content))  # Control structures
        complexity += len(re.findall(r"useState|useEffect|useCallback|useMemo", content))  # Hooks
        complexity += len(re.findall(r"function", content))  # Functions
        return complexity

    def _analyze_dependencies(self, file_path: Path) -> List[str]:
        """Analyze component data dependencies"""
        content = file_path.read_text()
        dependencies = []
        # Find Redux selectors
        dependencies.extend(re.findall(r"useSelector\(\s*(?:state\s*=>\s*)?state\.(\w+)", content))
        # Find useState hooks
        dependencies.extend(re.findall(r"const\s+\[(\w+),", content))
        return dependencies

    def _analyze_api_usage(self, file_path: Path) -> List[str]:
        """Analyze API endpoints used by component"""
        content = file_path.read_text()
        # Find fetch/axios calls
        return re.findall(r"(?:fetch|axios\.get|axios\.post|axios\.put|axios\.delete)\(['\"]([^'\"]+)", content)

    def _analyze_user_interactions(self, file_path: Path) -> List[str]:
        """Analyze user interaction points"""
        content = file_path.read_text()
        # Find event handlers
        return re.findall(r"on(?:Click|Change|Submit|Input|Focus|Blur|KeyPress|MouseOver)=", content)

    def _find_test_file(self, component_file: Path) -> Optional[Path]:
        """Find corresponding test file for a component"""
        test_patterns = [
            component_file.parent / f"{component_file.stem}.test.tsx",
            component_file.parent / f"{component_file.stem}.spec.tsx",
            component_file.parent / "__tests__" / f"{component_file.stem}.test.tsx",
        ]
        return next((p for p in test_patterns if p.exists()), None)

    def _extract_scenarios(self, feature_file: Path) -> List[dict]:
        """Extract scenarios from feature file"""
        content = feature_file.read_text()
        scenarios = []
        current_scenario = None
        
        for line in content.split('\n'):
            if line.strip().startswith('Scenario:'):
                if current_scenario:
                    scenarios.append(current_scenario)
                current_scenario = {'name': line.split('Scenario:')[1].strip(), 'steps': []}
            elif current_scenario and line.strip().startswith(('Given', 'When', 'Then', 'And')):
                current_scenario['steps'].append(line.strip())
                
        if current_scenario:
            scenarios.append(current_scenario)
            
        return scenarios

    def _determine_test_type(self, scenario: dict) -> TestLevel:
        """Determine if a scenario is integration or E2E test"""
        # Check for API calls or multiple component interactions
        steps = ' '.join(scenario['steps']).lower()
        if 'api' in steps or 'request' in steps or 'response' in steps:
            return TestLevel.INTEGRATION
        return TestLevel.E2E

    def _find_affected_components(self, scenario: dict) -> Set[str]:
        """Find components affected by a test scenario"""
        affected = set()
        steps = ' '.join(scenario['steps']).lower()
        
        # Match steps with component names and interactions
        for component in self.component_coverage.keys():
            component_lower = component.lower()
            if component_lower in steps:
                affected.add(component)
            
        return affected

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Analyze test coverage across MFEs and automation repo")
    parser.add_argument("--mfe-paths", nargs="+", required=True, help="Paths to MFE projects")
    parser.add_argument("--automation-path", required=True, help="Path to automation repo")
    args = parser.parse_args()

    analyzer = TestAnalyzer(args.mfe_paths, args.automation_path)
    analysis = analyzer.analyze_test_coverage()

    print("\n=== Test Coverage Analysis ===")
    
    if analysis.missing_coverage:
        print("\nMissing Coverage:")
        for item in analysis.missing_coverage:
            print(f"- {item}")
    
    print("\nTest Placement Suggestions:")
    for component, level in analysis.test_placement_suggestions.items():
        print(f"- {component}: {level.value}")
    
    if analysis.refactoring_suggestions:
        print("\nRefactoring Suggestions:")
        for suggestion in analysis.refactoring_suggestions:
            print(f"- {suggestion}")
    
    if analysis.pyramid_violations:
        print("\nTest Pyramid Violations:")
        for violation in analysis.pyramid_violations:
            print(f"- {violation}") 
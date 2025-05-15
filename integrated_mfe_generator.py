from pathlib import Path
import json
from typing import Dict, List, Optional
from generate_mfe_templates import MFETemplateGenerator as ExistingTemplateAnalyzer
from genai_template_generator import GenAITemplateGenerator, TemplateType

class IntegratedMFEGenerator:
    def __init__(self, mfe_root: Path, openai_api_key: str):
        self.analyzer = ExistingTemplateAnalyzer(mfe_root)
        self.generator = GenAITemplateGenerator(openai_api_key)
        self.mfe_root = mfe_root

    def generate_integrated_template(self, output_path: Path, framework: TemplateType):
        # First analyze existing MFE
        self.analyzer.analyze_mfe()
        
        # Extract features from analysis
        features = self._extract_features_from_analysis()
        
        # Extract testing requirements
        testing_requirements = self._extract_testing_requirements()
        
        # Generate new template using AI
        return self.generator.generate_mfe_template(
            output_path=output_path,
            framework=framework,
            features=features,
            testing_requirements=testing_requirements
        )

    def _extract_features_from_analysis(self) -> List[str]:
        """Extract features from existing MFE analysis"""
        features = []
        
        # Add features based on Redux usage
        if self.analyzer.redux_store:
            features.append("state-management")
        
        # Add features based on API endpoints
        if self.analyzer.api_endpoints:
            features.append("api-integration")
        
        # Add features based on component analysis
        for component in self.analyzer.components.values():
            if component.events:
                features.append("event-handling")
            if component.test_id:
                features.append("testable-components")
        
        return list(set(features))  # Remove duplicates

    def _extract_testing_requirements(self) -> Dict[str, any]:
        """Extract testing requirements from existing MFE"""
        return {
            "framework": "jest",  # Common in React projects
            "testIds": True if any(c.test_id for c in self.analyzer.components.values()) else False,
            "componentTests": True,
            "coverage": {
                "statements": 80,
                "branches": 80,
                "functions": 80,
                "lines": 80
            }
        }

if __name__ == "__main__":
    import argparse
    from dotenv import load_dotenv
    
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Generate integrated MFE templates")
    parser.add_argument("mfe_root", help="Root directory of the existing MFE project")
    parser.add_argument("output_path", help="Output path for the new template")
    parser.add_argument("--framework", choices=[t.value for t in TemplateType], 
                       default="react", help="Frontend framework")
    args = parser.parse_args()
    
    generator = IntegratedMFEGenerator(
        Path(args.mfe_root),
        os.getenv("OPENAI_API_KEY")
    )
    
    template = generator.generate_integrated_template(
        Path(args.output_path),
        TemplateType(args.framework)
    )
    
    print("\n=== Integrated MFE Template Generated ===")
    print(f"\nOutput Path: {args.output_path}")
    print("\nFeatures detected and included:")
    for feature in generator._extract_features_from_analysis():
        print(f"- {feature}") 
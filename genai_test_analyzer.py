from pathlib import Path
import json
import re
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
from enum import Enum
import ast
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from test_analyzer import TestAnalyzer, TestLevel, ComponentCoverage, TestAnalysis

class AITestSuggestion(BaseModel):
    test_description: str = Field(description="Description of the test to be created")
    test_level: TestLevel = Field(description="Suggested test level (unit/integration/e2e)")
    priority: int = Field(description="Priority (1-5, where 1 is highest)")
    rationale: str = Field(description="Explanation for why this test is needed")
    implementation_hints: List[str] = Field(description="Hints for implementing the test")

class AIRefactoringSuggestion(BaseModel):
    component: str = Field(description="Component name")
    suggestion: str = Field(description="Refactoring suggestion")
    impact: str = Field(description="Impact on test coverage")
    implementation_approach: str = Field(description="How to implement the refactoring")

class GenAITestAnalyzer(TestAnalyzer):
    def __init__(self, mfe_paths: List[Path], automation_repo_path: Path, openai_api_key: str):
        super().__init__(mfe_paths, automation_repo_path)
        self.llm = ChatOpenAI(
            temperature=0.2,
            model="gpt-4",
            openai_api_key=openai_api_key
        )
        self._setup_prompts()

    def _setup_prompts(self):
        """Setup prompt templates for different analysis tasks"""
        self.test_suggestion_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a senior test automation architect. Analyze the component and suggest tests.
            Consider:
            1. Component complexity and responsibilities
            2. User interactions and UI elements
            3. Data flow and state management
            4. API integrations
            5. Test pyramid principles
            6. Existing test coverage"""),
            ("human", """Component Info:
            {component_info}
            
            Existing Coverage:
            {existing_coverage}
            
            Suggest a test that would improve coverage.""")
        ])

        self.refactoring_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a senior React architect. Analyze the component and suggest refactoring to improve testability.
            Consider:
            1. Component complexity
            2. Dependencies and coupling
            3. State management
            4. Testing challenges
            5. Best practices"""),
            ("human", """Component Analysis:
            {component_analysis}
            
            Current Testing Issues:
            {testing_issues}
            
            Suggest refactoring to improve testability.""")
        ])

    def analyze_with_ai(self) -> Dict[str, List]:
        """Perform AI-enhanced analysis"""
        # First do regular analysis
        base_analysis = self.analyze_test_coverage()
        
        # Enhance with AI suggestions
        ai_suggestions = {
            "test_suggestions": self._generate_ai_test_suggestions(base_analysis),
            "refactoring_suggestions": self._generate_ai_refactoring_suggestions(base_analysis),
            "test_strategy": self._generate_test_strategy()
        }
        
        return ai_suggestions

    def _generate_ai_test_suggestions(self, base_analysis: TestAnalysis) -> List[AITestSuggestion]:
        """Generate AI-powered test suggestions"""
        suggestions = []
        parser = PydanticOutputParser(pydantic_object=AITestSuggestion)

        for component_name, coverage in self.component_coverage.items():
            # Prepare component info
            component_info = {
                "name": component_name,
                "complexity": coverage.complexity,
                "dependencies": coverage.data_dependencies,
                "api_calls": coverage.api_calls,
                "user_interactions": coverage.user_interactions
            }

            # Prepare coverage info
            existing_coverage = {
                "unit_tests": len(coverage.unit_tests),
                "integration_tests": len(coverage.integration_tests),
                "e2e_tests": len(coverage.e2e_tests)
            }

            # Get AI suggestion
            response = self.llm.predict_messages([
                ("system", "Suggest a test based on the component analysis."),
                ("human", f"Component: {json.dumps(component_info)}\nCoverage: {json.dumps(existing_coverage)}")
            ])

            try:
                suggestion = parser.parse(response.content)
                suggestions.append(suggestion)
            except Exception as e:
                print(f"Error parsing suggestion for {component_name}: {e}")

        return suggestions

    def _generate_ai_refactoring_suggestions(self, base_analysis: TestAnalysis) -> List[AIRefactoringSuggestion]:
        """Generate AI-powered refactoring suggestions"""
        suggestions = []
        parser = PydanticOutputParser(pydantic_object=AIRefactoringSuggestion)

        for component_name, coverage in self.component_coverage.items():
            if coverage.complexity > 5 or len(coverage.data_dependencies) > 3:
                # Prepare analysis
                component_analysis = {
                    "name": component_name,
                    "complexity": coverage.complexity,
                    "dependencies": coverage.data_dependencies,
                    "api_calls": coverage.api_calls
                }

                testing_issues = [
                    issue for issue in base_analysis.missing_coverage 
                    if component_name in issue
                ]

                # Get AI suggestion
                response = self.llm.predict_messages([
                    ("system", "Suggest refactoring to improve testability."),
                    ("human", f"Component: {json.dumps(component_analysis)}\nIssues: {json.dumps(testing_issues)}")
                ])

                try:
                    suggestion = parser.parse(response.content)
                    suggestions.append(suggestion)
                except Exception as e:
                    print(f"Error parsing refactoring suggestion for {component_name}: {e}")

        return suggestions

    def _generate_test_strategy(self) -> str:
        """Generate overall test strategy recommendations"""
        # Prepare summary of current state
        summary = {
            "components": len(self.component_coverage),
            "total_unit_tests": sum(len(c.unit_tests) for c in self.component_coverage.values()),
            "total_integration_tests": sum(len(c.integration_tests) for c in self.component_coverage.values()),
            "total_e2e_tests": sum(len(c.e2e_tests) for c in self.component_coverage.values()),
            "complex_components": sum(1 for c in self.component_coverage.values() if c.complexity > 5),
            "api_dependent_components": sum(1 for c in self.component_coverage.values() if c.api_calls)
        }

        # Get AI recommendation
        response = self.llm.predict_messages([
            ("system", """As a test architect, provide a strategic recommendation for improving test coverage.
            Consider:
            1. Test pyramid balance
            2. Resource allocation
            3. Priority areas
            4. Implementation approach
            5. Timeline and phases"""),
            ("human", f"Current Test State: {json.dumps(summary)}")
        ])

        return response.content

if __name__ == "__main__":
    import argparse
    import os
    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser(description="AI-Enhanced test coverage analysis")
    parser.add_argument("--mfe-paths", nargs="+", required=True, help="Paths to MFE projects")
    parser.add_argument("--automation-path", required=True, help="Path to automation repo")
    args = parser.parse_args()

    analyzer = GenAITestAnalyzer(
        args.mfe_paths, 
        args.automation_path,
        os.getenv("OPENAI_API_KEY")
    )
    
    analysis = analyzer.analyze_with_ai()

    print("\n=== AI-Enhanced Test Analysis ===")
    
    print("\nTest Suggestions:")
    for suggestion in analysis["test_suggestions"]:
        print(f"\n- {suggestion.test_description}")
        print(f"  Level: {suggestion.test_level.value}")
        print(f"  Priority: {suggestion.priority}")
        print(f"  Rationale: {suggestion.rationale}")
        print("  Implementation Hints:")
        for hint in suggestion.implementation_hints:
            print(f"    * {hint}")
    
    print("\nRefactoring Suggestions:")
    for suggestion in analysis["refactoring_suggestions"]:
        print(f"\n- Component: {suggestion.component}")
        print(f"  Suggestion: {suggestion.suggestion}")
        print(f"  Impact: {suggestion.impact}")
        print(f"  Approach: {suggestion.implementation_approach}")
    
    print("\nTest Strategy:")
    print(analysis["test_strategy"]) 
from pathlib import Path
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os
import shutil

class TemplateType(str, Enum):
    REACT = "react"
    VUE = "vue"
    ANGULAR = "angular"

class ComponentTemplate(BaseModel):
    name: str = Field(description="Name of the component")
    code: str = Field(description="Component code")
    styles: Optional[str] = Field(description="Component styles")
    tests: str = Field(description="Component tests")
    dependencies: List[str] = Field(description="Required dependencies")

class MFETemplate(BaseModel):
    structure: Dict[str, str] = Field(description="Directory and file structure")
    config_files: Dict[str, str] = Field(description="Configuration files content")
    base_components: List[ComponentTemplate] = Field(description="Base components to include")
    setup_instructions: List[str] = Field(description="Setup and installation instructions")

class GenAITemplateGenerator:
    def __init__(self, openai_api_key: str):
        self.llm = ChatOpenAI(
            temperature=0.2,
            model="gpt-4",
            openai_api_key=openai_api_key
        )
        self._setup_prompts()

    def _setup_prompts(self):
        """Setup prompt templates for different generation tasks"""
        self.structure_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a senior frontend architect specializing in micro-frontend architecture.
            Create a well-structured MFE template considering:
            1. Modern best practices
            2. Scalability
            3. Maintainability
            4. Testing setup
            5. Build optimization
            6. Development workflow"""),
            ("human", """Template Requirements:
            Framework: {framework}
            Features: {features}
            Testing Requirements: {testing_requirements}
            
            Generate a complete MFE template structure.""")
        ])

        self.component_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a senior frontend developer. Create reusable component templates.
            Consider:
            1. Component best practices
            2. Accessibility
            3. Performance
            4. Testing
            5. Documentation"""),
            ("human", """Component Requirements:
            Name: {name}
            Type: {component_type}
            Features: {features}
            
            Generate a component template.""")
        ])

    def generate_mfe_template(
        self,
        output_path: Path,
        framework: TemplateType,
        features: List[str],
        testing_requirements: Dict[str, any]
    ) -> MFETemplate:
        """Generate a complete MFE template"""
        
        # Get template structure from AI
        response = self.llm.predict_messages([
            ("system", "Generate MFE template structure"),
            ("human", f"""
            Framework: {framework.value}
            Features: {json.dumps(features)}
            Testing: {json.dumps(testing_requirements)}
            """)
        ])

        parser = PydanticOutputParser(pydantic_object=MFETemplate)
        template = parser.parse(response.content)

        # Create the template structure
        self._create_template_structure(output_path, template)
        
        return template

    def _create_template_structure(self, base_path: Path, template: MFETemplate):
        """Create the physical template structure"""
        # Create directories
        for path, description in template.structure.items():
            full_path = base_path / path
            full_path.mkdir(parents=True, exist_ok=True)
            (full_path / 'README.md').write_text(description)

        # Create config files
        for filename, content in template.config_files.items():
            (base_path / filename).write_text(content)

        # Create base components
        components_path = base_path / 'src' / 'components'
        components_path.mkdir(parents=True, exist_ok=True)
        
        for component in template.base_components:
            component_path = components_path / component.name
            component_path.mkdir(exist_ok=True)
            
            # Write component files
            (component_path / f'{component.name}.tsx').write_text(component.code)
            if component.styles:
                (component_path / f'{component.name}.styles.ts').write_text(component.styles)
            (component_path / f'{component.name}.test.tsx').write_text(component.tests)

        # Write setup instructions
        (base_path / 'SETUP.md').write_text('\n'.join(template.setup_instructions))

    def generate_component_template(
        self,
        name: str,
        component_type: str,
        features: List[str]
    ) -> ComponentTemplate:
        """Generate a single component template"""
        
        response = self.llm.predict_messages([
            ("system", "Generate component template"),
            ("human", f"""
            Name: {name}
            Type: {component_type}
            Features: {json.dumps(features)}
            """)
        ])

        parser = PydanticOutputParser(pydantic_object=ComponentTemplate)
        return parser.parse(response.content)

if __name__ == "__main__":
    import argparse
    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser(description="Generate MFE templates using GenAI")
    parser.add_argument("--output-path", required=True, help="Output path for the template")
    parser.add_argument("--framework", choices=[t.value for t in TemplateType], required=True, help="Frontend framework")
    parser.add_argument("--features", nargs="+", default=[], help="Required features")
    parser.add_argument("--testing-config", type=str, help="Path to testing configuration JSON")
    args = parser.parse_args()

    generator = GenAITemplateGenerator(os.getenv("OPENAI_API_KEY"))

    # Load testing config
    testing_requirements = {}
    if args.testing_config:
        with open(args.testing_config) as f:
            testing_requirements = json.load(f)

    template = generator.generate_mfe_template(
        Path(args.output_path),
        TemplateType(args.framework),
        args.features,
        testing_requirements
    )

    print("\n=== MFE Template Generated ===")
    print(f"\nOutput Path: {args.output_path}")
    print("\nSetup Instructions:")
    for instruction in template.setup_instructions:
        print(f"- {instruction}") 
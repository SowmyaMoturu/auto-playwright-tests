from pathlib import Path
import yaml
from typing import Dict, Optional
from dataclasses import dataclass
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

@dataclass
class TestGenerationInput:
    manual_test: dict
    framework_config: dict
    har_data: Optional[dict] = None
    dom_snapshot: Optional[dict] = None

@dataclass
class GeneratedFeature:
    content: str
    metadata: dict  # Stores technical details extracted from manual test

def load_prompt(prompt_file: Path) -> str:
    """Load prompt template from file"""
    return prompt_file.read_text()

def extract_technical_details(manual_test: dict) -> dict:
    """Extract technical implementation details from manual test"""
    technical_details = {
        "api_endpoints": [],
        "validation_rules": {},
        "formatting_rules": {},
        "test_data": {},
        "error_scenarios": []
    }
    
    # Extract API endpoints
    if "API Details" in manual_test:
        for line in manual_test["API Details"].split("\n"):
            if "Endpoint:" in line:
                technical_details["api_endpoints"].append(
                    line.split("Endpoint:")[1].strip()
                )
    
    # Extract validation rules
    if "Validation Rules" in manual_test:
        for line in manual_test["Validation Rules"].split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                technical_details["validation_rules"][key.strip()] = value.strip()
    
    # Extract formatting rules
    if "Data Format" in manual_test:
        for line in manual_test["Data Format"].split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                technical_details["formatting_rules"][key.strip()] = value.strip()
    
    return technical_details

def generate_feature_file(
    input_data: TestGenerationInput,
    feature_prompt_template: str
) -> GeneratedFeature:
    """Generate feature file from manual test"""
    
    # Initialize LLM chain
    llm = ChatOpenAI(temperature=0.2)
    prompt = PromptTemplate(
        template=feature_prompt_template,
        input_variables=["manual_test"]
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Generate feature file
    feature_content = chain.predict(
        manual_test=yaml.dump(input_data.manual_test)
    )
    
    # Extract technical details for step definition generation
    technical_details = extract_technical_details(input_data.manual_test)
    
    return GeneratedFeature(
        content=feature_content,
        metadata=technical_details
    )

def generate_step_definitions(
    feature: GeneratedFeature,
    input_data: TestGenerationInput,
    step_prompt_template: str
) -> str:
    """Generate step definitions using both feature and manual test details"""
    
    # Initialize LLM chain
    llm = ChatOpenAI(temperature=0.2)
    prompt = PromptTemplate(
        template=step_prompt_template,
        input_variables=["feature_file", "technical_details", "framework_config"]
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Generate step definitions
    return chain.predict(
        feature_file=feature.content,
        technical_details=yaml.dump(feature.metadata),
        framework_config=yaml.dump(input_data.framework_config)
    )

def generate_test_components(
    manual_test_path: Path,
    framework_config_path: Path,
    prompts_dir: Path
) -> tuple[str, str]:
    """Main function to generate test components"""
    
    # Load inputs
    with open(manual_test_path) as f:
        manual_test = yaml.safe_load(f)
    
    with open(framework_config_path) as f:
        framework_config = yaml.safe_load(f)
    
    input_data = TestGenerationInput(
        manual_test=manual_test,
        framework_config=framework_config
    )
    
    # Load prompts
    feature_prompt = load_prompt(prompts_dir / "feature_file_prompt.md")
    step_prompt = load_prompt(prompts_dir / "step_definition_prompt.md")
    
    # Generate feature file with technical details
    feature = generate_feature_file(input_data, feature_prompt)
    
    # Generate step definitions using both feature and technical details
    step_definitions = generate_step_definitions(
        feature,
        input_data,
        step_prompt
    )
    
    return feature.content, step_definitions 
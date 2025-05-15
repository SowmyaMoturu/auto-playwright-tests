from pathlib import Path
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import yaml
import os
from .test_generation_manager import TestGenerationManager, TestComponents

from utils.framework_analyzer import FrameworkAnalysis


@dataclass
class TestComponents:
    feature_file: str
    step_definitions: str
    page_objects: Dict[str, str]
    page_objects_updates: Optional[str] = None


def load_manual_test(path: str) -> dict:
    """Load manual test from file"""
    with open(path) as f:
        return yaml.safe_load(f)


def load_har_data(path: Optional[str]) -> Optional[dict]:
    """Load HAR recording data if available"""
    if not path or not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def load_dom_snapshot(path: Optional[str]) -> Optional[dict]:
    """Load DOM snapshot data if available"""
    if not path or not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def load_prompts() -> Dict[str, str]:
    """Load all prompt templates"""
    prompts_dir = Path("prompts")
    return {
        "feature": (prompts_dir / "feature_file_prompt.md").read_text(),
        "step_definition": (prompts_dir / "step_definition_prompt.md").read_text(),
        "test_generation": (prompts_dir / "test_generation_prompt.md").read_text()
    }


def generate_feature_file(
    manual_test: dict,
    llm_chain: LLMChain,
    prompts: Dict[str, str]
) -> str:
    """Generate feature file content"""
    feature_prompt = PromptTemplate(
        template=prompts["feature"],
        input_variables=["manual_test"]
    )
    feature_chain = LLMChain(llm=llm_chain.llm, prompt=feature_prompt)
    return feature_chain.predict(manual_test=yaml.dump(manual_test))


def generate_step_definitions(
    manual_test: dict,
    framework_analysis: FrameworkAnalysis,
    llm_chain: LLMChain,
    prompts: Dict[str, str],
    har_data: Optional[dict] = None,
    dom_snapshot: Optional[dict] = None
) -> str:
    """Generate step definitions"""
    step_prompt = PromptTemplate(
        template=prompts["step_definition"],
        input_variables=["manual_test", "framework_analysis", "har_data", "dom_snapshot"]
    )
    step_chain = LLMChain(llm=llm_chain.llm, prompt=step_prompt)
    return step_chain.predict(
        manual_test=yaml.dump(manual_test),
        framework_analysis=yaml.dump(framework_analysis),
        har_data=yaml.dump(har_data) if har_data else "None",
        dom_snapshot=yaml.dump(dom_snapshot) if dom_snapshot else "None"
    )


def generate_page_objects(
    manual_test: dict,
    framework_analysis: FrameworkAnalysis,
    llm_chain: LLMChain,
    prompts: Dict[str, str],
    dom_snapshot: Optional[dict] = None
) -> Dict[str, str]:
    """Generate page objects"""
    page_prompt = PromptTemplate(
        template=prompts["test_generation"],
        input_variables=["manual_test", "framework_analysis", "dom_snapshot"]
    )
    page_chain = LLMChain(llm=llm_chain.llm, prompt=page_prompt)
    page_objects_content = page_chain.predict(
        manual_test=yaml.dump(manual_test),
        framework_analysis=yaml.dump(framework_analysis),
        dom_snapshot=yaml.dump(dom_snapshot) if dom_snapshot else "None"
    )
    
    # Parse the generated content into individual page objects
    pages = {}
    current_page = []
    current_name = None
    
    for line in page_objects_content.split('\n'):
        if line.startswith('// PAGE:'):
            if current_name and current_page:
                pages[current_name] = '\n'.join(current_page)
                current_page = []
            current_name = line[8:].strip()
        else:
            current_page.append(line)
            
    if current_name and current_page:
        pages[current_name] = '\n'.join(current_page)
        
    return pages


def update_page_objects_file(
    framework_analysis: FrameworkAnalysis,
    new_pages: Dict[str, str],
    llm_chain: LLMChain,
    prompts: Dict[str, str]
) -> Optional[str]:
    """Generate updates for PageObjects.ts"""
    if not new_pages:
        return None
        
    update_prompt = PromptTemplate(
        template=prompts["test_generation"],
        input_variables=["framework_analysis", "new_pages"]
    )
    update_chain = LLMChain(llm=llm_chain.llm, prompt=update_prompt)
    return update_chain.predict(
        framework_analysis=yaml.dump(framework_analysis),
        new_pages=yaml.dump(new_pages)
    )


def generate_feature_and_steps(
    manual_test_path: str,
    framework_analysis: dict,
    project_id: Optional[str] = None,
    location: str = "us-central1"
) -> TestComponents:
    """Main function to generate test components using Codey API"""
    # Get GCP project ID from environment if not provided
    if not project_id:
        project_id = os.getenv('GCP_PROJECT_ID')
        if not project_id:
            raise ValueError("GCP_PROJECT_ID must be provided either as an argument or environment variable")
    
    # Load manual test
    manual_test = load_manual_test(manual_test_path)
    
    # Load related files if available
    har_path = manual_test.get('Related Files', '').split('HAR Recording: ')[1].split('\n')[0].strip('[]') if 'Related Files' in manual_test else None
    dom_path = manual_test.get('Related Files', '').split('DOM Snapshot: ')[1].split('\n')[0].strip('[]') if 'Related Files' in manual_test else None
    
    har_data = load_har_data(har_path)
    dom_snapshot = load_dom_snapshot(dom_path)
    
    # Initialize test generation manager
    manager = TestGenerationManager(project_id=project_id, location=location)
    
    # Generate components
    feature_content = manager.generate_feature_file(manual_test)
    step_definitions = manager.generate_step_definitions(
        manual_test, framework_analysis, har_data, dom_snapshot
    )
    page_objects = manager.generate_page_objects(
        manual_test, framework_analysis, dom_snapshot
    )
    
    return TestComponents(
        feature_file=feature_content,
        step_definitions=step_definitions,
        page_objects=page_objects
    )

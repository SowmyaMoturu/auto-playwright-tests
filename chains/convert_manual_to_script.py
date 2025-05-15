from pathlib import Path
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import yaml

from utils.framework_analyzer import FrameworkAnalysis


@dataclass
class TestComponents:
    feature_file: str
    step_definitions: str
    page_objects: Dict[str, str]
    page_objects_updates: Optional[str] = None


def load_manual_test(file_path: str) -> dict:
    """Load and parse manual test file"""
    content = Path(file_path).read_text()
    
    # Parse markdown sections
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split('\n'):
        if line.startswith('## '):
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
                current_content = []
            current_section = line[3:].strip()
        else:
            current_content.append(line)
            
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
        
    return sections


def load_har_data(har_path: str) -> Optional[dict]:
    """Load HAR recording if available"""
    try:
        return json.loads(Path(har_path).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def load_dom_snapshot(snapshot_path: str) -> Optional[dict]:
    """Load DOM snapshot if available"""
    try:
        return json.loads(Path(snapshot_path).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


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
    framework_analysis: FrameworkAnalysis
) -> TestComponents:
    """Main function to generate test components"""
    # Load manual test
    manual_test = load_manual_test(manual_test_path)
    
    # Load prompts
    prompts = load_prompts()
    
    # Load related files if available
    har_path = manual_test.get('Related Files', '').split('HAR Recording: ')[1].split('\n')[0].strip('[]') if 'Related Files' in manual_test else None
    dom_path = manual_test.get('Related Files', '').split('DOM Snapshot: ')[1].split('\n')[0].strip('[]') if 'Related Files' in manual_test else None
    
    har_data = load_har_data(har_path) if har_path else None
    dom_snapshot = load_dom_snapshot(dom_path) if dom_path else None
    
    # Initialize LLM chain
    llm = ChatOpenAI(temperature=0.2)
    base_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate(template="{text}", input_variables=["text"])
    )
    
    # Generate components
    feature_content = generate_feature_file(manual_test, base_chain, prompts)
    step_definitions = generate_step_definitions(
        manual_test, framework_analysis, base_chain, prompts, har_data, dom_snapshot
    )
    page_objects = generate_page_objects(
        manual_test, framework_analysis, base_chain, prompts, dom_snapshot
    )
    page_objects_updates = update_page_objects_file(
        framework_analysis, page_objects, base_chain, prompts
    )
    
    return TestComponents(
        feature_file=feature_content,
        step_definitions=step_definitions,
        page_objects=page_objects,
        page_objects_updates=page_objects_updates
    )

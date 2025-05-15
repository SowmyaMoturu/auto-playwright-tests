import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from utils.codey_client import CodeyClient

@dataclass
class TestComponents:
    feature_file: str
    step_definitions: str
    page_objects: Dict[str, str]
    page_objects_updates: Optional[Dict[str, str]] = None

class TestGenerationManager:
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.codey_client = CodeyClient(
            project_id=project_id,
            location=location,
            max_output_tokens=1024,
            temperature=0.2
        )
        self.prompts = {}
        self.load_prompts()

    def load_prompts(self):
        """Load all prompt templates"""
        prompts_dir = Path("prompts")
        for prompt_file in prompts_dir.glob("*.md"):
            self.prompts[prompt_file.stem] = prompt_file.read_text()

    def generate_feature_file(self, manual_test: dict) -> str:
        """Generate feature file in chunks if needed"""
        system_prompt = "You are a test automation expert. Generate a Cucumber feature file from the manual test instructions."
        
        # Break manual test into logical sections if too large
        sections = self._split_manual_test(manual_test)
        
        # Generate feature file content for each section
        feature_contents = self.codey_client.predict_in_chunks(
            system_prompt=system_prompt,
            user_messages=[
                f"{self.prompts['feature_file']}\n\nManual Test Section:\n{yaml.dump(section)}"
                for section in sections
            ]
        )
        
        # Combine feature file contents
        return self._combine_feature_contents(feature_contents)

    def generate_step_definitions(self, 
                                manual_test: dict,
                                framework_analysis: dict,
                                har_data: Optional[dict] = None,
                                dom_snapshot: Optional[dict] = None) -> str:
        """Generate step definitions in chunks"""
        system_prompt = "You are a test automation expert. Generate Playwright step definitions from the test scenario."
        
        # Break down into smaller chunks based on scenarios
        scenarios = self._extract_scenarios(manual_test)
        
        # Generate step definitions for each scenario
        step_contents = self.codey_client.predict_in_chunks(
            system_prompt=system_prompt,
            user_messages=[
                f"{self.prompts['step_definition']}\n\n"
                f"Scenario:\n{yaml.dump(scenario)}\n"
                f"Framework Analysis:\n{yaml.dump(framework_analysis)}\n"
                f"HAR Data:\n{yaml.dump(har_data) if har_data else 'None'}\n"
                f"DOM Snapshot:\n{yaml.dump(dom_snapshot) if dom_snapshot else 'None'}"
                for scenario in scenarios
            ]
        )
        
        # Combine step definitions
        return self._combine_step_definitions(step_contents)

    def generate_page_objects(self,
                            manual_test: dict,
                            framework_analysis: dict,
                            dom_snapshot: Optional[dict] = None) -> Dict[str, str]:
        """Generate page objects in chunks if needed"""
        system_prompt = "You are a test automation expert. Generate Playwright page objects from the test scenario."
        
        # Extract pages and their elements
        pages = self._extract_pages(manual_test, dom_snapshot)
        
        # Generate page objects for each page
        page_contents = {}
        for page_name, page_data in pages.items():
            content = self.codey_client.predict(
                system_prompt=system_prompt,
                user_message=f"{self.prompts['page_object']}\n\n"
                            f"Page:\n{yaml.dump(page_data)}\n"
                            f"Framework Analysis:\n{yaml.dump(framework_analysis)}"
            )
            page_contents[page_name] = content
            
        return page_contents

    def _split_manual_test(self, manual_test: dict) -> List[dict]:
        """Split manual test into smaller chunks if needed"""
        # If manual test is small enough, return as single chunk
        if len(yaml.dump(manual_test)) < 2000:
            return [manual_test]
            
        sections = []
        current_section = {}
        
        for key, value in manual_test.items():
            current_section[key] = value
            if len(yaml.dump(current_section)) >= 2000:
                sections.append(current_section)
                current_section = {}
                
        if current_section:
            sections.append(current_section)
            
        return sections

    def _extract_scenarios(self, manual_test: dict) -> List[dict]:
        """Extract individual scenarios from manual test"""
        scenarios = []
        
        if 'Scenarios' in manual_test:
            scenarios.extend(manual_test['Scenarios'])
        else:
            # If no explicit scenarios, treat whole test as one scenario
            scenarios.append(manual_test)
            
        return scenarios

    def _extract_pages(self, manual_test: dict, dom_snapshot: Optional[dict]) -> Dict[str, dict]:
        """Extract page information from manual test and DOM snapshot"""
        pages = {}
        
        # Extract from manual test
        if 'Pages' in manual_test:
            pages.update(manual_test['Pages'])
            
        # Extract from DOM snapshot if available
        if dom_snapshot:
            for page_name, elements in dom_snapshot.items():
                if page_name not in pages:
                    pages[page_name] = {'elements': elements}
                else:
                    pages[page_name]['elements'] = elements
                    
        return pages

    def _combine_feature_contents(self, contents: List[str]) -> str:
        """Combine feature file contents from multiple chunks"""
        combined = []
        for content in contents:
            # Remove duplicate Feature: lines except first one
            if combined and content.startswith("Feature:"):
                content = content[content.find("\n")+1:]
            combined.append(content)
        return "\n".join(combined)

    def _combine_step_definitions(self, contents: List[str]) -> str:
        """Combine step definitions from multiple chunks"""
        combined = []
        imports = set()
        
        for content in contents:
            # Extract and deduplicate imports
            lines = content.split("\n")
            for line in lines:
                if line.startswith("import ") or line.startswith("from "):
                    imports.add(line)
                else:
                    combined.append(line)
                    
        # Combine with imports at top
        return "\n".join(sorted(imports)) + "\n\n" + "\n".join(combined) 
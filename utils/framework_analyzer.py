from pathlib import Path
from typing import Dict, List, Optional, Set
import re
import ast
from dataclasses import dataclass

from config import FrameworkConfig


@dataclass
class PageObjectInfo:
    name: str
    locators: Dict[str, str]
    methods: List[str]
    extends_base: bool
    getter_name: str  # Name of the getter in PageObjects.ts


@dataclass
class FrameworkAnalysis:
    base_page_methods: List[str]
    world_context_properties: List[str]
    page_objects: Dict[str, PageObjectInfo]
    common_patterns: Dict[str, str]
    page_getters: Dict[str, str]  # Mapping of page name to getter method


class FrameworkAnalyzer:
    def __init__(self, config: FrameworkConfig):
        self.config = config
        self._existing_page_getters: Dict[str, str] = {}

    def analyze_framework(self) -> FrameworkAnalysis:
        """Analyze the framework structure and return insights"""
        # First analyze PageObjects.ts to get existing getters
        self._analyze_page_objects_file()
        
        base_methods = self._analyze_base_page()
        world_props = self._analyze_world_context()
        page_objects = self._analyze_page_objects()
        patterns = self._extract_common_patterns()
        
        return FrameworkAnalysis(
            base_page_methods=base_methods,
            world_context_properties=world_props,
            page_objects=page_objects,
            common_patterns=patterns,
            page_getters=self._existing_page_getters
        )

    def _analyze_page_objects_file(self) -> None:
        """Analyze PageObjects.ts to extract existing page getters"""
        if not self.config.page_objects_file or not self.config.page_objects_file.exists():
            return
        
        content = self.config.page_objects_file.read_text()
        
        # Extract getter methods for pages
        getter_pattern = r'static\s+get\s+(\w+)\s*\(\)\s*{\s*return\s+new\s+(\w+)'
        matches = re.findall(getter_pattern, content)
        
        for getter_name, page_class in matches:
            self._existing_page_getters[page_class] = getter_name

    def _analyze_base_page(self) -> List[str]:
        """Extract common methods from base page"""
        if not self.config.base_page_path or not self.config.base_page_path.exists():
            return []
        
        methods = []
        content = self.config.base_page_path.read_text()
        
        # Extract method names using regex
        method_pattern = r'async\s+(\w+)\s*\([^)]*\)\s*{'
        methods = re.findall(method_pattern, content)
        return methods

    def _analyze_world_context(self) -> List[str]:
        """Analyze world.ts to understand shared context"""
        if not self.config.world_context_path or not self.config.world_context_path.exists():
            return []
        
        properties = []
        content = self.config.world_context_path.read_text()
        
        # Extract properties from World interface/class
        prop_pattern = r'(\w+):\s*[^;]+;'
        properties = re.findall(prop_pattern, content)
        return properties

    def _analyze_page_objects(self) -> Dict[str, PageObjectInfo]:
        """Analyze all page objects to understand structure"""
        page_objects = {}
        
        if not self.config.page_objects_dir.exists():
            return page_objects

        for page_file in self.config.page_objects_dir.glob("*.ts"):
            if page_file.name == "base_page.ts" or page_file.name == "PageObjects.ts":
                continue
                
            content = page_file.read_text()
            
            # Extract class name
            class_pattern = r'export\s+class\s+(\w+)'
            class_matches = re.findall(class_pattern, content)
            if not class_matches:
                continue
                
            class_name = class_matches[0]
            
            # Extract locators
            locator_pattern = r'export\s+const\s+(\w+)\s*=\s*[\'"]([^\'"]+)[\'"]'
            locators = dict(re.findall(locator_pattern, content))
            
            # Extract methods
            method_pattern = r'async\s+(\w+)\s*\([^)]*\)\s*{'
            methods = re.findall(method_pattern, content)
            
            # Check if extends BasePage
            extends_base = "extends BasePage" in content
            
            # Get or generate getter name
            getter_name = self._existing_page_getters.get(
                class_name,
                f"get{class_name}"  # Default getter name if not found
            )
            
            page_objects[class_name] = PageObjectInfo(
                name=class_name,
                locators=locators,
                methods=methods,
                extends_base=extends_base,
                getter_name=getter_name
            )
            
        return page_objects

    def _extract_common_patterns(self) -> Dict[str, str]:
        """Extract common patterns and conventions used in the framework"""
        patterns = {
            "locator_style": self._detect_locator_style(),
            "method_naming": self._detect_method_naming_convention(),
            "file_structure": self._detect_file_structure_pattern()
        }
        return patterns

    def _detect_locator_style(self) -> str:
        """Always return data-testid as the preferred locator style"""
        return "data-testid"

    def _detect_method_naming_convention(self) -> str:
        """Detect the method naming convention used"""
        return "camelCase"

    def _detect_file_structure_pattern(self) -> str:
        """Detect the file organization pattern"""
        return "page-object-model" 
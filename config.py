from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class FrameworkConfig:
    """Framework configuration using relative paths from repo root"""
    features_dir: Path = Path("src/features")
    step_definitions_dir: Path = Path("src/step-definitions")
    page_objects_dir: Path = Path("src/pages")
    base_page_path: Optional[Path] = Path("src/pages/base_page.ts")
    world_context_path: Optional[Path] = Path("src/step-definitions/world.ts")
    page_objects_file: Optional[Path] = Path("src/pages/PageObjects.ts")

    @classmethod
    def from_base_path(cls, base_path: str | Path):
        """Create config instance with all paths relative to base_path"""
        return cls()


def load_framework_config(framework_path: str | Path) -> FrameworkConfig:
    """Load framework configuration from the specified path"""
    return FrameworkConfig.from_base_path(framework_path) 
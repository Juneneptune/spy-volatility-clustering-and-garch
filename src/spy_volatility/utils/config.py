# src/spy_volatility/utils/config.py

from pathlib import Path
from typing import Any, Dict

import yaml

def get_project_root() -> Path:
    """
    Get the root directory of the project.
    """
    # From src/spy_volatility/utils/config.py, go up 3 levels to project root
    project_root = Path(__file__).parents[3]
    print(f"[config] Project root: {project_root}")
    return project_root

def load_config(config_name: str = "default.yaml") -> Dict[str, Any]:
    """
    Load a YAML config from the configs/ directory at the project root.

    Returns a nested dict, e.g. cfg["data"]["spy_ticker"].
    """
    project_root = get_project_root()
    config_path = project_root / "configs" / config_name

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)
    
    if cfg is None:
        raise ValueError(f"Config file {config_path} is empty or invalid")
    
    return cfg
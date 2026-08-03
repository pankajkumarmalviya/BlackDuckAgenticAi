"""Utility functions for BlackDuck AI Command"""

import os
import json
import uuid
from pathlib import Path
from typing import Dict, Any
from .logger import get_logger

logger = get_logger(__name__)


def validate_project_path(path: str) -> bool:
    """
    Validate that project path exists and is readable

    Args:
        path: Project path to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        p = Path(path).expanduser()
        if not p.exists():
            logger.error(f"Project path does not exist: {p}")
            return False
        if not p.is_dir():
            logger.error(f"Project path is not a directory: {p}")
            return False
        if not os.access(p, os.R_OK):
            logger.error(f"Project path is not readable: {p}")
            return False
        logger.debug(f"Project path validated: {p}")
        return True
    except Exception as e:
        logger.error(f"Error validating project path: {str(e)}")
        return False


def generate_uuid() -> str:
    """
    Generate a unique UUID for scan identification

    Returns:
        UUID string
    """
    scan_uuid = str(uuid.uuid4())
    logger.debug(f"Generated UUID: {scan_uuid}")
    return scan_uuid


def load_json_template(template_path: str) -> Dict[str, Any]:
    """
    Load JSON template from file

    Args:
        template_path: Path to template file

    Returns:
        Parsed JSON data

    Raises:
        FileNotFoundError: If template file doesn't exist
        json.JSONDecodeError: If template is invalid JSON
    """
    try:
        p = Path(template_path).expanduser()
        if not p.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")

        with open(p, "r") as f:
            data = json.load(f)
        logger.debug(f"Loaded template from {template_path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in template {template_path}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error loading template: {str(e)}")
        raise


def replace_variables(data: Dict[str, Any], variables: Dict[str, str]) -> Dict[str, Any]:
    """
    Replace ${VAR} placeholders with actual values recursively

    Args:
        data: Dictionary or nested structure with placeholders
        variables: Mapping of variable names to values

    Returns:
        Data structure with variables replaced
    """

    def replace_recursive(obj: Any) -> Any:
        """Recursively replace variables in any object"""
        if isinstance(obj, dict):
            return {k: replace_recursive(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [replace_recursive(item) for item in obj]
        elif isinstance(obj, str):
            result = obj
            for var_name, var_value in variables.items():
                placeholder = f"${{{var_name}}}"
                if placeholder in result:
                    result = result.replace(placeholder, str(var_value))
                    logger.debug(f"Replaced {placeholder} in string")
            return result
        return obj

    logger.debug(f"Replacing variables: {list(variables.keys())}")
    return replace_recursive(data)


def ensure_directory(path: str) -> Path:
    """
    Create directory if it doesn't exist

    Args:
        path: Directory path to create

    Returns:
        Path object

    Raises:
        OSError: If directory cannot be created
    """
    try:
        p = Path(path).expanduser()
        p.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directory ensured: {p}")
        return p
    except OSError as e:
        logger.error(f"Error creating directory {path}: {str(e)}")
        raise


def save_json_file(data: Dict[str, Any], file_path: str) -> str:
    """
    Save dictionary to JSON file with proper permissions

    Args:
        data: Dictionary to save
        file_path: Output file path

    Returns:
        Path to saved file

    Raises:
        IOError: If file cannot be written
    """
    try:
        p = Path(file_path).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)

        with open(p, "w") as f:
            json.dump(data, f, indent=2)

        # Set restrictive permissions (read/write for owner only)
        os.chmod(p, 0o600)
        logger.debug(f"JSON file saved with secure permissions: {p}")
        return str(p)
    except IOError as e:
        logger.error(f"Error saving JSON file {file_path}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error saving JSON file: {str(e)}")
        raise


def read_json_file(file_path: str) -> Dict[str, Any]:
    """
    Read JSON file from disk

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON data

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is invalid JSON
    """
    try:
        p = Path(file_path).expanduser()
        if not p.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(p, "r") as f:
            data = json.load(f)
        logger.debug(f"Read JSON file: {p}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {file_path}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error reading JSON file: {str(e)}")
        raise


def mask_sensitive_data(text: str, tokens: Dict[str, str]) -> str:
    """
    Mask sensitive tokens in text for logging

    Args:
        text: Text containing potential tokens
        tokens: Mapping of token names to values

    Returns:
        Text with tokens masked as ***
    """
    result = text
    for token_name, token_value in tokens.items():
        if token_value:
            result = result.replace(token_value, "***")
    return result

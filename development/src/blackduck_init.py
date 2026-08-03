"""Core BlackDuck initialization module - Platform agnostic"""

import os
from pathlib import Path
from typing import Tuple

from .types import BlackDuckInitInput, BlackDuckInitOutput
from .utils import (
    validate_project_path,
    generate_uuid,
    load_json_template,
    replace_variables,
    ensure_directory,
    save_json_file,
    read_json_file,
)
from .bridge_executor import execute_bridge_cli
from .logger import get_logger

logger = get_logger(__name__)


class BlackDuckInitializer:
    """Core logic for BlackDuck initialization"""

    def __init__(self):
        """Initialize the BlackDuck initializer"""
        # Get template path relative to this file
        project_root = Path(__file__).parent.parent
        self.template_path = str(project_root / "templates" / "input.json")
        self.input_dir = str(project_root / "input")
        self.output_dir = str(project_root / "output")

        # Ensure directories exist
        try:
            ensure_directory(self.input_dir)
            ensure_directory(self.output_dir)
            logger.info("BlackDuckInitializer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize directories: {str(e)}")
            raise

    def validate_inputs(self, input_data: BlackDuckInitInput) -> Tuple[bool, str]:
        """
        Validate all required inputs

        Args:
            input_data: Input parameters to validate

        Returns:
            Tuple of (valid: bool, message: str)
        """
        logger.info("Validating inputs...")

        # Validate project path
        if not validate_project_path(input_data.project_path):
            error_msg = f"Invalid project path: {input_data.project_path}"
            return False, error_msg

        # Validate polaris token
        if not input_data.polaris_token or len(input_data.polaris_token) < 10:
            error_msg = "Polaris token is required and must be at least 10 characters"
            return False, error_msg

        # Validate server URL (should start with https://)
        if not input_data.server_url.startswith("https://"):
            error_msg = "Server URL must start with https://"
            return False, error_msg

        logger.info("Input validation passed")
        return True, "Valid"

    def initialize(self, input_data: BlackDuckInitInput) -> BlackDuckInitOutput:
        """
        Main initialization logic

        Steps:
        1. Validate inputs
        2. Generate UUID
        3. Load input.json template
        4. Replace variables
        5. Save input.json
        6. Execute Bridge CLI
        7. Read output.json
        8. Return results

        Args:
            input_data: Input parameters

        Returns:
            BlackDuckInitOutput with results
        """
        logger.info("Starting BlackDuck initialization")

        try:
            # Step 1: Validate
            valid, msg = self.validate_inputs(input_data)
            if not valid:
                logger.error(f"Validation failed: {msg}")
                return BlackDuckInitOutput(
                    success=False,
                    message=msg,
                    error=msg,
                )

            # Step 2: Generate UUID
            scan_uuid = generate_uuid()
            logger.info(f"Generated scan UUID: {scan_uuid}")

            # Step 3: Load template
            try:
                template = load_json_template(self.template_path)
                logger.info("Loaded input.json template")
            except FileNotFoundError as e:
                error_msg = f"Template file not found: {str(e)}"
                logger.error(error_msg)
                return BlackDuckInitOutput(
                    success=False,
                    message=error_msg,
                    error=error_msg,
                )

            # Step 4: Replace variables
            variables = {
                "UUID": scan_uuid,
                "PROJECT_PATH": input_data.project_path,
                "POLARIS_TOKEN": input_data.polaris_token,
                "SERVER_URL": input_data.server_url,
                "API_TOKEN": input_data.api_token or "",
                "INCLUDE_DEV_DEPS": str(input_data.include_dev_deps).lower(),
            }

            input_data_replaced = replace_variables(template, variables)
            logger.info("Replaced template variables")

            # Step 5: Save input.json
            input_file = os.path.join(self.input_dir, f"input_{scan_uuid}.json")
            try:
                input_file = save_json_file(input_data_replaced, input_file)
                logger.info(f"Saved input JSON: {input_file}")
            except IOError as e:
                error_msg = f"Failed to save input file: {str(e)}"
                logger.error(error_msg)
                return BlackDuckInitOutput(
                    success=False,
                    message=error_msg,
                    error=error_msg,
                )

            # Step 6: Execute Bridge CLI
            logger.info("Executing Bridge CLI...")
            success, output_info, output_data = execute_bridge_cli(
                input_data.project_path,
                input_file,
                scan_uuid,
            )

            if not success:
                error_msg = output_info
                logger.error(f"Bridge CLI execution failed: {error_msg}")
                return BlackDuckInitOutput(
                    success=False,
                    message="Bridge CLI execution failed",
                    error=error_msg,
                )

            output_file = output_info

            # Step 7: Verify output
            try:
                if not os.path.exists(output_file):
                    error_msg = f"Output file not found: {output_file}"
                    logger.error(error_msg)
                    return BlackDuckInitOutput(
                        success=False,
                        message=error_msg,
                        error=error_msg,
                    )
            except Exception as e:
                error_msg = f"Error accessing output file: {str(e)}"
                logger.error(error_msg)
                return BlackDuckInitOutput(
                    success=False,
                    message=error_msg,
                    error=error_msg,
                )

            # Step 8: Return results
            logger.info(f"BlackDuck initialization successful. Scan ID: {scan_uuid}")
            return BlackDuckInitOutput(
                success=True,
                message="BlackDuck initialization successful",
                scan_id=scan_uuid,
                config_path=input_file,
                output_file=output_file,
                details=output_data,
            )

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return BlackDuckInitOutput(
                success=False,
                message="Unexpected error occurred",
                error=error_msg,
            )


def blackduck_init(input_data: BlackDuckInitInput) -> BlackDuckInitOutput:
    """
    Entry point for blackduck_init command

    Args:
        input_data: Input parameters

    Returns:
        BlackDuckInitOutput with results
    """
    initializer = BlackDuckInitializer()
    return initializer.initialize(input_data)

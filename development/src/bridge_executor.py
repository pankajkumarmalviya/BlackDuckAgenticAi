"""Bridge CLI execution module"""

import subprocess
import os
import json
from pathlib import Path
from typing import Tuple
from .logger import get_logger

logger = get_logger(__name__)

# Default Bridge CLI path
DEFAULT_BRIDGE_CLI_PATH = os.getenv("BRIDGE_CLI_PATH", "bridge-cli")


class BridgeExecutor:
    """Handles Bridge CLI execution"""

    def __init__(self, bridge_cli_path: str = DEFAULT_BRIDGE_CLI_PATH):
        """
        Initialize Bridge executor

        Args:
            bridge_cli_path: Path to bridge-cli executable
        """
        self.bridge_cli_path = bridge_cli_path

    def execute(
        self,
        project_path: str,
        input_json_path: str,
        scan_uuid: str,
    ) -> Tuple[bool, str, dict]:
        """
        Execute Bridge CLI command with exact specification

        Command: bridge-cli {project_path} --stage polaris --input input.json \\
                 --out {project_path}/output/output_{UUID}.json --diagnostics

        Args:
            project_path: Path to project being scanned
            input_json_path: Path to input.json configuration
            scan_uuid: Unique scan identifier

        Returns:
            Tuple of (success: bool, output_file: str, output_data: dict)
        """
        logger.info(f"Starting Bridge CLI execution for project: {project_path}")

        # Create output directory
        output_dir = os.path.join(project_path, "output")
        try:
            os.makedirs(output_dir, exist_ok=True)
            logger.debug(f"Output directory ready: {output_dir}")
        except OSError as e:
            error_msg = f"Failed to create output directory: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, {}

        # Build output file path
        output_file = os.path.join(output_dir, f"output_{scan_uuid}.json")

        # Build Bridge CLI command
        command = [
            self.bridge_cli_path,
            project_path,
            "--stage",
            "polaris",
            "--input",
            input_json_path,
            "--out",
            output_file,
            "--diagnostics",
        ]

        logger.info(f"Bridge CLI command: {' '.join(command)}")

        try:
            # Execute Bridge CLI with timeout
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )

            logger.debug(f"Bridge CLI return code: {result.returncode}")

            if result.returncode != 0:
                error_msg = result.stderr or result.stdout
                logger.error(f"Bridge CLI execution failed: {error_msg}")
                return False, error_msg, {}

            # Check if output file was created
            if not os.path.exists(output_file):
                error_msg = f"Output file not created: {output_file}"
                logger.error(error_msg)
                return False, error_msg, {}

            # Read and parse output
            try:
                with open(output_file, "r") as f:
                    output_data = json.load(f)
                logger.info(f"Bridge CLI succeeded. Output file: {output_file}")
                return True, output_file, output_data
            except json.JSONDecodeError as e:
                error_msg = f"Invalid JSON in output file: {str(e)}"
                logger.error(error_msg)
                return False, error_msg, {}

        except subprocess.TimeoutExpired:
            error_msg = "Bridge CLI execution timeout (5 minutes exceeded)"
            logger.error(error_msg)
            return False, error_msg, {}
        except FileNotFoundError:
            error_msg = f"Bridge CLI not found: {self.bridge_cli_path}"
            logger.error(error_msg)
            return False, error_msg, {}
        except Exception as e:
            error_msg = f"Bridge CLI execution error: {str(e)}"
            logger.error(error_msg)
            return False, error_msg, {}


def execute_bridge_cli(
    project_path: str,
    input_json_path: str,
    scan_uuid: str,
) -> Tuple[bool, str, dict]:
    """
    Helper function to execute Bridge CLI

    Args:
        project_path: Path to project
        input_json_path: Path to input.json
        scan_uuid: Scan UUID

    Returns:
        Tuple of (success, output_file_or_error, output_data)
    """
    executor = BridgeExecutor()
    return executor.execute(project_path, input_json_path, scan_uuid)

"""Unit tests for Bridge CLI executor"""

import pytest
import tempfile
import json
from pathlib import Path

from src.bridge_executor import BridgeExecutor, execute_bridge_cli


class TestBridgeExecutor:
    """Tests for BridgeExecutor class"""

    def test_executor_initialization(self):
        """Test BridgeExecutor can be initialized"""
        executor = BridgeExecutor("/usr/bin/bridge-cli")
        assert executor.bridge_cli_path == "/usr/bin/bridge-cli"

    def test_executor_default_path(self):
        """Test BridgeExecutor uses default path when not specified"""
        executor = BridgeExecutor()
        assert executor.bridge_cli_path is not None

    def test_execute_bridge_cli_not_found(self):
        """Test execute fails gracefully when Bridge CLI not found"""
        executor = BridgeExecutor("/nonexistent/bridge-cli")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a fake input file
            input_file = Path(tmpdir) / "input.json"
            input_file.write_text('{"test": "data"}')

            success, output, data = executor.execute(tmpdir, str(input_file), "test-uuid")

            assert success is False
            assert "Bridge CLI not found" in output or "No such file" in output or "not found" in output.lower()

    def test_execute_creates_output_directory(self):
        """Test that execute creates output directory if missing"""
        executor = BridgeExecutor("/usr/bin/bridge-cli")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            assert not output_dir.exists()

            # Create fake input file
            input_file = Path(tmpdir) / "input.json"
            input_file.write_text('{"test": "data"}')

            # Call execute (will fail because bridge-cli doesn't exist)
            executor.execute(tmpdir, str(input_file), "test-uuid")

            # Output directory should be created
            assert output_dir.exists()


class TestExecuteBridgeCliFunction:
    """Tests for execute_bridge_cli function"""

    def test_execute_bridge_cli_returns_tuple(self):
        """Test execute_bridge_cli returns proper tuple"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = Path(tmpdir) / "input.json"
            input_file.write_text('{"test": "data"}')

            result = execute_bridge_cli(tmpdir, str(input_file), "test-uuid")

            assert isinstance(result, tuple)
            assert len(result) == 3
            assert isinstance(result[0], bool)  # success
            assert isinstance(result[1], str)   # output file or error
            assert isinstance(result[2], dict)  # output data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

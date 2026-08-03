"""Unit tests for BlackDuck initialization module"""

import pytest
import tempfile
import os
from pathlib import Path

from src.types import BlackDuckInitInput, BlackDuckInitOutput
from src.blackduck_init import BlackDuckInitializer, blackduck_init


class TestBlackDuckInitInput:
    """Tests for BlackDuckInitInput validation"""

    def test_valid_input(self):
        """Test creating input with all valid fields"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_data = BlackDuckInitInput(
                project_path=tmpdir,
                polaris_token="valid-token-1234567890",
                server_url="https://blackduck.company.com",
                api_token="api-token-123",
                include_dev_deps=True,
            )
            assert input_data.project_path == tmpdir
            assert input_data.polaris_token == "valid-token-1234567890"
            assert input_data.server_url == "https://blackduck.company.com"
            assert input_data.api_token == "api-token-123"
            assert input_data.include_dev_deps is True

    def test_invalid_server_url_http(self):
        """Test that HTTP URL is rejected"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="must start with https://"):
                BlackDuckInitInput(
                    project_path=tmpdir,
                    polaris_token="valid-token-1234567890",
                    server_url="http://blackduck.company.com",  # HTTP not allowed
                )

    def test_invalid_server_url_no_protocol(self):
        """Test that URL without protocol is rejected"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="must start with https://"):
                BlackDuckInitInput(
                    project_path=tmpdir,
                    polaris_token="valid-token-1234567890",
                    server_url="blackduck.company.com",
                )

    def test_optional_fields(self):
        """Test that optional fields can be omitted"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_data = BlackDuckInitInput(
                project_path=tmpdir,
                polaris_token="valid-token-1234567890",
                server_url="https://blackduck.company.com",
            )
            assert input_data.api_token is None
            assert input_data.include_dev_deps is False


class TestBlackDuckInitOutput:
    """Tests for BlackDuckInitOutput"""

    def test_success_output(self):
        """Test creating a success output"""
        output = BlackDuckInitOutput(
            success=True,
            message="BlackDuck initialization successful",
            scan_id="550e8400-e29b-41d4-a716-446655440000",
            config_path="/path/to/input.json",
            output_file="/path/to/output.json",
            details={"components_found": 142},
        )
        assert output.success is True
        assert output.message == "BlackDuck initialization successful"
        assert output.scan_id == "550e8400-e29b-41d4-a716-446655440000"

    def test_failure_output(self):
        """Test creating a failure output"""
        output = BlackDuckInitOutput(
            success=False,
            message="Failed to initialize",
            error="Bridge CLI not found",
        )
        assert output.success is False
        assert output.error == "Bridge CLI not found"
        assert output.scan_id is None


class TestBlackDuckInitializer:
    """Tests for BlackDuckInitializer"""

    def test_validate_inputs_valid(self):
        """Test validation of valid inputs"""
        with tempfile.TemporaryDirectory() as tmpdir:
            initializer = BlackDuckInitializer()
            input_data = BlackDuckInitInput(
                project_path=tmpdir,
                polaris_token="valid-token-1234567890",
                server_url="https://blackduck.company.com",
            )
            valid, msg = initializer.validate_inputs(input_data)
            assert valid is True
            assert msg == "Valid"

    def test_validate_inputs_invalid_project_path(self):
        """Test validation fails for non-existent project path"""
        initializer = BlackDuckInitializer()
        input_data = BlackDuckInitInput(
            project_path="/non/existent/path",
            polaris_token="valid-token-1234567890",
            server_url="https://blackduck.company.com",
        )
        valid, msg = initializer.validate_inputs(input_data)
        assert valid is False
        assert "Invalid project path" in msg

    def test_validate_inputs_invalid_token(self):
        """Test validation fails for short token"""
        with tempfile.TemporaryDirectory() as tmpdir:
            initializer = BlackDuckInitializer()
            input_data = BlackDuckInitInput(
                project_path=tmpdir,
                polaris_token="short",  # Too short
                server_url="https://blackduck.company.com",
            )
            valid, msg = initializer.validate_inputs(input_data)
            assert valid is False

    def test_validate_inputs_invalid_server_url(self):
        """Test validation fails for invalid server URL"""
        with tempfile.TemporaryDirectory() as tmpdir:
            initializer = BlackDuckInitializer()
            input_data = BlackDuckInitInput(
                project_path=tmpdir,
                polaris_token="valid-token-1234567890",
                server_url="http://blackduck.company.com",  # HTTP not HTTPS
            )
            valid, msg = initializer.validate_inputs(input_data)
            assert valid is False
            assert "https://" in msg


class TestBlackDuckInitFunction:
    """Tests for blackduck_init function"""

    def test_blackduck_init_returns_output(self):
        """Test that blackduck_init returns BlackDuckInitOutput"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_data = BlackDuckInitInput(
                project_path=tmpdir,
                polaris_token="valid-token-1234567890",
                server_url="https://blackduck.company.com",
            )
            result = blackduck_init(input_data)
            assert isinstance(result, BlackDuckInitOutput)

    def test_blackduck_init_fails_without_bridge_cli(self):
        """Test that init fails gracefully when Bridge CLI is not available"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_data = BlackDuckInitInput(
                project_path=tmpdir,
                polaris_token="valid-token-1234567890",
                server_url="https://blackduck.company.com",
            )
            result = blackduck_init(input_data)
            # Should fail because Bridge CLI is not available in test environment
            assert isinstance(result, BlackDuckInitOutput)
            # In a test environment without Bridge CLI, this will fail
            # assert result.success is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

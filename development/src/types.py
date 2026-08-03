"""Type definitions for BlackDuck AI Command"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class BlackDuckInitInput(BaseModel):
    """Input parameters for /blackduck-init command"""

    project_path: str = Field(
        ...,
        description="Path to the project directory",
        example="/Users/me/myapp"
    )
    polaris_token: str = Field(
        ...,
        description="User-specific Polaris authentication token",
        min_length=10
    )
    server_url: str = Field(
        ...,
        description="BlackDuck Hub server URL (must be HTTPS)",
        example="https://blackduck.company.com"
    )
    api_token: Optional[str] = Field(
        None,
        description="BlackDuck API authentication token",
        default=None
    )
    include_dev_deps: bool = Field(
        False,
        description="Include development dependencies in scan",
        default=False
    )

    @field_validator("server_url")
    @classmethod
    def validate_server_url(cls, v: str) -> str:
        """Validate server URL is HTTPS"""
        if not v.startswith("https://"):
            raise ValueError("Server URL must start with https://")
        return v


class BlackDuckInitOutput(BaseModel):
    """Output response from /blackduck-init command"""

    success: bool = Field(
        ...,
        description="Whether the initialization was successful"
    )
    message: str = Field(
        ...,
        description="Human-readable status message"
    )
    scan_id: Optional[str] = Field(
        None,
        description="Unique scan identifier (UUID)",
        example="550e8400-e29b-41d4-a716-446655440000"
    )
    config_path: Optional[str] = Field(
        None,
        description="Path to generated input.json configuration",
        example="/Users/me/myapp/input/input_550e8400-e29b-41d4-a716-446655440000.json"
    )
    output_file: Optional[str] = Field(
        None,
        description="Path to output.json with scan results",
        example="/Users/me/myapp/output/output_550e8400-e29b-41d4-a716-446655440000.json"
    )
    error: Optional[str] = Field(
        None,
        description="Error message if initialization failed"
    )
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional details about the scan",
        example={
            "project_name": "myapp",
            "scan_status": "completed",
            "components_found": 142,
            "vulnerabilities": {
                "critical": 2,
                "high": 8,
                "medium": 15,
                "low": 22
            }
        }
    )

    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "BlackDuck initialization successful",
                "scan_id": "550e8400-e29b-41d4-a716-446655440000",
                "config_path": "/Users/me/myapp/input/input_550e8400-e29b-41d4-a716-446655440000.json",
                "output_file": "/Users/me/myapp/output/output_550e8400-e29b-41d4-a716-446655440000.json",
                "details": {
                    "project_name": "myapp",
                    "components_found": 142
                }
            }
        }

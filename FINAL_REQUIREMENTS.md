# BlackDuck AI Command - Final Requirements Document

**Version**: 1.0  
**Date**: August 3, 2024  
**Status**: ✅ APPROVED FOR DEVELOPMENT  

---

## 📋 Executive Summary

**Project**: BlackDuck AI Command (`/blackduck-init`)

**Objective**: Create a platform-agnostic Python MCP server that enables users to initialize BlackDuck security scanning via Bridge CLI through Claude Code, with extensibility for other AI platforms.

**Scope**: 
- Phase 1 (MVP): Python MCP Server + CLI tool
- Phase 2+: REST API, Copilot integration, ChatGPT plugin

**Tech Stack**: Python 3.10+, MCP Protocol, Click CLI

**Timeline**: 4 weeks

---

## 🎯 Business Requirements

### Goals
1. Democratize BlackDuck security scanning via AI assistants
2. Reduce friction - one command instead of manual setup
3. Support multiple AI platforms (Claude primary, others follow)
4. Open source and community-driven

### Target Users
- Software engineers using Claude Code
- DevOps engineers in CI/CD pipelines
- Security teams enforcing scanning standards
- Copilot users (Phase 2)
- ChatGPT users (Phase 3)

---

## 📌 Functional Requirements

### 1.1 Core Command: `/blackduck-init`

**Purpose**: Initialize BlackDuck security scanning for a project using Bridge CLI

**Input Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `project_path` | string | YES | - | Path to project directory (e.g., `/Users/me/myapp` or `~/myproject`) |
| `polaris_token` | string | YES | - | User-specific Polaris authentication token |
| `server_url` | string | YES | - | BlackDuck Hub server URL (must be HTTPS) |
| `api_token` | string | NO | - | BlackDuck API authentication token |
| `include_dev_deps` | boolean | NO | false | Include development dependencies in scan |

**Output (Success)**:

```json
{
  "success": true,
  "message": "BlackDuck initialization successful",
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "config_path": "/Users/me/myapp/input/input_550e8400-e29b-41d4-a716-446655440000.json",
  "output_file": "/Users/me/myapp/output/output_550e8400-e29b-41d4-a716-446655440000.json",
  "details": {
    "project_name": "myapp",
    "scan_status": "completed",
    "components_found": 142,
    "vulnerabilities": {
      "critical": 2,
      "high": 8,
      "medium": 15,
      "low": 22
    },
    "timestamp": "2024-08-03T17:04:00Z"
  }
}
```

**Output (Failure)**:

```json
{
  "success": false,
  "message": "Failed to execute Bridge CLI",
  "error": "Bridge CLI not found in PATH",
  "details": null
}
```

---

### 1.2 Bridge CLI Execution

**Bridge CLI Download URL**:
```
https://artifactory.tools.duckutil.net/artifactory/clops-local/integrations/bridge/binaries/bridge-cli-bundle
```

**Exact Bridge CLI Command**:

```bash
bridge-cli {project_path} --stage polaris --input input.json --out {project_path}/output/output_{UUID}.json --diagnostics
```

**Command Parameter Details**:

| Parameter | Value | Description |
|-----------|-------|-------------|
| Program | `bridge-cli` | Bridge CLI executable |
| Positional 1 | `{project_path}` | Path to project being scanned (replaced at runtime) |
| Flag | `--stage polaris` | Scan stage (fixed value) |
| Flag | `--input input.json` | Input configuration file path |
| Flag | `--out` | Output file path (with {UUID} replaced) |
| Flag | `--diagnostics` | Enable diagnostic logging |

**Example Execution**:

```bash
bridge-cli /Users/me/myapp \
  --stage polaris \
  --input input.json \
  --out /Users/me/myapp/output/output_550e8400-e29b-41d4-a716-446655440000.json \
  --diagnostics
```

---

## 📂 Input/Output File Specifications

### 2.1 Input File (input.json)

**Location**: `development/input/input_{UUID}.json`

**Template** (`development/templates/input.json`):

```json
{
  "scan_id": "${UUID}",
  "project_path": "${PROJECT_PATH}",
  "polaris": {
    "token": "${POLARIS_TOKEN}",
    "server_url": "${SERVER_URL}"
  },
  "blackduck": {
    "api_token": "${API_TOKEN}",
    "include_dev_deps": ${INCLUDE_DEV_DEPS}
  },
  "correlation_id": "${UUID}",
  "diagnostics": true
}
```

**Variable Replacement**:

| Placeholder | Runtime Value | Example |
|-------------|---------------|---------|
| `${UUID}` | Generated UUID | `550e8400-e29b-41d4-a716-446655440000` |
| `${PROJECT_PATH}` | User's project path | `/Users/me/myapp` |
| `${POLARIS_TOKEN}` | User's Polaris token | `xyz-token-123` |
| `${SERVER_URL}` | BlackDuck server URL | `https://blackduck.company.com` |
| `${API_TOKEN}` | User's API token (optional) | `abc-api-token-456` |
| `${INCLUDE_DEV_DEPS}` | Boolean flag | `true` or `false` |

**Generated Example** (After replacement):

```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "project_path": "/Users/me/myapp",
  "polaris": {
    "token": "xyz-token-123",
    "server_url": "https://blackduck.company.com"
  },
  "blackduck": {
    "api_token": "abc-api-token-456",
    "include_dev_deps": false
  },
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "diagnostics": true
}
```

### 2.2 Output File (output.json)

**Location**: `{project_path}/output/output_{UUID}.json`

**Format**:

```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "message": "BlackDuck scan completed successfully",
  "details": {
    "project_name": "myapp",
    "scan_status": "completed",
    "components_found": 142,
    "vulnerabilities": {
      "critical": 2,
      "high": 8,
      "medium": 15,
      "low": 22
    },
    "timestamp": "2024-08-03T17:04:00Z"
  }
}
```

---

## 🏗️ System Architecture

### 3.1 Data Flow

```
User Input
    ↓
Claude Code or CLI
    ↓
/blackduck-init command
    ↓
Input Validation
    ↓
UUID Generation
    ↓
Load input.json template
    ↓
Replace variables (UUID, tokens, paths)
    ↓
Save input.json to development/input/
    ↓
Execute Bridge CLI
    ↓
Bridge CLI reads input.json
    ↓
Bridge CLI writes output.json to {project_path}/output/
    ↓
Read output.json
    ↓
Return results to user
    ↓
User sees success/failure
```

### 3.2 Module Architecture

```
blackduck_init.py (Core Logic - Platform Agnostic)
├── validate_inputs()
├── generate_uuid()
├── load_template()
├── replace_variables()
└── execute_bridge_cli()
    ├── bridge_executor.py
    │   ├── build_command()
    │   ├── run_subprocess()
    │   └── read_output()
    └── utils.py
        ├── file_operations()
        ├── json_handling()
        └── path_validation()

Adapters:
├── mcp_server.py (Claude Code)
│   └── Wraps blackduck_init.py as MCP tool
│
├── cli.py (Command Line)
│   └── Wraps blackduck_init.py with Click
│
└── [Phase 2] rest_server.py (REST API)
    └── Wraps blackduck_init.py with Flask/FastAPI
```

---

## ⚙️ Implementation Details

### 4.1 Platform Support (Phase 1 MVP)

| Platform | Technology | Status | Entry Point |
|----------|-----------|--------|------------|
| Claude Code | MCP Server | Primary | `mcp_server.py` |
| CLI/Terminal | Click CLI | Primary | `cli.py` |
| Copilot | REST API | Phase 2 | `rest_server.py` |
| ChatGPT | ChatGPT Plugin | Phase 3 | REST API |
| Gemini | REST API | Phase 3 | REST API |

### 4.2 Project Structure

```
BlackDuckAgenticAi/
├── WORKFLOW.html                          # Visual diagram
├── SDLC.md                               # SDLC phases
├── REQUIREMENTS.md                        # Original requirements
├── FINAL_REQUIREMENTS.md                 # This file
├── BRIDGE_CLI_COMMAND.md                 # Command reference
├── IMPLEMENTATION_PLAN.md                # Implementation plan
├── README.md                             # Main docs (to create)
├── LICENSE                               # MIT License (to create)
├── .gitignore                            # Git ignore (to create)
│
└── development/
    ├── src/
    │   ├── __init__.py
    │   ├── blackduck_init.py             # ⭐ Core logic
    │   ├── bridge_executor.py            # Bridge CLI wrapper
    │   ├── mcp_server.py                 # MCP adapter
    │   ├── cli.py                        # CLI adapter
    │   ├── types.py                      # Type definitions
    │   ├── utils.py                      # Utilities
    │   └── logger.py                     # Logging
    │
    ├── tests/
    │   ├── __init__.py
    │   ├── test_blackduck_init.py
    │   ├── test_bridge_executor.py
    │   ├── test_mcp_server.py
    │   └── test_cli.py
    │
    ├── templates/
    │   └── input.json                    # Template with ${VAR}
    │
    ├── input/                            # Generated inputs
    │   └── input_{UUID}.json
    │
    ├── output/                           # Generated outputs
    │   └── output_{UUID}.json
    │
    ├── logs/                             # Application logs
    │   └── app.log
    │
    ├── requirements.txt
    ├── .env.example
    └── README.md
```

---

## 🔒 Security Requirements

### 5.1 Input Validation

```
✅ project_path
   - Must exist and be directory
   - Must be readable
   - Path normalization (expand ~, resolve ..)

✅ polaris_token
   - Must be non-empty string
   - Min length: 10 characters
   - Never logged as plaintext

✅ server_url
   - Must be valid HTTPS URL
   - Must start with https://
   - Domain validation

✅ api_token
   - Optional, but if provided must be non-empty
   - Never logged as plaintext

✅ include_dev_deps
   - Must be boolean type
   - Default: false
```

### 5.2 Data Protection

```
✅ Token Handling
   - Load from environment variables (.env)
   - Never hardcode tokens
   - Never include in logs
   - Mask in error messages
   - Never save to files

✅ File Operations
   - Input JSON: Secure file permissions (600)
   - Output JSON: Read-only after Bridge CLI completes
   - Temp files: Auto-cleanup
   - No tokens in filenames

✅ Error Messages
   - Don't reveal infrastructure details
   - Don't expose token values
   - Provide helpful remediation steps
```

### 5.3 Network Security

```
✅ HTTPS Only
   - All API calls use HTTPS
   - Verify SSL certificates
   - Handle SSL errors gracefully

✅ Timeouts
   - Bridge CLI execution: 300 seconds (5 minutes)
   - Network requests: 10 seconds
   - Prevent hanging processes

✅ Retry Logic
   - Max 3 retries for transient failures
   - Exponential backoff (1s, 2s, 4s)
   - Only retry on safe operations
```

---

## ✅ Validation & Testing

### 6.1 Input Validation

**Valid Cases**:
- ✅ All required fields provided
- ✅ Project path exists and is readable
- ✅ Server URL is HTTPS
- ✅ Tokens are non-empty strings

**Invalid Cases**:
- ❌ Missing required field
- ❌ Project path doesn't exist
- ❌ Server URL is HTTP (not HTTPS)
- ❌ Empty or invalid tokens

### 6.2 Unit Tests

```python
test_blackduck_init.py:
  ✅ test_valid_inputs()
  ✅ test_invalid_project_path()
  ✅ test_invalid_server_url()
  ✅ test_missing_tokens()
  ✅ test_uuid_generation()
  ✅ test_variable_replacement()

test_bridge_executor.py:
  ✅ test_command_building()
  ✅ test_bridge_execution()
  ✅ test_output_parsing()
  ✅ test_timeout_handling()

test_mcp_server.py:
  ✅ test_tool_registration()
  ✅ test_tool_invocation()
  ✅ test_response_format()

test_cli.py:
  ✅ test_cli_arguments()
  ✅ test_cli_execution()
  ✅ test_exit_codes()
```

### 6.3 Integration Tests

```
✅ End-to-end workflow with mock Bridge CLI
✅ File creation and cleanup
✅ Error handling scenarios
✅ Multi-user concurrent execution
```

---

## 🎯 Success Criteria

### Phase 1 Completion (Week 4)

#### Code Quality
- [ ] All unit tests passing (100% coverage for core logic)
- [ ] No security vulnerabilities (token handling verified)
- [ ] Code follows PEP 8 standards
- [ ] Type hints throughout codebase
- [ ] Clear error messages for all failure paths

#### Functionality
- [ ] `/blackduck-init` command works end-to-end
- [ ] MCP server registers tool correctly
- [ ] CLI tool accepts all parameters
- [ ] input.json created with correct variable replacement
- [ ] output.json parsed and returned correctly
- [ ] UUID is unique for each scan
- [ ] Handles all error scenarios gracefully

#### Documentation
- [ ] README with setup instructions
- [ ] Architecture documentation
- [ ] API documentation
- [ ] Troubleshooting guide
- [ ] Example usage for Claude and CLI

#### Deployment Readiness
- [ ] Code pushed to public GitHub repository
- [ ] All dependencies in requirements.txt
- [ ] .env.example with all required variables
- [ ] .gitignore properly configured
- [ ] License (MIT) included
- [ ] Ready for GitHub marketplace submission

---

## 📈 Performance Requirements

| Aspect | Requirement | Target |
|--------|-------------|--------|
| Command execution | < 30 seconds (excluding Bridge CLI) | 10-15 seconds |
| MCP server startup | < 2 seconds | 1 second |
| Input file generation | < 1 second | < 500ms |
| Memory usage | < 100MB | < 50MB |
| Bridge CLI execution | Depends on project size | Monitored |

---

## 🗓️ Timeline & Milestones

| Week | Milestone | Deliverables |
|------|-----------|-------------|
| Week 1 | Foundation | Folder structure, core logic, utils, logger |
| Week 2 | Adapters | MCP server, CLI tool, bridge executor |
| Week 3 | Testing | Unit tests, integration tests, bug fixes |
| Week 4 | Finalization | Documentation, GitHub push, polishing |

---

## 🔄 Future Enhancements (Phase 2+)

- [ ] REST API server for multi-platform support
- [ ] GitHub Copilot integration
- [ ] ChatGPT plugin
- [ ] Google Gemini integration
- [ ] Docker containerization
- [ ] Advanced caching strategies
- [ ] Webhook integration for CI/CD
- [ ] Dashboard for scan results
- [ ] Scheduled scans
- [ ] Team/organization features

---

## 📚 References

- [Bridge CLI Guide](https://docs.blackduck.com/r/bridge/latest/bridge-cli-guide/)
- [Polaris Documentation](https://docs.blackduck.com/r/polaris)
- [MCP Protocol](https://modelcontextprotocol.io)
- [Python Best Practices (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Security (OWASP Top 10)](https://owasp.org/www-project-top-ten/)

---

## ✍️ Approval & Sign-Off

**Document Status**: ✅ **FINAL - READY FOR DEVELOPMENT**

**Confirmed Details**:
- [x] Bridge CLI command format correct
- [x] Input/output file specifications understood
- [x] UUID generation requirements clear
- [x] Token handling requirements clear
- [x] Phase 1 scope defined (MCP + CLI)
- [x] 4-week timeline acceptable
- [x] Success criteria defined

---

**Next Action**: Proceed with Phase 1 Development Implementation

**Phase 1 Start Date**: August 3, 2024

---

*Document Version: 1.0*  
*Last Updated: August 3, 2024*  
*Status: APPROVED FOR DEVELOPMENT*

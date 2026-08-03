# BlackDuck AI Command - Phase 1 Development

## 📌 Overview

This is the development directory for Phase 1 of the BlackDuck AI Command project. It contains a Python MCP server implementation that provides a `/blackduck-init` command for initializing BlackDuck security scanning.

**Status**: ✅ Phase 1 Complete

---

## 🚀 Quick Start

### 1. Setup

```bash
# Navigate to development directory
cd development/

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template and configure
cp .env.example .env
# Edit .env with your BlackDuck credentials
```

### 2. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_blackduck_init.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### 3. Use CLI

```bash
# Show help
python -m src.cli --help

# Initialize BlackDuck for a project
python -m src.cli init \
  --project /path/to/project \
  --polaris-token your-token \
  --server https://blackduck.company.com \
  --api-token your-api-token

# Output as JSON
python -m src.cli init \
  --project /path/to/project \
  --polaris-token your-token \
  --server https://blackduck.company.com \
  --json
```

### 4. Run MCP Server

```bash
# Start MCP server for Claude Code
python -m src.mcp_server
```

---

## 📂 Directory Structure

```
development/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── types.py                 # Type definitions (Pydantic models)
│   ├── logger.py                # Logging configuration
│   ├── utils.py                 # Utility functions
│   ├── bridge_executor.py       # Bridge CLI execution
│   ├── blackduck_init.py        # ⭐ Core logic
│   ├── cli.py                   # Click CLI adapter
│   └── mcp_server.py            # MCP server adapter
│
├── tests/
│   ├── __init__.py
│   ├── test_blackduck_init.py   # Core logic tests
│   ├── test_bridge_executor.py  # Bridge executor tests
│   ├── test_cli.py              # CLI tests
│   └── test_mcp_server.py       # MCP server tests
│
├── templates/
│   └── input.json               # Input configuration template
│
├── input/                       # Generated input files
│   └── input_{UUID}.json
│
├── output/                      # Generated output files
│   └── output_{UUID}.json
│
├── logs/                        # Application logs
│   └── app.log
│
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

---

## 🔧 Core Modules

### `src/types.py`
Pydantic models for input/output validation:
- `BlackDuckInitInput` - Input parameters for the command
- `BlackDuckInitOutput` - Output response format

### `src/logger.py`
Logging setup with:
- Console output (colored)
- File logging (rotating)
- Configurable log level

### `src/utils.py`
Helper functions:
- `validate_project_path()` - Validate project directory
- `generate_uuid()` - Generate unique scan ID
- `load_json_template()` - Load template file
- `replace_variables()` - Replace variables in JSON
- `save_json_file()` - Save JSON with secure permissions
- `read_json_file()` - Read JSON file

### `src/bridge_executor.py`
Bridge CLI execution:
- `BridgeExecutor` class - Handles Bridge CLI invocation
- `execute_bridge_cli()` - Helper function

### `src/blackduck_init.py` ⭐
Core business logic:
- `BlackDuckInitializer` class - Main initialization logic
- `blackduck_init()` - Entry point function

### `src/cli.py`
CLI interface using Click:
- `init` command - Initialize BlackDuck scanning
- `version` command - Show version

### `src/mcp_server.py`
MCP server for Claude Code:
- `list_tools()` - Register tools
- `call_tool()` - Handle tool invocations

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Test Coverage

```bash
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

### Mock Testing

Tests use `tempfile.TemporaryDirectory()` for safe file operations without affecting the system.

---

## 📝 Environment Variables

Create `.env` file from `.env.example`:

```bash
# Required
POLARIS_TOKEN=your-polaris-token-here
BLACKDUCK_SERVER_URL=https://your-blackduck-server

# Optional
BLACKDUCK_API_TOKEN=your-api-token-here
BRIDGE_CLI_PATH=/usr/local/bin/bridge-cli

# Application
LOG_LEVEL=INFO
DEBUG=false
```

---

## 🔍 How It Works

### Workflow

1. **User Input**: Provides project path, tokens, and server URL
2. **Validation**: Validates all inputs
3. **UUID Generation**: Creates unique scan ID
4. **Template Loading**: Loads input.json template
5. **Variable Replacement**: Replaces ${VAR} with actual values
6. **File Generation**: Saves modified input.json
7. **Bridge CLI Execution**: Runs Bridge CLI with the command:
   ```bash
   bridge-cli {project_path} --stage polaris \
     --input input.json \
     --out {project_path}/output/output_{UUID}.json \
     --diagnostics
   ```
8. **Output Reading**: Reads and parses output.json
9. **Result Return**: Returns success/failure with details

### Platform Adapters

- **CLI**: Direct Python invocation via Click
- **MCP**: Claude Code integration via MCP protocol
- **Future**: REST API, Copilot, ChatGPT, Gemini

---

## 🚨 Error Handling

All errors are handled gracefully:
- Invalid inputs → Clear validation error message
- Missing project path → File not found error
- Bridge CLI not available → Helpful error message
- Timeout → Execution timeout error
- Invalid output → JSON parsing error

Each error includes suggestions for remediation.

---

## 📊 Logging

Logs are written to both console and file:

**Console**:
- Colored output
- Real-time monitoring
- DEBUG or INFO level based on environment

**File** (`logs/app.log`):
- Full timestamp
- Function and line number
- Rotating logs (10MB rotation, 1-week retention)

Configure log level:
```bash
export LOG_LEVEL=DEBUG  # More verbose
export LOG_LEVEL=INFO   # Standard
export LOG_LEVEL=ERROR  # Only errors
```

---

## 🔒 Security

### Token Handling
- ✅ Tokens loaded from environment variables only
- ✅ Never logged to console or files
- ✅ Masked in error messages
- ✅ Input JSON saved with secure permissions (600)

### Input Validation
- ✅ Project path must exist and be readable
- ✅ Server URL must be HTTPS
- ✅ Tokens must meet minimum requirements
- ✅ Pydantic validation on all inputs

---

## 🐛 Troubleshooting

### Bridge CLI Not Found
```
Error: Bridge CLI not found: /usr/local/bin/bridge-cli
```
**Solution**: Install Bridge CLI or set `BRIDGE_CLI_PATH` environment variable

### Template Not Found
```
FileNotFoundError: Template file not found: development/templates/input.json
```
**Solution**: Ensure you're running from the correct directory

### Permission Denied
```
PermissionError: [Errno 13] Permission denied
```
**Solution**: Check directory permissions on project path and output directory

### Invalid JSON in Output
```
json.JSONDecodeError: Invalid JSON in file
```
**Solution**: Verify Bridge CLI completed successfully and output.json is valid

---

## 🔄 Development Workflow

### Adding New Features

1. Create feature branch
2. Add tests in `tests/`
3. Implement in `src/`
4. Run tests: `pytest tests/ -v`
5. Create commit with message describing changes

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for functions
- Keep functions focused and small

### Testing

- Unit tests for all core logic
- Mock external dependencies
- Test error cases
- Aim for 80%+ coverage

---

## 📚 References

- [MCP Protocol](https://modelcontextprotocol.io)
- [Bridge CLI Documentation](https://docs.blackduck.com/r/bridge/latest/bridge-cli-guide/)
- [Click CLI Framework](https://click.palletsprojects.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Loguru Logger](https://loguru.readthedocs.io/)

---

## 📝 Phase 1 Completion Checklist

- [x] Folder structure created
- [x] Core logic implemented (blackduck_init.py)
- [x] Type definitions (types.py)
- [x] Utilities (utils.py, logger.py)
- [x] Bridge executor (bridge_executor.py)
- [x] CLI adapter (cli.py)
- [x] MCP server (mcp_server.py)
- [x] Input template (input.json)
- [x] Unit tests (test_*.py)
- [x] Documentation (README.md)
- [x] Requirements (requirements.txt)
- [x] Environment template (.env.example)

---

## 🎯 Next Steps (Phase 2)

- [ ] REST API server
- [ ] GitHub Copilot integration
- [ ] ChatGPT plugin
- [ ] Docker containerization
- [ ] Deployment to production

---

**Phase 1 Status**: ✅ COMPLETE  
**Ready for Phase 2**: Yes  
**Ready for GitHub**: Yes  

For Phase 2 and beyond, see the main project documentation.

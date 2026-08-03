# BlackDuck AI Command - Requirements Document

## 📋 Project Overview

**Project Name**: BlackDuck AI Command (blackduck-init)

**Vision**: A platform-agnostic AI command that allows engineers to initialize BlackDuck security scanning from Claude, Copilot, ChatGPT, and other AI platforms - making security scanning a natural part of the AI-assisted development workflow.

**Current Phase**: Requirements Understanding ✅

---

## 🎯 Business Goals

1. **Democratize Security**: Make BlackDuck security scanning accessible via AI assistants
2. **Reduce Friction**: One command instead of manual setup
3. **Multi-Platform**: Work seamlessly across Claude, Copilot, ChatGPT, Gemini
4. **Open Source**: Community-driven, publicly available tool

---

## 👥 Target Users

| User Type | Platform | Use Case |
|-----------|----------|----------|
| **Claude Users** | Claude Code | Initialize BlackDuck while coding with Claude |
| **Copilot Users** | GitHub Copilot (VS Code) | Quick security setup in their IDE |
| **ChatGPT Users** | ChatGPT Plugin | Ask ChatGPT to set up security scanning |
| **DevOps Teams** | CLI / CI/CD | Automate in pipelines |
| **Security Teams** | Any platform | Enforce security scanning standards |

---

## 📌 Functional Requirements

### 1. Core Command: `/blackduck-init`

**What it does**: Initialize BlackDuck security scanning for a project, It will download the bridge cli https://artifactory.tools.duckutil.net/artifactory/clops-local/integrations/bridge/binaries/bridge-cli-bundle
and execute it in the shared local repository path with input.json file.
input.json will be present in the input folder, replace variable at the run time and execute brige-cli and share result in the output.json format.
generate UUID which will be unique and same for all the UUID variables present in the input.json file.

**Inputs Required**:
```
- project_path (string)
  Example: /Users/me/myapp or ~/myproject
  Description: Path to the project directory
  Required: YES

- polaris_token
  Description: User specific Polaris token
  Required: YES

- server_url (string)
  Example: https://blackduck.company.com
  Description: BlackDuck Hub server URL
  Required: YES

- api_token (string)
  Example: (secret token)
  Description: BlackDuck API authentication token
  Required: NO
  Security: Must NOT be logged or exposed

- include_dev_deps (boolean)
  Example: true/false
  Description: Include development dependencies in scan
  Required: NO
  Default: false
```

**Output (Success)**:
```json
{
  "success": true,
  "message": "BlackDuck initialization successful",
  "config_path": "/Users/me/myapp/.blackduck.json",
  "scan_id": "scan-uuid-12345",
  "details": {
    "project_name": "myapp",
    "scan_status": "queued",
    "components_found": 142,
    "next_steps": "BlackDuck scan started. Results will be available in 5-15 minutes."
  }
}
```

**Output (Failure)**:
```json
{
  "success": false,
  "message": "Failed to connect to BlackDuck server",
  "error": "Connection refused: https://blackduck.company.com",
  "solution": "Verify server URL and network connectivity"
}
```

---

### 2. Supported Platforms

#### 2.1 Claude Code (Phase 1 - MVP)
- **Technology**: MCP (Model Context Protocol) Server
- **How it works**: 
  - User: `@Claude please initialize BlackDuck for /Users/me/myapp`
  - Claude calls `/blackduck-init` tool from MCP server
  - Returns results to user
- **Installation**: Users run `claude mcp add ...`
- **Status**: PRIMARY PLATFORM

#### 2.2 GitHub Copilot (Phase 2 - Future)
- **Technology**: VS Code Extension + REST API
- **How it works**: Copilot calls REST API backend
- **Status**: PLANNED

#### 2.3 ChatGPT Plugin (Phase 3 - Future)
- **Technology**: ChatGPT Plugin API + REST API
- **How it works**: ChatGPT calls REST API with OpenAPI schema
- **Status**: PLANNED

#### 2.4 Local CLI (Phase 1 - MVP)
- **Technology**: Python CLI tool
- **How it works**: Users run `python -m blackduck_ai_command init ...`
- **Use case**: Testing, automation, direct use
- **Status**: PRIMARY (for development/testing)

---

## ⚙️ Non-Functional Requirements

### 3.1 Performance
- Command execution: < 30 seconds (including API calls)
- MCP server startup: < 2 seconds
- Memory usage: < 100MB

### 3.2 Security
- ✅ API tokens NEVER logged or stored in plaintext
- ✅ Use environment variables for secrets
- ✅ Validate all inputs before processing
- ✅ HTTPS-only for all network calls
- ✅ No sensitive data in response messages
- ✅ Rate limiting (future): 100 requests/hour per IP

### 3.3 Reliability
- ✅ Graceful error handling for network failures
- ✅ Clear error messages for troubleshooting
- ✅ Retry logic for transient failures (max 3 retries)
- ✅ Connection timeout: 10 seconds

### 3.4 Compatibility
- ✅ Python 3.10+ (minimum)
- ✅ Works on macOS, Linux, Windows
- ✅ No external binaries required (pure Python)
- ✅ Works with BlackDuck API v6+

### 3.5 Maintainability
- ✅ Clean, well-documented code
- ✅ Unit tests for core logic
- ✅ Type hints throughout
- ✅ Modular design (core logic separate from adapters)

---

## 📊 Scope Definition

### What's INCLUDED (Phase 1 - MVP):
```
✅ Core business logic (blackduck_init.py)
✅ MCP Server implementation
✅ Python CLI tool
✅ Input validation (JSON Schema)
✅ Error handling & logging
✅ Unit tests
✅ Documentation
✅ GitHub repository
✅ README with setup guide
```

### What's EXCLUDED (Future Phases):
```
❌ ChatGPT Plugin (Phase 2)
❌ GitHub Copilot integration (Phase 2)
❌ Google Gemini integration (Phase 3)
❌ REST API server (Phase 2)
❌ Docker deployment (Phase 2)
❌ Web UI/Dashboard (Future)
❌ Advanced scanning options (Future)
```

---

## 🏗️ Architecture Requirements

### 3.1 Core Architecture

```
Core Logic (blackduck_init.py)
├── Validate inputs
├── Load configuration from .env
├── Connect to BlackDuck API
├── Initialize project
└── Return standardized response

Adapters:
├── MCP Server (mcp_server.py) → Claude Code
├── CLI Tool (cli.py) → Terminal/Automation
└── REST API (rest_server.py) → [Future] Other platforms
```

### 3.2 File Structure (Phase 1)

```
development/
├── src/
│   ├── __init__.py
│   ├── blackduck_init.py      # Core logic (no platform deps)
│   ├── mcp_server.py          # MCP adapter for Claude
│   ├── cli.py                 # CLI adapter
│   ├── types.py               # Type definitions
│   ├── utils.py               # Helper functions
│   └── logger.py              # Logging setup
├── tests/
│   ├── test_blackduck_init.py
│   ├── test_mcp_server.py
│   └── test_cli.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📝 User Stories

### Story 1: Claude User
**As a** software engineer using Claude Code  
**I want to** initialize BlackDuck scanning with a simple command  
**So that** I can secure my project without leaving Claude

**Acceptance Criteria**:
- [ ] Type `@Claude please init BlackDuck for /path/to/project`
- [ ] Claude calls the `/blackduck-init` tool
- [ ] Tool returns configuration details
- [ ] User sees: "BlackDuck initialized successfully" + next steps

---

### Story 2: DevOps Engineer
**As a** DevOps engineer managing CI/CD pipelines  
**I want to** use the CLI tool to initialize BlackDuck in scripts  
**So that** I can automate security scanning setup

**Acceptance Criteria**:
- [ ] Can run: `python -m blackduck_ai_command init --project /path --server URL --token TOKEN`
- [ ] Tool creates `.blackduck.json` config file
- [ ] Script can check exit code (0 = success, 1 = failure)
- [ ] Suitable for Docker/automation

---

### Story 3: Security Team
**As a** security team lead  
**I want to** provide a one-click tool for developers  
**So that** they consistently use BlackDuck scanning

**Acceptance Criteria**:
- [ ] Tool is open source and trustworthy
- [ ] Easy to install via public GitHub
- [ ] Works on developer machines
- [ ] Clear documentation for setup

---

## 🔒 Security Requirements

### Input Validation
```
✅ project_path: Must exist and be readable
✅ server_url: Must be valid HTTPS URL
✅ api_token: Must be non-empty string
✅ include_dev_deps: Must be boolean
```

### Data Protection
```
✅ API tokens NOT logged anywhere
✅ API tokens NOT stored in temporary files
✅ Error messages don't reveal infrastructure details
✅ Use `.env` files for local secrets (never in code)
```

### API Security
```
✅ HTTPS only for BlackDuck API calls
✅ Bearer token authentication
✅ Request timeout: 10 seconds
✅ Retry logic with exponential backoff
```

---

## 📋 Testing Requirements

### Unit Tests
- [ ] Test input validation (valid/invalid inputs)
- [ ] Test error handling (network failure, auth failure, etc.)
- [ ] Test response formatting
- [ ] Test configuration file creation

### Integration Tests
- [ ] Test with mock BlackDuck API
- [ ] Test MCP server communication
- [ ] Test CLI argument parsing

### Manual Testing
- [ ] Test with real BlackDuck server (if available)
- [ ] Test error scenarios
- [ ] Test on macOS, Linux (if possible)

---

## 📈 Success Metrics

### Phase 1 (MVP) Success:
- [ ] Core logic implemented and tested
- [ ] MCP server runs without errors
- [ ] CLI tool functional
- [ ] Documentation complete
- [ ] Code pushed to GitHub
- [ ] All tests passing

### Phase 2 (Post-MVP) Goals:
- [ ] 50+ downloads in first month
- [ ] 10+ GitHub stars
- [ ] Positive community feedback
- [ ] REST API deployed for multi-platform use

---

## 🗓️ Timeline (Phase 1 - MVP)

| Week | Deliverable | Status |
|------|-------------|--------|
| Week 1 | Core logic + Tests + Documentation | Planned |
| Week 2 | MCP Server + CLI tool | Planned |
| Week 3 | Polish + Final testing | Planned |
| Week 4 | Push to GitHub + README | Planned |

---

## ❓ Questions for Clarification

Before we start building, please confirm/clarify:

1. **BlackDuck Integration**
   - [ ] You have a BlackDuck account to test with? YES
   - [ ] You know your BlackDuck server URL? YES
   - [ ] API token generation is understood? YES

2. **Scope**
   - [ ] Phase 1 = Claude MCP + CLI only (correct)? YES
   - [ ] Future platforms can be added later (correct)? YES

3. **Target Users**
   - [ ] Who are the primary users? (e.g., your team, open source community)? BOTH
   - [ ] Should documentation focus on enterprise or individuals? BOTH

4. **Timeline**
   - [ ] Is 4-week MVP timeline realistic? YES
   - [ ] Any hard deadline? NO

5. **Features**
   - [ ] Any specific BlackDuck features you must have? NO
   - [ ] Any features to exclude? NO

---

## 📚 References & Standards

- MCP Protocol: https://modelcontextprotocol.io
- BlackDuck API: https://docs.blackduck.com/r/bridge/latest/bridge-cli-guide/using-bridge-cli-with-polaris.html
- Python Best Practices: PEP 8, Type Hints (PEP 484)
- Security: OWASP Top 10

---

## ✅ Sign-Off

**Requirements Status**: 🟡 PENDING REVIEW

Please review the above requirements and confirm:

- [ ] All functional requirements are clear?
- [ ] Non-functional requirements acceptable?
- [ ] Scope is correct?
- [ ] Questions answered?

Once confirmed, we'll proceed to **Phase 1 Development**.

---

**Next Step**: Review requirements → Confirm → Start Development Phase

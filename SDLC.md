# BlackDuck AI Command - SDLC Workflow

This project follows a structured **Software Development Life Cycle (SDLC)** with the following phases:

## 📊 Workflow Phases

For a visual diagram, see **[WORKFLOW.html](WORKFLOW.html)** - Open in browser to view the complete workflow.

---

## 🏗️ Phase 1: Development (📁 `/development` folder)

**Status**: Currently here ✅

### What Happens:
- Create core logic locally
- Test functionality
- Write documentation
- Set up MCP server
- Create CLI tool

### Deliverables:
```
/development/
├── src/
│   ├── blackduck_init.py          # Core business logic
│   ├── mcp_server.py              # MCP server implementation
│   └── utils.py                   # Helper functions
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── README.md                       # Documentation
└── tests/                         # Unit tests
```

### Success Criteria:
- ✅ Core logic implemented and tested
- ✅ MCP server running locally
- ✅ CLI tool working
- ✅ Documentation complete
- ✅ All tests passing

### Next Step:
→ Proceed to **Phase 2: Publish** once development is complete

---

## 📤 Phase 2: Publish (GitHub)

**Status**: Pending

### What Happens:
- Create public GitHub repository
- Push all code to main branch
- Set repository settings (public, descriptions)
- Add GitHub-specific files

### Deliverables:
- GitHub repo: `https://github.com/your-username/blackduck-ai-command`
- Public repository with README, LICENSE
- Git history tracking all commits

### Commands:
```bash
# Initialize git (if not already done)
cd /Users/pankajk/project/GitHub/BlackDuckAgenticAi
git init
git add .
git commit -m "Initial commit: BlackDuck AI Command - Python MCP Server"

# Add remote
git remote add origin https://github.com/your-username/blackduck-ai-command.git
git branch -M main
git push -u origin main
```

### Success Criteria:
- ✅ Code pushed to GitHub
- ✅ Repository is public
- ✅ README visible on GitHub
- ✅ All files properly committed

### Next Step:
→ Proceed to **Phase 3: Marketplace (Optional)** or skip to **Phase 4**

---

## ⭐ Phase 3: Marketplace (Optional)

**Status**: Pending (Optional)

### What Happens:
- Submit plugin to Claude community marketplace
- Anthropic reviews and approves
- Plugin becomes discoverable in Claude Code UI
- Auto-updates when you push commits

### Process:
1. Go to [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)
2. Fill in plugin details
3. Link GitHub repository
4. Wait for Anthropic review
5. Once approved, users can search and install from Claude Code

### Success Criteria:
- ✅ Plugin submitted
- ✅ Anthropic approves
- ✅ Listed in marketplace
- ✅ Searchable by users

### Timeline:
- Submission → Approval: 1-2 weeks typically

### Next Step:
→ If approved, proceed to **Phase 4: Installation**
→ Users can install immediately from GitHub even without marketplace approval

---

## 📥 Phase 4: Installation

**Status**: Pending

### What Happens:
Users can install your MCP server via:

#### Option A: Direct from GitHub (Immediate)
```bash
# Users run this to install
claude mcp add --stdio python -m blackduck_ai_command.mcp_server
```

Or via Claude Code CLI:
```bash
claude mcp add https://github.com/your-username/blackduck-ai-command
```

#### Option B: From Marketplace (After Phase 3 Approval)
- Users search for "blackduck" in Claude Code
- Click Install
- MCP server auto-configured

### Success Criteria:
- ✅ Users can install via CLI
- ✅ Installation completes successfully
- ✅ MCP server connects properly

---

## 🚀 Phase 5: Usage

**Status**: Pending

### What Happens:
Users run `/blackduck-init` command in Claude Code:

```
@Claude please initialize BlackDuck for my project at /Users/me/myapp
```

Claude Code:
1. Lists available tools from MCP server
2. Finds `blackduck-init` tool
3. Calls the tool with user's parameters
4. Returns results to user

### User Flow:
```
User Request
    ↓
Claude Code (MCP Client)
    ↓
MCP Server (your code)
    ↓
Core Logic (blackduck_init.py)
    ↓
BlackDuck API
    ↓
Results → User
```

### Success Criteria:
- ✅ Command available in Claude Code
- ✅ Parameters accepted correctly
- ✅ BlackDuck integration works
- ✅ Results displayed properly

---

## 📋 Project Folder Structure

```
BlackDuckAgenticAi/
├── WORKFLOW.html                  # Visual workflow diagram
├── SDLC.md                        # This file
├── README.md                      # Main documentation
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
├── .git/                          # Git repository (after init)
│
├── development/                   # Phase 1: Development
│   ├── src/
│   │   ├── __init__.py
│   │   ├── blackduck_init.py     # Core logic
│   │   ├── mcp_server.py         # MCP server
│   │   └── utils.py              # Utilities
│   │
│   ├── tests/
│   │   ├── test_blackduck_init.py
│   │   └── test_mcp_server.py
│   │
│   ├── requirements.txt           # Dependencies
│   ├── .env.example               # Environment template
│   └── README.md                  # Phase 1 documentation
│
├── publish/                       # Phase 2: Publish
│   └── README.md                  # How to publish to GitHub
│
├── marketplace/                   # Phase 3: Marketplace
│   └── submission-checklist.md    # Marketplace submission guide
│
├── install/                       # Phase 4: Installation
│   └── user-guide.md              # How users install
│
└── usage/                         # Phase 5: Usage
    └── examples.md                # Usage examples
```

---

## 🎯 Quick Start (From Current State)

### Current Phase: Development ✅

1. **Create project structure** (next step)
   ```bash
   mkdir -p development/src
   mkdir -p development/tests
   ```

2. **Create Python files** 
   - `blackduck_init.py` - Core logic
   - `mcp_server.py` - MCP server
   - `utils.py` - Helpers

3. **Create requirements.txt**
   ```
   mcp>=0.5.0
   pydantic>=2.0
   python-dotenv>=1.0.0
   requests>=2.31.0
   loguru>=0.7.0
   ```

4. **Test locally**
   ```bash
   pip install -r development/requirements.txt
   python development/src/mcp_server.py
   ```

5. **Write tests and documentation**

6. **Commit to git**
   ```bash
   git add .
   git commit -m "Phase 1 Complete: Development done"
   ```

### Then Proceed:
→ **Phase 2**: Push to GitHub
→ **Phase 3**: Submit to Marketplace (optional)
→ **Phase 4**: Users install
→ **Phase 5**: Users run `/blackduck-init`

---

## 📝 Progress Tracking

- [ ] **Phase 1: Development** - Create and test locally
  - [ ] Core logic (`blackduck_init.py`)
  - [ ] MCP server (`mcp_server.py`)
  - [ ] Tests written
  - [ ] Documentation complete
  
- [ ] **Phase 2: Publish** - Push to GitHub
  - [ ] GitHub repo created
  - [ ] Code pushed
  - [ ] README visible
  - [ ] License added
  
- [ ] **Phase 3: Marketplace** - Submit for approval (optional)
  - [ ] Plugin submitted
  - [ ] Anthropic review
  - [ ] Approval granted
  
- [ ] **Phase 4: Installation** - Users can install
  - [ ] GitHub URL shareable
  - [ ] CLI install works
  - [ ] MCP connects properly
  
- [ ] **Phase 5: Usage** - Users run the command
  - [ ] Command available in Claude Code
  - [ ] Parameters work correctly
  - [ ] Results displayed

---

## 🔗 References

- **Workflow Visualization**: `WORKFLOW.html`
- **Phase 1 Docs**: `development/README.md`
- **Phase 2 Docs**: `publish/README.md`
- **Phase 3 Docs**: `marketplace/submission-checklist.md`
- **Phase 4 Docs**: `install/user-guide.md`
- **Phase 5 Docs**: `usage/examples.md`

---

**Next Action**: Start Phase 1 Development - Create Python MCP Server structure

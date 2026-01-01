# Adaptive Task Planner Agent - Setup Guide

**Developer: Rana Karmakar (Gen AI Engineer)**

## Quick Start

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
# Install core LangGraph and LangChain dependencies
pip install langgraph>=1.0.5 langchain>=0.3.26 langchain-core>=0.3.26 typing-extensions

# Install Streamlit (without pandas dependencies to avoid build issues)
pip install streamlit --no-deps
pip install altair blinker cachetools click importlib-metadata numpy pillow protobuf pytz requests rich tenacity toml tornado tzlocal validators
```

### 3. Run the Demo

#### Option 1: Streamlit Web UI (Recommended)
```bash
python run_demo.py
```
This will open the interactive web interface at http://localhost:8501

#### Option 2: Command Line Demo
```bash
python main.py
```

## What's Updated

### Latest Versions
- **LangGraph 1.0.5** - Stable production release with improved APIs
- **LangChain 0.3.26** - Latest stable version with enhanced features
- **Streamlit 1.52.2** - Modern web UI framework

### Key Improvements
1. **Updated LangGraph imports** - Uses `START` constant instead of `set_entry_point()`
2. **Simplified dependencies** - Removed pandas/pyarrow to avoid build issues
3. **Custom table display** - Built table rendering without pandas dependency
4. **Enhanced error handling** - Better error messages and dependency checking

## Features

### Interactive Web Interface
- Add/remove tasks dynamically
- Real-time agent execution
- Visual progress tracking
- Detailed analysis and metrics

### Agent Capabilities
- **Intelligent Planning** - Sorts tasks by deadline, respects 8-hour daily limits
- **Simulated Execution** - Completes tasks one by one
- **Progress Reflection** - Analyzes what's done vs. what remains
- **Dynamic Replanning** - Moves unfinished tasks back for future cycles

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure virtual environment is activated
   source venv/bin/activate
   
   # Verify installations
   python -c "import langgraph, langchain, streamlit; print('All imports successful')"
   ```

2. **PyArrow Build Errors**
   - This setup avoids PyArrow by using custom table rendering
   - If you need pandas, install cmake first: `brew install cmake` (macOS) or `apt-get install cmake` (Linux)

3. **Streamlit Dependency Conflicts**
   - The setup uses `--no-deps` to avoid automatic pandas installation
   - All required Streamlit dependencies are installed manually

### Verification
```bash
# Test the agent core functionality
python -c "
from agent import create_initial_state, run_agent_workflow
import datetime
tasks = [{'name': 'Test', 'deadline': datetime.datetime.now().isoformat(), 'estimated_hours': 1.0}]
state = create_initial_state(tasks)
final_state = run_agent_workflow(state)
print(f'Success: {len(final_state[\"completed_tasks\"])}/{len(final_state[\"tasks\"])} tasks completed')
"
```

## Project Structure

```
adaptive-task-planner-agent/
├── agent/
│   ├── __init__.py          # Package initialization
│   ├── state.py             # AgentState definition and utilities
│   ├── nodes.py             # Workflow node implementations
│   └── graph.py             # LangGraph workflow creation
├── main.py                  # CLI demo runner
├── streamlit_app.py         # Streamlit web UI demo
├── run_demo.py              # Demo launcher script
├── requirements.txt         # Full dependencies (with pandas)
├── requirements-minimal.txt # Core dependencies only
├── SETUP_GUIDE.md          # This file
└── README.md               # Project documentation
```

## Success!

If everything is working correctly, you should see:
- CLI demo runs without errors
- Streamlit app launches at http://localhost:8501
- Agent completes task planning, execution, and reflection cycles
- Web interface allows interactive task management

**Built with LangGraph 1.0 and LangChain 0.3 by Rana Karmakar (Gen AI Engineer)**
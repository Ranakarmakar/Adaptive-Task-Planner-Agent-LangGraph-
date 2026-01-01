# Adaptive Task Planner Agent

A simple, clean AI agent built with **LangGraph 1.0** that demonstrates intelligent task planning, execution simulation, reflection, and dynamic replanning capabilities.

## 🎯 Overview

This project showcases a production-ready AI agent architecture that:
- **Plans tasks** intelligently based on deadlines and time constraints
- **Simulates execution** by completing tasks one at a time
- **Reflects on progress** to identify unfinished work
- **Replans dynamically** when tasks remain incomplete

The agent follows a continuous improvement loop, adapting its approach based on execution results.

## 🏗️ Why LangGraph 1.0?

LangGraph 1.0 was chosen for this project because it provides:

- **Stable Core APIs**: Production-ready with unchanged graph primitives and execution model
- **Stateful Workflows**: Maintains context across multiple planning cycles with built-in checkpointing
- **Graph-Based Orchestration**: Natural modeling of decision points and transitions
- **Durable Execution**: Built-in persistence, streaming, and human-in-the-loop patterns
- **Seamless Integration**: Works hand-in-hand with LangChain 1.0 for high-level to low-level control

## 🔧 Agent Architecture

The agent consists of four main components working in a cycle:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ plan_tasks  │───▶│ execute_day │───▶│   reflect   │
│             │    │             │    │             │
└─────────────┘    └─────────────┘    └──────┬──────┘
       ▲                                     │
       │           ┌─────────────┐           ▼
       └───────────│   replan    │◀──────[feedback?]
                   │             │
                   └─────────────┘           │
                                            ▼
                                         [ END ]
```

### Components

1. **plan_tasks**: Creates daily schedule based on deadlines (up to 8 hours)
2. **execute_day**: Simulates completing the first task in the plan
3. **reflect**: Analyzes progress and identifies unfinished work
4. **replan**: Moves incomplete tasks back for future planning

## 📊 Graph Flow

The LangGraph workflow follows this decision tree:

```
START
  │
  ▼
plan_tasks ──────────────────────────────────┐
  │                                          │
  ▼                                          │
execute_day                                  │
  │                                          │
  ▼                                          │
reflect                                      │
  │                                          │
  ├─[no feedback]──────────────▶ END         │
  │                                          │
  └─[has feedback]──────────────┐            │
                                │            │
                                ▼            │
                              replan         │
                                │            │
                                └────────────┘
```

**Decision Logic:**
- `reflect → END`: When all planned tasks are complete
- `reflect → replan`: When tasks remain unfinished
- `replan → execute_day`: Continue the cycle with replanned tasks

## 🚀 Example Run

```bash
$ python main.py

🎭 ADAPTIVE TASK PLANNER AGENT DEMO
============================================================
This demo shows an AI agent that plans tasks, executes them,
reflects on progress, and replans when needed using LangGraph.
============================================================

📋 Sample Tasks (6 total):
  1. Review project requirements
     Due: 2024-01-15T09:00:00 (2.0h)
  2. Design system architecture
     Due: 2024-01-15T17:00:00 (4.0h)
  ...

🚀 Starting Adaptive Task Planner Agent
🏗️ Building LangGraph workflow...
✅ LangGraph workflow created successfully

🎬 Executing workflow...

🎯 Planning tasks for the day...
  → Planned 3 tasks (7.5 hours total)
    • Review project requirements
    • Design system architecture
    • Set up development environment

⚡ Executing daily plan...
  → Completing: Review project requirements
  → ✅ Task completed!

🤔 Reflecting on progress...
  → 2 tasks remain unfinished
  → These tasks need replanning:
    • Design system architecture
    • Set up development environment

🔄 Replanning based on feedback...
  → Moving 2 unfinished tasks back to planning
    • Design system architecture → back to planning
    • Set up development environment → back to planning

[Cycle continues until all tasks are complete...]

🏁 Workflow completed successfully!

==================================================
AGENT STATE SUMMARY
==================================================
Total Tasks: 6
Daily Plan: 0 tasks
Completed: 6 tasks

Completed Tasks:
  ✓ Review project requirements
  ✓ Design system architecture
  ✓ Set up development environment
  ✓ Implement core features
  ✓ Write unit tests
  ✓ Create documentation
==================================================

📊 FINAL ANALYSIS:
  Completion Rate: 100% (6/6)
  Status: All planned tasks completed successfully!

✨ The agent demonstrated:
  • Intelligent task planning based on deadlines
  • Simulated task execution
  • Reflection on progress and unfinished work
  • Dynamic replanning when tasks remain incomplete
```

## 🛠️ How to Run

### Prerequisites

```bash
# Install Python 3.8+ and pip
python --version  # Should be 3.8 or higher
```

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd adaptive-task-planner-agent

# Install dependencies
pip install -r requirements.txt
```

### Running the Demo

#### Option 1: Streamlit Web UI (Recommended)

```bash
# Run the interactive web demo
python run_demo.py

# Or directly with streamlit
streamlit run streamlit_app.py
```

The Streamlit demo provides:
- Interactive task management (add/remove tasks)
- Real-time agent execution
- Visual progress tracking
- Detailed analysis and metrics
- User-friendly web interface

#### Option 2: Command Line Demo

```bash
# Run the original CLI demo
python main.py
```

### Project Structure

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
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔮 Future Improvements

This project provides a solid foundation that can be extended with:

### Enhanced Planning
- **Resource Constraints**: Consider team capacity and availability
- **Task Dependencies**: Handle prerequisite relationships between tasks
- **Priority Weighting**: More sophisticated priority algorithms
- **Time Zone Support**: Multi-timezone scheduling capabilities

### Advanced Execution
- **Real Task Integration**: Connect to actual project management tools
- **Progress Tracking**: Detailed completion percentage monitoring
- **Parallel Execution**: Handle multiple concurrent tasks
- **External APIs**: Integration with calendars, Slack, etc.

### Intelligent Learning
- **Historical Analysis**: Learn from past planning accuracy
- **Pattern Recognition**: Identify recurring bottlenecks
- **Predictive Modeling**: Estimate task completion times
- **User Preferences**: Adapt to individual working styles

### Production Features
- **Web Interface**: React/Vue.js dashboard for task management
- **Database Storage**: Persistent task and history storage
- **User Authentication**: Multi-user support with permissions
- **API Endpoints**: RESTful API for external integrations
- **Monitoring**: Logging, metrics, and alerting capabilities

## 🏆 Technical Achievements

This project demonstrates several advanced concepts:

- **State Management**: Clean TypedDict-based state with immutable updates
- **Graph Orchestration**: Conditional workflow routing with LangGraph
- **Separation of Concerns**: Clear boundaries between planning, execution, and reflection
- **Error Handling**: Graceful failure handling and recovery
- **Extensible Design**: Easy to add new nodes and workflow paths
- **Production Patterns**: Code structure suitable for real-world deployment

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

---

**Built with ❤️ using LangGraph 1.0 and LangChain 0.3**
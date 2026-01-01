# Design Document: Streamlit Demo UI

## Overview

The Streamlit Demo UI provides an interactive web interface for the Adaptive Task Planner Agent. It features a clean, intuitive design that allows users to add tasks, visualize the agent's workflow, and observe the planning/execution process in real-time. The UI is built using Streamlit's component system and integrates seamlessly with the existing LangGraph agent.

## Architecture

The UI follows a simple single-page application architecture:

```
┌─────────────────────────────────────────┐
│           Streamlit Frontend            │
├─────────────────────────────────────────┤
│  Task Input │ Agent Controls │ Display  │
├─────────────────────────────────────────┤
│           Session State                 │
├─────────────────────────────────────────┤
│        Existing Agent Module           │
│   (graph.py, nodes.py, state.py)       │
└─────────────────────────────────────────┘
```

The design leverages Streamlit's session state for maintaining application state between user interactions and directly imports the existing agent functionality.

## Components and Interfaces

### Main Application (streamlit_app.py)
- **Purpose**: Entry point and main UI orchestration
- **Key Functions**:
  - `main()`: Application entry point with page layout
  - `initialize_session_state()`: Set up default session variables
  - `render_sidebar()`: Task input and control panel
  - `render_main_content()`: Agent visualization and results

### Task Input Component
- **Location**: Sidebar panel
- **Elements**:
  - Text input for task name
  - Date/time picker for deadline
  - Number input for estimated hours
  - "Add Task" button
  - "Load Sample Tasks" button

### Agent Visualization Component
- **Location**: Main content area
- **Elements**:
  - Current task list table
  - Agent state display (daily plan, completed tasks)
  - Workflow execution log
  - Progress metrics and charts

### Control Panel Component
- **Location**: Sidebar panel
- **Elements**:
  - "Run Agent" button
  - "Reset All" button
  - Agent status indicator

## Data Models

### Session State Schema
```python
{
    "tasks": List[Dict[str, Any]],           # Current task list
    "agent_state": AgentState,               # Current agent state
    "execution_log": List[str],              # Workflow step log
    "is_running": bool,                      # Agent execution status
    "last_updated": datetime                 # Last state update time
}
```

### Task Input Validation
- **Name**: Required, non-empty string, max 100 characters
- **Deadline**: Valid datetime, must be in the future
- **Estimated Hours**: Positive float, range 0.1 to 24.0

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Input Validation Consistency
*For any* task input data, the validation function should consistently accept valid inputs and reject invalid inputs according to the defined rules
**Validates: Requirements 1.2**

### Property 2: Task Addition Behavior
*For any* valid task submission, the task should be added to the task list and the form should be cleared
**Validates: Requirements 1.3**

### Property 3: Error Handling Preservation
*For any* invalid task data submission, an error message should be displayed and the form state should remain unchanged
**Validates: Requirements 1.4**

### Property 4: Agent State Display Synchronization
*For any* agent state change during workflow execution, the UI display should accurately reflect the current state
**Validates: Requirements 2.1**

### Property 5: Daily Plan Visualization
*For any* daily plan created by the agent, all planned tasks should be displayed in an organized, readable format
**Validates: Requirements 2.2**

### Property 6: Task Completion Updates
*For any* task execution event, the UI should immediately update to show the task as completed
**Validates: Requirements 2.3**

### Property 7: Feedback Display Accuracy
*For any* agent reflection and replanning event, the feedback and replanning information should be clearly displayed
**Validates: Requirements 2.4**

### Property 8: Task List Formatting
*For any* collection of tasks, they should be displayed in a structured table format with all required columns
**Validates: Requirements 3.1**

### Property 9: Task State Visual Distinction
*For any* task list containing both completed and pending tasks, completed tasks should be visually distinguishable from pending ones
**Validates: Requirements 3.2**

### Property 10: Task Deletion Functionality
*For any* task in the task list, there should be a mechanism to remove it from the list
**Validates: Requirements 3.3**

### Property 11: Statistics Calculation Accuracy
*For any* task list state, the displayed statistics (total, completed, remaining) should accurately reflect the actual counts
**Validates: Requirements 3.4**

### Property 12: Agent Workflow Execution
*For any* task configuration, clicking "Run Agent" should execute the workflow and display the results
**Validates: Requirements 4.2**

### Property 13: Reset Functionality Completeness
*For any* application state, clicking "Reset" should clear all tasks and return the agent to its initial state
**Validates: Requirements 4.3**

## Error Handling

The UI implements comprehensive error handling:

- **Input Validation Errors**: Display inline error messages for invalid task inputs
- **Agent Execution Errors**: Show error notifications if the agent workflow fails
- **State Synchronization Errors**: Graceful fallback to previous known good state
- **Network/Performance Issues**: Loading indicators and timeout handling

## Testing Strategy

### Dual Testing Approach
The testing strategy combines unit tests for specific functionality with property-based tests for comprehensive coverage:

**Unit Tests**:
- Test specific UI component rendering
- Test sample data loading functionality
- Test button click handlers
- Test error message display

**Property-Based Tests**:
- Test input validation across all possible input combinations
- Test UI state synchronization with random agent states
- Test task list operations with various task configurations
- Test statistics calculations with random task distributions

**Property-Based Testing Configuration**:
- Use Hypothesis for Python property-based testing
- Minimum 100 iterations per property test
- Each test tagged with: **Feature: streamlit-demo-ui, Property {number}: {property_text}**
- Tests focus on UI behavior consistency across all input variations

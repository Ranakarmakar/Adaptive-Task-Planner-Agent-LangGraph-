"""
Agent State Definition

This module defines the state structure that flows through the LangGraph workflow.
The state contains all information needed for task planning, execution, and replanning.
"""

from typing_extensions import TypedDict
from typing import List, Dict, Any


class AgentState(TypedDict):
    """
    State schema for the Adaptive Task Planner Agent.
    
    This TypedDict defines the structure of data that flows between
    LangGraph nodes during the agent's workflow execution.
    """
    
    # Core task management
    tasks: List[Dict[str, Any]]
    """List of all tasks with their metadata (name, deadline, estimated_hours)"""
    
    daily_plan: List[str]
    """List of task names planned for execution today"""
    
    completed_tasks: List[str]
    """List of task names that have been successfully completed"""
    
    feedback: str
    """Explanation of what went wrong or needs adjustment"""


def create_initial_state(tasks: List[Dict[str, Any]]) -> AgentState:
    """
    Create an initial AgentState with the provided tasks.
    
    Args:
        tasks: List of task dictionaries with name, deadline, and estimated_hours
        
    Returns:
        Initialized AgentState ready for workflow execution
    """
    return AgentState(
        tasks=tasks,
        daily_plan=[],
        completed_tasks=[],
        feedback=""
    )


def print_state_summary(state: AgentState) -> None:
    """
    Print a human-readable summary of the current agent state.
    
    Args:
        state: Current agent state to summarize
    """
    print("\n" + "="*50)
    print("AGENT STATE SUMMARY")
    print("="*50)
    
    print(f"Total Tasks: {len(state['tasks'])}")
    print(f"Daily Plan: {len(state['daily_plan'])} tasks")
    print(f"Completed: {len(state['completed_tasks'])} tasks")
    
    if state['daily_plan']:
        print(f"\nToday's Plan:")
        for i, task_name in enumerate(state['daily_plan'], 1):
            print(f"  {i}. {task_name}")
    
    if state['completed_tasks']:
        print(f"\nCompleted Tasks:")
        for task_name in state['completed_tasks']:
            print(f"  ✓ {task_name}")
    
    if state['feedback']:
        print(f"\nFeedback: {state['feedback']}")
    
    print("="*50)
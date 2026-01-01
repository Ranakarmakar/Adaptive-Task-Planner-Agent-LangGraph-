"""
Agent Nodes

This module implements the core workflow nodes for the Adaptive Task Planner Agent.
Each node represents a phase in the agent's decision-making process.
"""

from datetime import datetime
from typing import Dict, Any
from .state import AgentState


def plan_tasks(state: AgentState) -> AgentState:
    """
    Create a simple daily plan based on task deadlines.
    
    This node analyzes available tasks and creates a daily plan by sorting
    tasks by deadline (earliest first) and selecting up to 8 hours of work.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with new daily plan
    """
    print("\n🎯 Planning tasks for the day...")
    
    # Get tasks that haven't been completed yet
    incomplete_tasks = [
        task for task in state["tasks"]
        if task["name"] not in state["completed_tasks"]
    ]
    
    if not incomplete_tasks:
        print("  → All tasks completed!")
        return {**state, "daily_plan": [], "feedback": ""}
    
    # Sort by deadline (earliest first)
    sorted_tasks = sorted(
        incomplete_tasks,
        key=lambda task: datetime.fromisoformat(task["deadline"])
    )
    
    # Simple planning: select tasks up to 8 hours total
    daily_plan = []
    total_hours = 0.0
    max_daily_hours = 8.0
    
    for task in sorted_tasks:
        if total_hours + task["estimated_hours"] <= max_daily_hours:
            daily_plan.append(task["name"])
            total_hours += task["estimated_hours"]
        else:
            # If we can't fit more tasks, stop planning
            break
    
    print(f"  → Planned {len(daily_plan)} tasks ({total_hours:.1f} hours total)")
    for task_name in daily_plan:
        print(f"    • {task_name}")
    
    return {**state, "daily_plan": daily_plan, "feedback": ""}


def execute_day(state: AgentState) -> AgentState:
    """
    Simulate task execution by completing the first task in the daily plan.
    
    This node simulates a work day by completing one task from the daily plan.
    In a real implementation, this would involve actual task execution.
    
    Args:
        state: Current agent state with daily plan
        
    Returns:
        Updated state with completed task
    """
    print("\n⚡ Executing daily plan...")
    
    if not state["daily_plan"]:
        print("  → No tasks to execute")
        return {**state, "feedback": ""}
    
    # Complete the first task in the daily plan
    current_task = state["daily_plan"][0]
    print(f"  → Completing: {current_task}")
    
    # Update state: move task from daily_plan to completed_tasks
    updated_daily_plan = state["daily_plan"][1:]  # Remove first task
    updated_completed = state["completed_tasks"] + [current_task]
    
    print(f"  → ✅ Task completed!")
    
    return {
        **state,
        "daily_plan": updated_daily_plan,
        "completed_tasks": updated_completed,
        "feedback": ""
    }


def reflect(state: AgentState) -> AgentState:
    """
    Analyze the current state and provide feedback on unfinished work.
    
    This node checks if there are unfinished tasks in the daily plan
    and generates feedback explaining what needs attention.
    
    Args:
        state: Current agent state after execution
        
    Returns:
        Updated state with reflection feedback
    """
    print("\n🤔 Reflecting on progress...")
    
    unfinished_count = len(state["daily_plan"])
    total_tasks = len(state["tasks"])
    completed_count = len(state["completed_tasks"])
    
    if unfinished_count == 0:
        if completed_count == total_tasks:
            feedback = ""  # All done, no feedback needed
            print("  → All tasks completed! 🎉")
        else:
            feedback = "Daily plan complete, but more tasks remain for future days"
            print(f"  → Daily plan complete, {total_tasks - completed_count} tasks remain")
    else:
        feedback = f"Daily plan incomplete: {unfinished_count} tasks remain unfinished"
        print(f"  → {unfinished_count} tasks remain unfinished")
        print("  → These tasks need replanning:")
        for task_name in state["daily_plan"]:
            print(f"    • {task_name}")
    
    return {**state, "feedback": feedback}


def replan(state: AgentState) -> AgentState:
    """
    Adjust the plan by moving unfinished tasks back to available tasks.
    
    This node handles replanning by taking unfinished tasks from the daily plan
    and making them available for future planning with higher priority.
    
    Args:
        state: Current agent state with feedback
        
    Returns:
        Updated state with cleared daily plan for replanning
    """
    print("\n🔄 Replanning based on feedback...")
    
    if not state["daily_plan"]:
        print("  → No tasks to replan")
        return {**state, "feedback": ""}
    
    unfinished_count = len(state["daily_plan"])
    print(f"  → Moving {unfinished_count} unfinished tasks back to planning")
    
    # In this simple implementation, we just clear the daily plan
    # The unfinished tasks will be picked up in the next planning cycle
    # since they're still in the main tasks list and not in completed_tasks
    
    for task_name in state["daily_plan"]:
        print(f"    • {task_name} → back to planning")
    
    return {
        **state,
        "daily_plan": [],  # Clear daily plan for replanning
        "feedback": "Replanning complete - unfinished tasks available for next cycle"
    }


# Helper function to find task details by name
def get_task_by_name(tasks: list, task_name: str) -> Dict[str, Any]:
    """
    Find a task dictionary by its name.
    
    Args:
        tasks: List of task dictionaries
        task_name: Name of the task to find
        
    Returns:
        Task dictionary if found, empty dict otherwise
    """
    for task in tasks:
        if task["name"] == task_name:
            return task
    return {}
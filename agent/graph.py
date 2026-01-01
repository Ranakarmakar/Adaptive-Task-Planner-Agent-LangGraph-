"""
LangGraph Workflow

This module creates the LangGraph StateGraph that orchestrates the agent's
planning, execution, reflection, and replanning cycle.
"""

from langgraph.graph import StateGraph, START, END
from .state import AgentState
from .nodes import plan_tasks, execute_day, reflect, replan


def should_continue_after_reflect(state: AgentState) -> str:
    """
    Conditional edge function to determine next step after reflection.
    
    Args:
        state: Current agent state after reflection
        
    Returns:
        Next node name or END based on feedback
    """
    if state["feedback"] and "incomplete" in state["feedback"]:
        # If there's feedback about incomplete tasks, go to replanning
        return "replan"
    else:
        # If no feedback or tasks are done, end the workflow
        return END


def create_agent_graph() -> StateGraph:
    """
    Create and configure the LangGraph StateGraph for the agent workflow.
    
    Returns:
        Compiled StateGraph ready for execution
    """
    print("🏗️ Building LangGraph workflow...")
    
    # Initialize the StateGraph with our AgentState schema
    workflow = StateGraph(AgentState)
    
    # Add nodes to the graph
    workflow.add_node("plan_tasks", plan_tasks)
    workflow.add_node("execute_day", execute_day)
    workflow.add_node("reflect", reflect)
    workflow.add_node("replan", replan)
    
    # Define the workflow edges
    # START → plan_tasks (entry point)
    workflow.add_edge(START, "plan_tasks")
    
    # plan_tasks → execute_day
    workflow.add_edge("plan_tasks", "execute_day")
    
    # execute_day → reflect
    workflow.add_edge("execute_day", "reflect")
    
    # reflect → END or replan (conditional)
    workflow.add_conditional_edges(
        "reflect",
        should_continue_after_reflect,
        {
            "replan": "replan",
            END: END
        }
    )
    
    # replan → execute_day (continue the cycle)
    workflow.add_edge("replan", "execute_day")
    
    print("✅ LangGraph workflow created successfully")
    
    # Compile and return the graph
    return workflow.compile()


def run_agent_workflow(initial_state: AgentState, max_iterations: int = 10) -> AgentState:
    """
    Execute the agent workflow with the given initial state.
    
    Args:
        initial_state: Starting state with tasks
        max_iterations: Maximum number of workflow cycles to prevent infinite loops
        
    Returns:
        Final state after workflow completion
    """
    print("\n🚀 Starting Adaptive Task Planner Agent")
    print("="*60)
    
    # Create the compiled workflow
    app = create_agent_graph()
    
    try:
        # Execute the workflow
        print("\n🎬 Executing workflow...")
        final_state = app.invoke(initial_state)
        
        print("\n🏁 Workflow completed successfully!")
        return final_state
        
    except Exception as e:
        print(f"\n❌ Workflow execution failed: {e}")
        raise
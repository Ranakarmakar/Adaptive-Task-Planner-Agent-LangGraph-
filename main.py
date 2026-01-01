"""
Main Runner for Adaptive Task Planner Agent

This script demonstrates the agent's capabilities by running it with
sample tasks and displaying the results.
"""

from agent import create_initial_state, run_agent_workflow, print_state_summary


def create_sample_tasks():
    """
    Create a set of sample tasks for demonstration.
    
    Returns:
        List of task dictionaries with realistic data
    """
    return [
        {
            "name": "Review project requirements",
            "deadline": "2024-01-15T09:00:00",
            "estimated_hours": 2.0
        },
        {
            "name": "Design system architecture",
            "deadline": "2024-01-15T17:00:00", 
            "estimated_hours": 4.0
        },
        {
            "name": "Set up development environment",
            "deadline": "2024-01-16T12:00:00",
            "estimated_hours": 1.5
        },
        {
            "name": "Implement core features",
            "deadline": "2024-01-17T17:00:00",
            "estimated_hours": 6.0
        },
        {
            "name": "Write unit tests",
            "deadline": "2024-01-18T15:00:00",
            "estimated_hours": 3.0
        },
        {
            "name": "Create documentation",
            "deadline": "2024-01-19T17:00:00",
            "estimated_hours": 2.0
        }
    ]


def main():
    """
    Main function that runs the Adaptive Task Planner Agent demo.
    """
    print("🎭 ADAPTIVE TASK PLANNER AGENT DEMO")
    print("="*60)
    print("This demo shows an AI agent that plans tasks, executes them,")
    print("reflects on progress, and replans when needed using LangGraph.")
    print("="*60)
    
    # Create sample tasks
    sample_tasks = create_sample_tasks()
    
    print(f"\n📋 Sample Tasks ({len(sample_tasks)} total):")
    for i, task in enumerate(sample_tasks, 1):
        print(f"  {i}. {task['name']}")
        print(f"     Due: {task['deadline']} ({task['estimated_hours']}h)")
    
    # Initialize agent state
    initial_state = create_initial_state(sample_tasks)
    
    # Run the agent workflow
    try:
        final_state = run_agent_workflow(initial_state)
        
        # Display final results
        print_state_summary(final_state)
        
        # Analysis
        total_tasks = len(final_state["tasks"])
        completed_tasks = len(final_state["completed_tasks"])
        completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        
        print(f"\n📊 FINAL ANALYSIS:")
        print(f"  Completion Rate: {completion_rate:.0f}% ({completed_tasks}/{total_tasks})")
        
        if final_state["feedback"]:
            print(f"  Status: {final_state['feedback']}")
        else:
            print(f"  Status: All planned tasks completed successfully!")
        
        print(f"\n✨ The agent demonstrated:")
        print(f"  • Intelligent task planning based on deadlines")
        print(f"  • Simulated task execution")
        print(f"  • Reflection on progress and unfinished work")
        print(f"  • Dynamic replanning when tasks remain incomplete")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Make sure you have installed the required dependencies:")
        print("pip install -r requirements.txt")


if __name__ == "__main__":
    main()
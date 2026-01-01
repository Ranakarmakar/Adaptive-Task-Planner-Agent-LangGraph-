"""
Streamlit Demo UI for Adaptive Task Planner Agent

A simple web interface to demonstrate the LangGraph-based task planning agent.
"""

import streamlit as st
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Import agent components
from agent import create_initial_state, run_agent_workflow, print_state_summary


def create_default_tasks() -> List[Dict[str, Any]]:
    """Create default sample tasks for the demo."""
    base_date = datetime.now()
    return [
        {
            "name": "Review project requirements",
            "deadline": (base_date + timedelta(hours=8)).isoformat(),
            "estimated_hours": 2.0
        },
        {
            "name": "Design system architecture",
            "deadline": (base_date + timedelta(hours=16)).isoformat(),
            "estimated_hours": 4.0
        },
        {
            "name": "Set up development environment",
            "deadline": (base_date + timedelta(days=1, hours=4)).isoformat(),
            "estimated_hours": 1.5
        },
        {
            "name": "Implement core features",
            "deadline": (base_date + timedelta(days=2, hours=8)).isoformat(),
            "estimated_hours": 6.0
        },
        {
            "name": "Write unit tests",
            "deadline": (base_date + timedelta(days=3)).isoformat(),
            "estimated_hours": 3.0
        },
        {
            "name": "Create documentation",
            "deadline": (base_date + timedelta(days=4)).isoformat(),
            "estimated_hours": 2.0
        }
    ]


def format_datetime(iso_string: str) -> str:
    """Format ISO datetime string for display."""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return iso_string


def display_tasks_table(tasks: List[Dict[str, Any]]):
    """Display tasks in a simple table format without pandas."""
    if not tasks:
        st.info("No tasks available.")
        return
    
    # Create table headers
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        st.write("**Task Name**")
    with col2:
        st.write("**Deadline**")
    with col3:
        st.write("**Hours**")
    
    st.divider()
    
    # Display each task
    for task in tasks:
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(task["name"])
        with col2:
            st.write(format_datetime(task["deadline"]))
        with col3:
            st.write(f"{task['estimated_hours']}h")


def main():
    """Main Streamlit application."""
    
    # Page configuration
    st.set_page_config(
        page_title="Adaptive Task Planner Agent Demo",
        page_icon="🎭",
        layout="wide"
    )
    
    # Header
    st.title("🎭 Adaptive Task Planner Agent Demo")
    st.markdown("---")
    
    # Description
    st.markdown("""
    This demo showcases an AI agent built with **LangGraph 1.0** that intelligently plans tasks, 
    simulates execution, reflects on progress, and dynamically replans when needed.
    
    **How it works:**
    1. **Plan** - Sorts tasks by deadline and creates daily schedule (max 8 hours)
    2. **Execute** - Simulates completing one task at a time
    3. **Reflect** - Analyzes progress and identifies unfinished work
    4. **Replan** - Moves incomplete tasks back for future planning
    """)
    
    # Sidebar for task management
    st.sidebar.header("📋 Task Management")
    
    # Initialize session state
    if 'tasks' not in st.session_state:
        st.session_state.tasks = create_default_tasks()
    if 'agent_state' not in st.session_state:
        st.session_state.agent_state = None
    if 'execution_log' not in st.session_state:
        st.session_state.execution_log = []
    
    # Task input section
    with st.sidebar.expander("➕ Add New Task", expanded=False):
        with st.form("add_task"):
            task_name = st.text_input("Task Name")
            deadline_date = st.date_input("Deadline Date", value=datetime.now().date())
            deadline_time = st.time_input("Deadline Time", value=datetime.now().time())
            estimated_hours = st.number_input("Estimated Hours", min_value=0.5, max_value=12.0, value=2.0, step=0.5)
            
            if st.form_submit_button("Add Task"):
                if task_name:
                    deadline_datetime = datetime.combine(deadline_date, deadline_time)
                    new_task = {
                        "name": task_name,
                        "deadline": deadline_datetime.isoformat(),
                        "estimated_hours": estimated_hours
                    }
                    st.session_state.tasks.append(new_task)
                    st.success(f"Added task: {task_name}")
                    st.rerun()
    
    # Reset tasks button
    if st.sidebar.button("🔄 Reset to Default Tasks"):
        st.session_state.tasks = create_default_tasks()
        st.session_state.agent_state = None
        st.session_state.execution_log = []
        st.success("Reset to default tasks!")
        st.rerun()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📋 Current Tasks")
        
        # Display tasks using custom table
        display_tasks_table(st.session_state.tasks)
        
        # Task management
        if len(st.session_state.tasks) > 0:
            st.subheader("Remove Task")
            task_to_remove = st.selectbox(
                "Select task to remove:",
                options=[""] + [task["name"] for task in st.session_state.tasks],
                key="remove_task"
            )
            
            if st.button("🗑️ Remove Selected Task") and task_to_remove:
                st.session_state.tasks = [
                    task for task in st.session_state.tasks 
                    if task["name"] != task_to_remove
                ]
                st.success(f"Removed task: {task_to_remove}")
                st.rerun()
    
    with col2:
        st.header("🤖 Agent Execution")
        
        # Run agent button
        if st.button("🚀 Run Agent Workflow", type="primary", use_container_width=True):
            if not st.session_state.tasks:
                st.error("Please add some tasks first!")
            else:
                with st.spinner("Running agent workflow..."):
                    try:
                        # Create initial state
                        initial_state = create_initial_state(st.session_state.tasks)
                        
                        # Capture execution in session state
                        st.session_state.execution_log = []
                        
                        # Run the agent workflow
                        final_state = run_agent_workflow(initial_state)
                        st.session_state.agent_state = final_state
                        
                        st.success("Agent workflow completed successfully!")
                        
                    except Exception as e:
                        st.error(f"Agent execution failed: {str(e)}")
                        st.error("Make sure you have installed the required dependencies: `pip install -r requirements.txt`")
        
        # Display agent state if available
        if st.session_state.agent_state:
            st.subheader("📊 Agent Results")
            
            state = st.session_state.agent_state
            
            # Metrics
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("Total Tasks", len(state["tasks"]))
            
            with col_b:
                st.metric("Completed", len(state["completed_tasks"]))
            
            with col_c:
                completion_rate = (len(state["completed_tasks"]) / len(state["tasks"]) * 100) if state["tasks"] else 0
                st.metric("Completion Rate", f"{completion_rate:.0f}%")
            
            # Current daily plan
            if state["daily_plan"]:
                st.subheader("📅 Current Daily Plan")
                for i, task_name in enumerate(state["daily_plan"], 1):
                    st.write(f"{i}. {task_name}")
            
            # Completed tasks
            if state["completed_tasks"]:
                st.subheader("✅ Completed Tasks")
                for task_name in state["completed_tasks"]:
                    st.write(f"✓ {task_name}")
            
            # Feedback
            if state["feedback"]:
                st.subheader("💭 Agent Feedback")
                st.info(state["feedback"])
    
    # Full-width section for detailed analysis
    st.markdown("---")
    st.header("📈 Detailed Analysis")
    
    if st.session_state.agent_state:
        state = st.session_state.agent_state
        
        # Task status breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Task Status Breakdown")
            
            completed_tasks = set(state["completed_tasks"])
            planned_tasks = set(state["daily_plan"])
            
            # Display task status without pandas
            st.write("**Task Status:**")
            for task in state["tasks"]:
                task_name = task["name"]
                if task_name in completed_tasks:
                    status = "✅ Completed"
                elif task_name in planned_tasks:
                    status = "📅 Planned"
                else:
                    status = "⏳ Pending"
                
                col_task, col_status, col_deadline, col_hours = st.columns([3, 2, 2, 1])
                with col_task:
                    st.write(task_name)
                with col_status:
                    st.write(status)
                with col_deadline:
                    st.write(format_datetime(task["deadline"]))
                with col_hours:
                    st.write(f"{task['estimated_hours']}h")
        
        with col2:
            st.subheader("Agent Workflow Summary")
            
            total_tasks = len(state["tasks"])
            completed_count = len(state["completed_tasks"])
            planned_count = len(state["daily_plan"])
            pending_count = total_tasks - completed_count - planned_count
            
            st.write(f"**Total Tasks:** {total_tasks}")
            st.write(f"**Completed:** {completed_count}")
            st.write(f"**Currently Planned:** {planned_count}")
            st.write(f"**Pending:** {pending_count}")
            
            if completed_count == total_tasks:
                st.success("🎉 All tasks completed successfully!")
            elif state["feedback"]:
                st.warning(f"⚠️ {state['feedback']}")
            
            # Agent capabilities demonstrated
            st.subheader("✨ Demonstrated Capabilities")
            st.write("✓ Intelligent task planning based on deadlines")
            st.write("✓ Simulated task execution")
            st.write("✓ Progress reflection and analysis")
            st.write("✓ Dynamic replanning when needed")
    
    else:
        st.info("Run the agent workflow to see detailed analysis results.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Built with ❤️ using:**
    - [LangGraph 1.0](https://langchain-ai.github.io/langgraph/) for workflow orchestration
    - [LangChain 0.3](https://python.langchain.com/) for AI framework
    - [Streamlit](https://streamlit.io/) for the web interface
    - Python for the agent implementation
    """)


if __name__ == "__main__":
    main()
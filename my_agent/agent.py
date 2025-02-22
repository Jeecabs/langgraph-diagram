# agent.py

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from my_agent.utils.state import AgentState
from my_agent.utils.nodes import (
    data_ingestion_node,
    workflow_analysis_node,
    recommendation_node,
    dashboard_ui_node,
    human_review_node,
    deployment_node,
    feedback_node
)

class GraphConfig(TypedDict):
    model_name: Literal["anthropic", "openai"]
    auto_approve: bool
    max_cycles: int  # Add maximum cycle counter

# Initialize the state graph with updated config
workflow = StateGraph(AgentState, config_schema=GraphConfig)

# Add nodes for each stage of the process
workflow.add_node("data_ingestion", data_ingestion_node)
workflow.add_node("workflow_analysis", workflow_analysis_node)
workflow.add_node("automation_recommendation", recommendation_node)
workflow.add_node("dashboard_ui", dashboard_ui_node)
workflow.add_node("human_review", human_review_node)
workflow.add_node("deploy_workflows", deployment_node)
workflow.add_node("collect_feedback", feedback_node)

# Set initial entry point
workflow.set_entry_point("data_ingestion")

# Main forward flow
workflow.add_edge("data_ingestion", "workflow_analysis")
workflow.add_edge("workflow_analysis", "automation_recommendation")
workflow.add_edge("automation_recommendation", "dashboard_ui")
workflow.add_edge("dashboard_ui", "human_review")

# Human review conditional flow with cycle limit
def route_human_decision(state):
    if state.get("approval"):
        return "approved"
    if state.get("review_cycles", 0) >= 3:  # Max 3 rejection cycles
        return "max_rejected"
    return "rejected"

workflow.add_conditional_edges(
    "human_review",
    route_human_decision,
    {
        "approved": "deploy_workflows",
        "rejected": "workflow_analysis",
        "max_rejected": END  # Termination point for stuck workflows
    }
)

# Deployment and feedback flow with cycle control
def should_continue(state, config):
    return "continue" if state.get("cycle_count", 0) < config["max_cycles"] else "end"

workflow.add_conditional_edges(
    "collect_feedback",
    should_continue,
    {
        "continue": "data_ingestion",
        "end": END
    }
)

workflow.add_edge("deploy_workflows", "collect_feedback")

# Compile the final workflow
graph = workflow.compile()